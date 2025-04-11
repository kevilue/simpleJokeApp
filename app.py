from flask import Flask, render_template, request, send_from_directory
import pymongo
import json
from dotenv import load_dotenv
import os

# Load environment variables
try:
    load_dotenv()
except:
    print("No .env file found.")
try:
    MONGO_URI = os.environ.get("MONGO_URI")
except:
    print("No MONGO_URI found in .env file -> using localhost address.")
    MONGO_URI = "mongodb://localhost:27017/"

app = Flask(__name__)

client = pymongo.MongoClient(MONGO_URI)
db = client["jokes"]
collection = db["pub"]

@app.route("/", methods=["GET", "POST"])
def index():
    """Renders and returns the main page."""
    return render_template("index.html")

@app.route("/index.js")
def send_js():
    """Returns the javascript file for the main page."""
    # Use send_from_directory to send the file and avoid directory traversal attacks
    return send_from_directory("static", "index.js")

@app.route("/index.css")
def send_css():
    """Returns the css stylesheet for the index page."""
    return send_from_directory("static", "index.css")

@app.route("/post_joke", methods=["GET", "POST"])
def insert_joke_to_db():
    """Insert a joke from a json object to the database."""
    if request.method == "POST":
        data = request.data.decode("utf-8")
        if len(data) < 5000: data = json.loads(data) 
        else: return "Invalid request size"
        # Check if joke already exists in db
        exist_check = collection.count_documents({"joke": data["joke"]})
        print("Exist check: " + str(exist_check))	
        # Max size of request is 5000
        if exist_check == 0:
            print("Adding joke: " + data["joke"])
            # Insert joke to db
            collection.insert_one({"joke": data["joke"], "comments": []})
            return "Joke added to database"
        else: return "Joke already exists"

@app.route("/load_db", methods=["GET", "POST"])
def load_db():
    """Load jokes from database and return them as json."""
    if request.method == "GET":
        print("Loading database")
        # Find all documents
        cursor = collection.find({})
        if cursor:
            jokes = []
            # Append jokes
            for item in cursor:
                jokes.append({"joke": item["joke"], "comments": item["comments"]})
            return json.dumps(jokes)

@app.route("/post_comment", methods=["GET", "POST"])
def post_comment():
    """Post a comment to a joke in the database."""
    if request.method == "POST":
        data = request.data.decode("utf-8")
        # Max size of joke and comment
        if len(data) < 8000:
            data = json.loads(data)
            # Search for joke entry in db
            exist_entry = collection.find_one({"joke": data["joke"]})
            try:
                if len(exist_entry["joke"]) > 0 and len(data["comment"]) > 0:
                    comments = exist_entry["comments"]
                    if not data["comment"] in comments:
                        print("Adding comment: " + data["comment"])
                        # Update comments
                        collection.update_one({"joke": data["joke"]}, {"$push": {"comments": data["comment"]}})
                    else:
                        print("Comment already exists.")
                        return "Comment already exists"
                else: 
                    print("Empty comment.")
                    return "Empty comment"
            # If joke not found, try adding joke and comment
            except: 
                if len(data["comment"]) > 0:
                    collection.insert_one({"joke": data["joke"], "comments": [data["comment"]]})
                    print("Joke not found. Joke and comment added.")
                    return "Joke and comment added."
                else:
                    print("Empty comment.")
                    return "Empty comment"
            return "Comment added"
        else: return "Invalid request size"

# Run
if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")