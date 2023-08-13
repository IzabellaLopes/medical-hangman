# Imports
import gspread
from google.oauth2.service_account import Credentials
import random

# List of scopes needed for accessing Google Sheets and Google Drive APIs
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

def authorize_google_sheets():
    """
    Authorizes the Google Sheets API using service account credentials.
    """
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    return GSPREAD_CLIENT

def select_random_word_from_sheet(sheet, column_number):
    """
    Selects a random word from a specified column in a Google Sheets worksheet.
            
    Returns:
        str or None: A randomly selected word or None if the word list is empty.
    """
    WORD_SHEET = sheet.worksheet('word_list')

    # Retrieve the values from the specified column in the 'word_list' worksheet
    words = WORD_SHEET.col_values(column_number)
    
    if not words:
        return None
    
    random_word = random.choice(words)
    return random_word

def create_hidden_word(word):
    """
    Creates a string of underscores to match the length of the input word.
    """
    return ' _ ' * len(word)

# Main function
def main():
    """
    Main function to demonstrate selecting random words from different categories.
    """
    GSPREAD_CLIENT = authorize_google_sheets()
    
    # Open the 'medical_hangman' Google Sheets 
    SHEET = GSPREAD_CLIENT.open('medical_hangman')
    
    # Select a random word from the 'bones' category (column 1)
    selected_bone_word = select_random_word_from_sheet(SHEET, 1)
    print("Randomly selected bone word:", selected_bone_word)
    
    hidden_bone_word = create_hidden_word(selected_bone_word)
    print("Hidden bone word:", hidden_bone_word)

    # Select a random word from the 'organs' category (column 2)
    selected_organs_word = select_random_word_from_sheet(SHEET, 2)
    print("Randomly selected organ word:", selected_organs_word)
    
    hidden_organs_word = create_hidden_word(selected_organs_word)
    print("Hidden organs word:", hidden_organs_word)

    # Select a random word from the 'diseases or conditions' category (column 3)
    selected_diseases_word = select_random_word_from_sheet(SHEET, 3)
    print("Randomly selected disease or condition word:", selected_diseases_word)
    
    hidden_diseases_word = create_hidden_word(selected_diseases_word)
    print("Hidden disease or condition word:", hidden_diseases_word)

    # Select a random word from the 'radiology' category (column 4)
    selected_radiology_word = select_random_word_from_sheet(SHEET, 4)
    print("Randomly selected radiology word:", selected_radiology_word)
    
    hidden_radiology_word = create_hidden_word(selected_radiology_word)
    print("Hidden radiology word:", hidden_radiology_word)


if __name__ == "__main__":
    main()

