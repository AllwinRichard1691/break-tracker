from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
from datetime import datetime, timedelta
import os
from io import BytesIO

app = Flask(__name__)

# ===== Configuration =====
CSV_FILE = "break_logs.csv"
ALLOWED_IPS = {"14.194.67.222"}  # Office public IP
ADMIN_PASSWORD = "Agrim@123"

AGENTS = [
    "Md Khushdil", "Riya", "Tarun Kumar", "Jyoti Pal", "Shakshi",
    "Jyoti Punera", "Kumari Apurva Pandey", "Garima Singh", "Bhavesh Karki",
    "Rahul Chandel", "Pooja Pandit", "Shubham Kumar", "Arpit Aryan",
    "Jahangir Alam", "Umesh Pandey", "Kajal Pandey", "Ravikant Dubey",
    "Deepanshu Singh", "Deepak Kumar", "Shareen Khushboo", "Sapna Yadav",
    "Mukesh Kumar", "Himanshi Rana", "Pinky", "Inderjot Sandhu",
    "Puneet Singh", "Kritanjli Atri", "Neha Kumari", "Vishal Singh 1",
    "Rishabh Srivastava", "Lokesh", "Shubham Kumar", "Mahima Mehta",
    "Mehebub Jahidi", "Rishabh Tripathi", "Kajal Kumari", "Nischal Rai",
    "Suryansh", "Deepak kumar", "Rahul Kumar"
]

# ===== Helper: Get actual client IP =====
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr

# ===== Restrict access to office IP =====
@app.before_request
def restrict_ip():
    client_ip = get_client_ip()
    if client_ip not in ALLOWED_IPS:
        return f"Access Denied. Your IP ({client_ip}) is not authorized.", 403

# ===== Ensure CSV exists =====
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agent", "Start Time", "End Time", "Duration (mins)", "Date"])

# ===== Home Page (Break Tracker) =====
@app.route("/", methods=["GET", "POST"])
def index():
    today = (datetime.now() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")
    agent_logs = []
    selected_agent = None

    if request.method == "POST":
        selected_agent = request.form["agent"]
        action = request.form["action"]
        now = datetime.now() + timedelta(hours=5, minutes=30)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        with open(CSV_FILE, "r") as file:
            rows = list(csv.reader(file))

        # Find open break for agent today
        last_open = None
        for row in reversed(rows):
            if row[0] == selected_agent and row[2] == "" and row[4] == today:
                last_open = row
                break

        if action == "start":
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([selected_agent, time_str, "", "", date_str])

        elif action == "end" and last_open:
            start_time = datetime.strptime(last_open[1], "%H:%M:%S")
            duration = (now - start_time).seconds // 60

            for i in range(len(rows)):
                if rows[i] == last_open:
                    rows[i][2] = time_str
                    rows[i][3] = duration
                    break

            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        return redirect(url_for("index", agent=selected_agent))

    # For GET — show logs for selected agent
    selected_agent = request.args.get("agent")
    if selected_agent:
        with open(CSV_FILE, "r") as file:
            rows = list(csv.reader(file))
            agent_logs = [row for row in rows if row[0] == selected_agent and row[4] == today]

    return render_template("index.html", agents=AGENTS, logs=agent_logs, selected_agent=selected_agent)

# ===== Admin Panel & CSV Download =====
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    data = None

    if request.method == "POST":
        password = request.form.get("password", "")
        if password != ADMIN_PASSWORD:
            error = "Invalid password"
        else:
            # Read CSV for logs
            with open(CSV_FILE, "r", newline="") as file:
                rows = list(csv.reader(file))
            data = rows

            # Handle CSV download
            if request.form.get("download") == "csv":
                csv_content = "\n".join([",".join(row) for row in rows])
                buffer = BytesIO()
                buffer.write(csv_content.encode('utf-8'))
                buffer.seek(0)
                return send_file(
                    buffer,
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name="break_logs.csv"
                )

    return render_template("admin.html", error=error, data=data)

# ===== Run Server =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
