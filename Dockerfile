FROM ubuntu:latest
LABEL name=rsb27
RUN apt update -qy
RUN apt install -qy python3.10 python3-pip python3.10-dev
ENV CHAT_ID=988347219
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python3", "iziQR_bot.py"]