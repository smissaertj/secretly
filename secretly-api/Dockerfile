# Base python package
FROM python:3.10.6-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the files
COPY . .

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]