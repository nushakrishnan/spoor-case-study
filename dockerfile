FROM python:3.9-slim
FROM ultralytics/ultralytics:latest-cpu
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r req.txt
ENTRYPOINT ["python", "run.py"]


