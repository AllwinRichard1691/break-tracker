# sheet_helper.py
import gspread
from google.oauth2.service_account import Credentials
import os
import json

# --------------------------
# 1️⃣ API Scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# --------------------------
# 2️⃣ Load credentials safely
CREDS = None
client = None
sheet = None

try:
    if "GOOGLE_CREDS" in os.environ:
        # Load from Render environment variable
        creds_json = json.loads(os.environ["GOOGLE_CREDS"])
        CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    else:
        # Load from local file
        CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    
    client = gspread.authorize(CREDS)

    # --------------------------
    # 3️⃣ Open your Google Sheet
    SPREADSHEET_ID = "1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI"
    SHEET_NAME = "Break Logs"
    sheet = client.open_by_key("1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI").worksheet("Break Logs")
except Exception as e:
    print(f"[ERROR] Could not connect to Google Sheet: {e}")
    sheet = None

# --------------------------
# 4️⃣ Append a row safely
def append_break_log(agent_name, break_start, break_end, duration, date_str):
    if sheet is None:
        print("[WARNING] Google Sheet not available. Skipping append.")
        return
    try:
        sheet.append_row([agent_name, break_start, break_end, duration, date_str])
        print(f"[INFO] Row appended for {agent_name} on {date_str}")
    except Exception as e:
        print(f"[ERROR] Failed to append row: {e}")
