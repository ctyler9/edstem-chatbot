FROM python:3.10-slim

ENV PORT=8501 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8501 

CMD ["streamlit", "run", "app.py", "--server.port=8501"]

#"--server.address=localhost"]
