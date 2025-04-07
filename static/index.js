/*
index.js
Javascript code for index.html

*/

// Event listener for commment form submission
document.getElementById('comment-form').addEventListener('submit', function(event) {
    // Prevent the default form submission
    event.preventDefault();
    
    // Get form data
    let formData = new FormData(this);
    $.ajax({
        type: "POST",
        url: "/post_comment",
        data: JSON.stringify({
            joke: $("#joke-content").text(),
            comment: formData.get('comment')
        }),
        contentType: "application/json; charset=UTF-8",
        success: function(data){
            console.log(data);
        },
        error: function(err){
            console.log(err);
        }
    });
});

// Function to load jokes and comments in the database
function loadDatabase(){
    console.log("Loading Database")
    $.ajax({
        type: "GET",
        url: "/load_db",
        success: function(data){
            console.log(data)
            data = JSON.parse(data)
            // Build html table from data
            let commentList = "<tr>\n\t<th>Joke</th>\n\t<th>Comment</th>\n</tr>";
            for(let i=0; i<data.length; i++){
                commentList += "<tr>\n\t<td>" + data[i].joke + "</td>\n\t<td>";
                for(let j=0; j<data[i].comments.length; j++){
                    if(j == 0){
                        commentList += "\n\t<ul>";
                    }
                    commentList += "<li>" + data[i].comments[j] + "</li>";
                    if(j == data[i].comments.length - 1){
                        commentList += "\n\t</ul>";
                    }
                }
                commentList += "\n\t</td>\n</tr>";
            }
            // Show html table
            $("#db-content").html(commentList);
        }
    })
}

// Function to get a joke from the API and set response in joke-content div
function getJoke(){
    $.ajax({
        url: "https://official-joke-api.appspot.com/random_joke",
        type: "GET",
        success: function(data){
            $("#joke-content").text(data.setup + " " + data.punchline);
            $("#save-joke-button").show();
            $("#comment-form").show();
            $("#comment").val("");
        }
    });
}


// Function to post a joke to the database
function postJoke(){
    $.ajax({
        type: "POST",
        url: "/post_joke",
        data: JSON.stringify({
            joke: $("#joke-content").text()
        }),
        contentType: "application/json; charset=UTF-8"
    })

}