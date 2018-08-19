FROM arm32v7/python:3.7.0-slim

WORKDIR /usr/src/shitpostd
COPY ./requirements.txt ./shitpostd.py ./

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "shitpostd.py"]
