FROM tiangolo/uwsgi-nginx:python3.12

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV STATIC_URL=/static
ENV STATIC_PATH=/static

ENV STATIC_INDEX 0

COPY . /app

WORKDIR /app
ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["python", "app.py"]