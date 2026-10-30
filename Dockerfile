FROM python:3.10-slim

# Install ffmpeg and nodejs (yt-dlp အတွက် မရှိမဖြစ် လိုအပ်ပါသည်)
RUN apt-get update && apt-get install -y ffmpeg nodejs

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
