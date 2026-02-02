# Official Python base image (3.10 ya 3.11 recommended)
FROM python:3.11-slim

# Working directory andar set karo
WORKDIR /app

# Requirements file copy karo aur dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora project copy karo
COPY . .

# FastAPI ko 7860 port pe chalao (Hugging Face Spaces ka default port)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]