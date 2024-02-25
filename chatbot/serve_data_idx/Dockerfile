FROM python:3.10-slim

ENV INDEX_NAME="class_files_full"
ENV INDEX_ROOT=".ragatouille/colbert/indexes"
ENV PORT=8893

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "server.py"]
