import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('medical_hangman')
WORD_SHEET = SHEET.worksheet('word_list')

bones_words = WORD_SHEET.col_values(1)
organs_words = WORD_SHEET.col_values(2)
diseases_words = WORD_SHEET.col_values(3)
radiology_words = WORD_SHEET.col_values(4)

print(bones_words)
print(organs_words)
print(diseases_words)
print(radiology_words)


