# Dockerfile
FROM python:3.9

WORKDIR /app

# Instala o nano e outras ferramentas úteis
RUN apt-get update && apt-get install -y nano vim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
