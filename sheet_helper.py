# sheet_helper.py
import gspread
from google.oauth2.service_account import Credentials

# --------------------------
# 1️⃣ Define API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# --------------------------
# 2️⃣ Load service account credentials from file
# Make sure 'service_account.json' is in the same folder
CREDS = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

# --------------------------
# 3️⃣ Authorize gspread client
client = gspread.authorize(CREDS)

# --------------------------
# 4️⃣ Open your Google Sheet by key
# Replace with your actual spreadsheet ID
SPREADSHEET_ID = "1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI"
sheet = client.open_by_key("1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI").worksheet("Break Logs")

# --------------------------
# 5️⃣ Function to append a row to the sheet
def append_break_log(agent_name, break_start, break_end, duration, date_str):
    """
    Appends a new break log row to the Google Sheet.

    Parameters:
    - agent_name: Name of the agent
    - break_start: Break start time (HH:MM)
    - break_end: Break end time (HH:MM)
    - duration: Duration string, e.g., "15 mins"
    - date_str: Date string (YYYY-MM-DD)
    """
    try:
        sheet.append_row([agent_name, break_start, break_end, duration, date_str])
        print(f"Row appended for {agent_name} on {date_str}")
    except Exception as e:
        print(f"Error appending row: {e}")
