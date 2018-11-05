FROM python:2.7
RUN apt-get update && apt-get install -y netcat
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"] 