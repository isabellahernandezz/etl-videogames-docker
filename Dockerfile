cat > Dockerfile << 'EOF'
FROM python:3.10-slim

RUN useradd -m app
USER app

WORKDIR /app
RUN mkdir -p /app/output

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "ETL.py", "--input", "genres_v2.csv", "--out-dir", "output"]
EOF
