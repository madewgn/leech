FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y ffmpeg python3 python3-pip && \
    apt-get clean
RUN pip3 installl -r req.txt
CMD ["python3", "bot.py"]
