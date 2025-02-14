FROM python:3.8

WORKDIR /app

ENV SECRET_KEY="gfdmhghif38yrf9ew0jkf32"

ENV JWT_SECRET="d3f73888-f725-41f2-ae33-df5bbaf99cbc"

COPY ./ /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]