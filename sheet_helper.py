# sheet_helper.py
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import WorksheetNotFound

# --------------------------
# 1️⃣ Define API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# --------------------------
# 2️⃣ Initialize variables
CREDS = None
client = None
sheet = None

# --------------------------
# 3️⃣ Load credentials safely
try:
    if "GOOGLE_CREDS" in os.environ:
        # Load from Render environment variable (recommended)
        creds_json = json.loads(os.environ["GOOGLE_CREDS"])
        CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
        print("[INFO] Loaded Google credentials from environment variable.")
    else:
        # Load from local file (for local testing)
        CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        print("[INFO] Loaded Google credentials from local file.")

    # Authorize gspread client
    client = gspread.authorize(CREDS)

    # --------------------------
    # 4️⃣ Open Google Sheet
    SPREADSHEET_ID = "1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI"
    SHEET_NAME = "Break Logs"

    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        print(f"[INFO] Connected to Google Sheet: '{SHEET_NAME}'")
    except WorksheetNotFound:
        print(f"[ERROR] Worksheet '{SHEET_NAME}' not found in the spreadsheet.")
        sheet = None

except Exception as e:
    print(f"[ERROR] Could not connect to Google Sheet: {e}")
    sheet = None

# --------------------------
# 5️⃣ Function to append a row safely
def append_break_log(agent_name, break_start, break_end, duration, date_str):
    """
    Appends a new break log row to the Google Sheet.
    Skips if the sheet is not available.
    """
    if sheet is None:
        print("[WARNING] Google Sheet not available. Skipping append.")
        return

    try:
        sheet.append_row([agent_name, break_start, break_end, duration, date_str])
        print(f"[INFO] Row appended for {agent_name} on {date_str}")
    except Exception as e:
        print(f"[ERROR] Failed to append row: {e}")
