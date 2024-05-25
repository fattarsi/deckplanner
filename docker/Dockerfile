FROM python:3

EXPOSE 8000
WORKDIR /
#COPY . /
COPY app/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir
ENTRYPOINT ["/app/docker/entrypoint.sh"]