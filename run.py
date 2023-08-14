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

# Authorize Google Sheets API using service account credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the 'medical_hangman' Google Sheets
SHEET = GSPREAD_CLIENT.open('medical_hangman')

# Function to select a random word from a specified column in a Google Sheets worksheet
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

# Function to create a hidden word with underscores
def create_hidden_word(word):
    """
    Creates a string of underscores to match the length of the input word.
    """
    hidden_word = ' '.join([' _ ' if char != ' ' else ' ' for char in word])
    return hidden_word

# Function to take a validated guess input from the user
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
        
# Function to check if the guessed letter is in the word and update the hidden word
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

# Game Menu and main function
def main():
    """
    Main function to run the Medical Hangman game with different word categories.
    
    Categories:
        - Bones
        - Organs
        - Diseases or Conditions
        - Radiology
    """
    print("Welcome to Medical Hangman!")
    
    categories = [
        ('Bones', 1),
        ('Organs', 2),
        ('Diseases or Conditions', 3),
        ('Radiology', 4)
    ]

    while True:
        print("\nMenu:")
        print("1) Play")
        print("2) How to Play")
        print("3) Highscores")
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter your name: ")
            print(f"Welcome {name}! Let's play Medical Terms Hangman.")

            while True:
                print("\nChoose the word list you want to play:")
                print("1) Bones")
                print("2) Organs")
                print("3) Diseases or Conditions")
                print("4) Radiology")
                category_choice = input("Select a category: ")

                if category_choice in ["1", "2", "3", "4"]:
                    category_name = categories[int(category_choice) - 1][0]
                    selected_word = select_random_word_from_sheet(SHEET, int(category_choice))
                    hidden_word = create_hidden_word(selected_word)

                    print(f"Hidden {category_name} word:", hidden_word)
                    
                    attempts = 7  # Maximum number of attempts
                    while '_' in hidden_word and attempts > 0:
                        guess = take_guess()
                        hidden_word, correct_guess = check_guess(selected_word, hidden_word, guess)

                        if correct_guess:
                            print("Correct guess!")
                        else:
                            print("Incorrect guess!")
                            attempts -= 1
                            print(f"{attempts} attempts left.")

                        print(f"Hidden {category_name} word:", hidden_word)

                    if '_' in hidden_word:
                        print("Sorry, you've run out of attempts. The word was:", selected_word)
                    else:
                        print(f"Congratulations, you've guessed the {category_name} word!")
                    break
                else:
                    print("Invalid category choice. Please select a valid option.")
        elif choice == "2":
            print("How to Play: ...")  # Add instructions
        elif choice == "3":
            print("Highscores: ...")   # Add highscores
        else:
            print("Invalid option. Please select a valid option.")
        
if __name__ == "__main__":
    main()