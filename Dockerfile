FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip
WORKDIR /app
ENV FLASK_DEBUG=1
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
CMD ["python3", "run.py"]