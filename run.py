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
    hidden_word = ' '.join(['_' if char != ' ' else ' ' for char in word])
    return hidden_word

def take_guess():
    """
    Takes a validated guess input from the user. 
    """
    while True:
        guess = input("Take a guess: ").upper()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid guess. Please enter a single letter.")
        else:
            return guess
        
def check_guess(word, hidden_word, guess):
    """
    Checks if the guessed letter is in the word and updates the hidden word accordingly.
    """
    correct_guess = False
    updated_hidden_word = ''
    
    for i in range(len(word)):
        if word[i] == guess:
            updated_hidden_word += guess
            correct_guess = True
        else:
            updated_hidden_word += hidden_word[i]
    
    return updated_hidden_word, correct_guess

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
    hidden_bone_word = create_hidden_word(selected_bone_word)
    
    print("Hidden bone word:", hidden_bone_word)
    
    while '_' in hidden_bone_word:
        guess = take_guess()
        hidden_bone_word, correct_guess = check_guess(selected_bone_word, hidden_bone_word, guess)
        
        if correct_guess:
            print("Correct guess!")
        else:
            print("Incorrect guess!")
        
        print("Hidden bone word:", hidden_bone_word)
    
    print("Congratulations, you've guessed the bone word!")

if __name__ == "__main__":
    main()

