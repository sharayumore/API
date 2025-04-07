
from flask import Blueprint, request, jsonify, render_template
from .limiter import is_rate_limited

main = Blueprint('main', __name__)

@main.route("/")
def dashboard():
    return render_template("dashboard.html")

@main.route("/api/data")
def api_data():
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return jsonify({"error": "Too Many Requests"}), 429
    return jsonify({"message": "Here is your data."})
