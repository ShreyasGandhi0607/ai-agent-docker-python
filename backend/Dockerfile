FROM python:3.13.4-slim-bullseye

# host.docker.internal -> localhost
# curl -X POST -d '{"message":"Hello world"}' http://host.docker.internal:8000/api/chat/
RUN apt-get update && apt-get install -y curl

# create a python virtual enviroment
# isolate our python app  and installs from system level requirements   
RUN  python -m venv /opt/venv/

# python path
ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app


# Copy local_folder/file container_destination
COPY requirements.txt .

# run within container while building
RUN pip install --upgrade pip && pip install -r requirements.txt


# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
