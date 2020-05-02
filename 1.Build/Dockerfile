FROM python:rc-buster
RUN pip install flask
WORKDIR /app
EXPOSE 5000
COPY flask-monitor.py /app
ENTRYPOINT [ "python" ]
CMD [ "flask-monitor.py" ]
