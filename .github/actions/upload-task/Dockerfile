FROM python:3.13-slim
COPY entrypoint.sh /entrypoint.sh
COPY upload_task.py /upload_task.py
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]