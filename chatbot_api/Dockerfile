# chatbot_api/Dockerfile

FROM python:3.11.5

WORKDIR /app
COPY ./src /app/src

COPY requirements.txt /app/
COPY entrypoint.sh /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]