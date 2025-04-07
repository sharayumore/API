FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Use Gunicorn to run the app (assuming your Flask app is in `main.py` and the app is called `app`)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]