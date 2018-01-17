FROM python:3.6.4
RUN pip install requests==2.5.1 \
                itchat==1.3.10
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY src /app
WORKDIR /app

ENTRYPOINT ["python","main.py"]