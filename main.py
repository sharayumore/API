from flask import Flask, jsonify, request, render_template
import redis
import time

app = Flask(__name__)

# Connect to Redis (important: use 'redis' as host name since it's the Docker service name)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Rate limiting settings
RATE_LIMIT = 5       # Max number of requests
WINDOW_SIZE = 60     # Time window in seconds

def is_rate_limited(ip):
    current_window = int(time.time() // WINDOW_SIZE)
    key = f"rate_limit:{ip}:{current_window}"
    count = r.get(key)

    if count is None:
        r.set(key, 1, ex=WINDOW_SIZE)
        return False
    elif int(count) < RATE_LIMIT:
        r.incr(key)
        return False
    else:
        return True

@app.route('/')
def home():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
    return jsonify({"message": "API is working!"})


# 🔥 Dashboard route
@app.route('/dashboard')
def dashboard():
    keys = r.keys("rate_limit:*")
    stats = {}

    for key in keys:
        parts = key.split(":")
        ip = parts[1]
        count = r.get(key)
        if ip in stats:
            stats[ip] += int(count)
        else:
            stats[ip] = int(count)

    return render_template('dashboard.html', stats=stats, per_ip=stats)


if __name__ == '__main__':
    app.run(debug=True)