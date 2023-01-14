FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y ffmpeg python3 python3-pip && \
    apt-get clean

WORKDIR /home

# Copy files:
COPY * /home

RUN pip3 install -r /home/requirements.txt
CMD ["python3", "/home/bot.py"]
