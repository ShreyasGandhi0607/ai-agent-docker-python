# declare what image to use
# from image_name : latest
FROM python:3.13.4-slim-bullseye

WORKDIR /app



# RUN mkdir -p /static_folder
# COPY ./static_frontend /static_folder
# u could have next.js application running here 
# react static app
# vue static app
# RUN echo "hello" > index.html 
# -> # linux command

# COPY ./static_frontend /app
# same destination is /app
COPY ./static_frontend .


# docker build -f Dockerfile -t dockerhub_name/pyapp:latest .
# docker run -it pyapp


# python -m http.server 8000
# docker run -it -p 3000:8000 pyapp
# docker run -it -p 8000:8000 pyapp
CMD ["python", "-m", "http.server", "8000"]
