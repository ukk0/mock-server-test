FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH="$PYTHONPATH:/app"

COPY requirements.txt /app/
RUN pip install --no-cache-dir pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["python", "main.py"]
