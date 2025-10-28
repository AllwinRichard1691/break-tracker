# test_sheet.py
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)

client = gspread.authorize(CREDS)

SPREADSHEET_ID = "1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI"
SHEET_NAME = "Break Logs"

try:
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    sheet.append_row(["Test Agent", "09:00", "09:15", "15 mins", "2025-10-28"])
    print("✅ Row appended successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
