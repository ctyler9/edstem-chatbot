FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["streamlit", "run", "app.py"]
