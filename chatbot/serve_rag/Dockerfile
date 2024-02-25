FROM python:3.10.13-bookworm

ENV PORT=8901

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["gunicorn", "-b", "0.0.0.0:8901", "server:app"]
