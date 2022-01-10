FROM alpine:3.15
EXPOSE 8080
WORKDIR /app
RUN apk add --no-cache uwsgi-python3 python3 cmd:pip3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir /uploads && chown uwsgi /uploads && chgrp uwsgi /uploads
CMD ["uwsgi", "--socket", "0.0.0.0:7070", "--protocol", "uwsgi", "--plugins", "python3", \
     "--wsgi-file", "app.py", "--callable", "app", "--uid", "uwsgi"]
