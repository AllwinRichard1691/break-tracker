from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# ---- CONFIG ----
AGENTS = [
    "Kajal Kumari", "Rishabh Tripathi", "Suryansh", "Deepak Kumar", "Mehebub Jahidi",
    "Mahima Mehta", "Apurva Pandey", "Vishal Singh 1", "Rishabh Srivastava", "Lokesh",
    "Kritanjli Atri", "Himanshi Rana ", "Mukesh Kumar", "Inderjot Sandhu", "Pinky Chauhan",
    "Puneet Pratap Singh", "Ravikant Dubey", "Sapna Yadav", "Shareen", "Umesh Pandey",
    "Kajal Pandey", "Shubham Kumar", "Arpit Aryan", "Pooja Pandit", "Bhavesh Karki",
    "Rahul Kumar", "Rahul Chandel", "Jyoti Punera", "Riya", "Tarun Kumar", "Hitesh", "Ajay L"
]
ADMIN_PASSWORD = "Agrim@123"  # change this for security
CSV_FILE = "break_logs.csv"

# ---- Initialize CSV ----
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agent", "Start Time", "End Time", "Duration (mins)", "Date"])

# ---- Home Page (Break Tracker) ----
@app.route("/", methods=["GET", "POST"])
def index():
    today = (datetime.now() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")  # +5:30 adjustment
    if request.method == "POST":
        agent = request.form["agent"]
        action = request.form["action"]
        now = datetime.now() + timedelta(hours=5, minutes=30)  # +5:30 adjustment
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Read existing data
        with open(CSV_FILE, "r") as file:
            rows = list(csv.reader(file))

        # Find the agent’s last open break
        last_open = None
        for row in reversed(rows):
            if row[0] == agent and row[2] == "" and row[4] == today:
                last_open = row
                break

        if action == "start":
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([agent, time_str, "", "", date_str])

        elif action == "end" and last_open:
            start_time = datetime.strptime(last_open[1], "%H:%M:%S")
            duration = (now - start_time).seconds // 60
            # Update the CSV
            for i in range(len(rows)):
                if rows[i] == last_open:
                    rows[i][2] = time_str
                    rows[i][3] = duration
                    break
            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        return redirect(url_for("index"))

    # Filter logs for today's breaks for the selected agent
    agent = request.args.get("agent")
    agent_logs = []
    if agent:
        with open(CSV_FILE, "r") as file:
            rows = list(csv.reader(file))
            agent_logs = [row for row in rows if row[0] == agent and row[4] == today]

    return render_template("index.html", agents=AGENTS, logs=agent_logs)


# ---- Admin Page (Password Protected) ----
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            with open(CSV_FILE, "r") as file:
                data = list(csv.reader(file))
            return render_template("admin.html", data=data)
        else:
            return render_template("admin.html", error="Invalid Password")
    return render_template("admin.html")


# ---- CSV Download ----
@app.route("/download", methods=["GET"])
def download_csv():
    # Optional: you can add password verification if needed
    return send_file(CSV_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
