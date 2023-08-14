# Imports
import gspread
from google.oauth2.service_account import Credentials
import random
import os
import time

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

# Game Variables
missed_letters = []
FEEDBACK_TIME = 2

# Misc Functions
def clear_terminal():
    """
    Clears the terminal.
    """
    # From: https://stackoverflow.com/questions/2084508/clear-terminal-in-python

    os.system('cls' if os.name == 'nt' else 'clear')

# Game Menu
def main_menu():
    """
    Displays the game menu and processes the user's choice.
    """
    clear_terminal()
    
    print("WELCOME TO MEDICAL HANGMAN!")
    
    print("\nMenu:")
    print("1) Play")
    print("2) How to Play")
    print("3) Highscores")
    
    choice = input("Select an option: ")
    valid_choice = ["1", "2", "3"]
    
    if choice not in valid_choice:
        print("Oh no! Invalid choice. Please try again.")
        time.sleep(FEEDBACK_TIME)
        return main_menu()
    else:
        return choice

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

# Function to print lines of underscores
# From: https://www.youtube.com/watch?v=pFvSb7cb_Us
def printLines(word):
    for char in word:
        print("\u203E", end=" ")
    print()
    
# Function to create a hidden word
def create_hidden_word(word):
    """
    Creates a string of underscores to match the length of the input word.
    """
    hidden_word = ''.join(['_' if char != ' ' else ' ' for char in word])
    return hidden_word

# Function to take a validated guess input from the user
def take_guess():
    """
    Takes a validated guess input from the user. 
    """
    while True:
        guess = input("\nTake a guess: ").upper()
        
        if len(guess) != 1 or not guess.isalpha():
            print("\nInvalid guess. Please enter a single letter.\n")
        else:
            return guess
        
# Function to check if the guessed letter is in the word and update the hidden word
def check_guess(word, hidden_word, guess):
    """
    Checks if the guessed letter is in the word and updates the hidden word accordingly.
    """
    if guess in hidden_word or guess in missed_letters:
        return hidden_word, False    
    
    correct_guess = False
    updated_hidden_word = ''
    
    for i in range(len(word)):
        if word[i] == guess:
            updated_hidden_word += guess
            correct_guess = True
        else:
            updated_hidden_word += hidden_word[i]
            
    if not correct_guess and guess not in missed_letters:
        missed_letters.append(guess)
    
    return updated_hidden_word, correct_guess

# Function to calculate the number of letters in a word without spaces
def calculate_word_length(word):
    """
    Calculate the number of letters in a word without spaces.
    """
    return len(word.replace(" ", ""))

# Main Game logic
def start_game():
    """
    Main function to run the Medical Hangman game with different word categories.
    
    Categories:
        - Bones
        - Organs
        - Diseases or Conditions
        - Radiology
    """   
    categories = [
        ('BONE', 1),
        ('ORGAN', 2),
        ('DISEASE OR CONDITION', 3),
        ('RADIOLOGY', 4)
    ]

    while True:
        choice = main_menu()

        if choice == "1":
            name = input("\nEnter your name: ")
            
            clear_terminal()
            
            print(f"Welcome {name}! Let's play Medical Terms Hangman.\n")
            time.sleep(FEEDBACK_TIME)
            
            while True:
                game_over = False
                print("Choose the word list you want to play:\n")
                for idx, category in enumerate(categories, start=1):
                    print(f"{idx}) {category[0]}")
                category_choice = input("\nSelect a category: ")
                time.sleep(FEEDBACK_TIME)
                
                clear_terminal()

                if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
                    category_name = categories[int(category_choice) - 1][0]
                    selected_word = select_random_word_from_sheet(SHEET, int(category_choice))
                    hidden_word = create_hidden_word(selected_word)
                    
                    missed_letters = [] # Reset the missed letters for a new game round

                    word_length = calculate_word_length(selected_word)
                    print(f"This word has {word_length} letters.\n")
                    print(f"Hidden {category_name} word:", hidden_word)
                    
                    attempts = 7  # Maximum number of attempts
                    while '_' in hidden_word and attempts > 0:
                        guess = take_guess()
                        
                        if guess in missed_letters or guess in hidden_word:
                            print("\nYou've already guessed that letter. Try again with a different letter.\n")
                        else:
                            hidden_word, correct_guess = check_guess(selected_word, hidden_word, guess)
                        
                        if correct_guess:
                            print("\nCorrect guess!\n")
                        else:
                            print("\nIncorrect guess!\n")
                            # Check if the guess is not a duplicate or already revealed
                            if guess not in missed_letters and guess not in hidden_word:
                                missed_letters.append(guess)
                                attempts -= 1
                        
                        print(f"{attempts} attempts left.\n")
                        
                        if attempts < 7:
                            print("Missed letters: ", ", ".join(missed_letters))
                        
                        print('')
                        print(f"Hidden {category_name} word:", hidden_word)

                    # Check for game over conditions
                    if '_' not in hidden_word:
                        print(f"Congratulations, you've guessed the {category_name} word!\n")
                        game_over = True
                    elif attempts == 0:
                        print("\nSorry, you've run out of attempts. The word was:", selected_word)
                        game_over = True

                    if game_over:
                        play_again = input("Do you want to play again? (y/n): ")
                        if play_again.lower() == "y":
                            clear_terminal()
                            break
                        else:
                            print("Thank you for playing Medical Hangman!")
                            time.sleep(FEEDBACK_TIME)
                            return  # Exit the game
                else:
                    print("Invalid category choice. Please select a valid option.\n")
        
        elif choice == "2":
            print("How to Play: ...")  # Add instructions
        elif choice == "3":
            print("Highscores: ...")   # Add highscores
        
        
if __name__ == "__main__":
    start_game()