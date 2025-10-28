import gspread
from google.oauth2.service_account import Credentials

# --------------------------
# 1️⃣ Set your scopes
# Only Sheets API is needed
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# --------------------------
# 2️⃣ Load service account credentials
CREDS = Credentials.from_service_account_file(
    "service_account.json",  # Path to your service account JSON
    scopes=SCOPES
)

# --------------------------
# 3️⃣ Authorize gspread client
client = gspread.authorize(CREDS)

# --------------------------
# 4️⃣ Open sheet by ID (replace with your actual spreadsheet ID)
SPREADSHEET_ID = "1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI"
sheet = client.open_by_key("1_x1ybwJbbOdeKY5Be-RbYtJ9I2VkpPYUUqgVBWQoDTI").worksheet("Break Logs")

# --------------------------
# 5️⃣ Read all records
records = sheet.get_all_records()
print("Current Sheet Data:")
for row in records:
    print(row)

# --------------------------
# 6️⃣ Optional: Append a new row
# new_row = ["2025-10-28 09:00", "2025-10-28 09:15", "Coffee Break"]
# sheet.append_row(new_row)
