FROM python:3.13-slim
COPY entrypoint.py /entrypoint.py
RUN pip install "requests>=2.32.3"
ENTRYPOINT [ "python3", "/entrypoint.py" ]