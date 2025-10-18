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
