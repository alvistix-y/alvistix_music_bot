FROM FROM python:3.10-slim

# Install ffmpeg and nodejs (yt-dlp JS runtime လိုအပ်ချက်အတွက်)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
