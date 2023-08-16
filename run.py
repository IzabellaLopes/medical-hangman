# Imports
import gspread
from google.oauth2.service_account import Credentials
import random
import os
import time
import ascii_img
from colorama import init, Fore, Style

# Initialize Colorama
init()

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

# Create the line
line = "-+" * 40
formatted_line = Fore.YELLOW + line + Fore.RESET

# Misc Functions


def clear_terminal():
    """
    Clears the terminal.
    """
    # From:
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python

    os.system('cls' if os.name == 'nt' else 'clear')


def print_mid(*args):
    """
    Print the given text centered within a line of width 80 characters.
    """
    terminal_width = 80
    centered_texts = [f"{text:^{terminal_width}}" for text in args]
    print(*centered_texts)


def print_bold_light_green_text(text):
    """
    Prints the provided text in bold and light green using Colorama.
    """
    print(Style.BRIGHT+Fore.LIGHTGREEN_EX+text+Fore.RESET+Style.RESET_ALL)


def bottom_input():
    '''
    Prints the formatted line and waits for user input
    before returning to the menu.
    '''
    print(formatted_line)
    print()
    input('Press ENTER to return to the menu...')
    main_menu()

# Game Menu


def main_menu():
    """
    Displays the game menu and processes the user's choice.
    """
    clear_terminal()

    print_bold_light_green_text(ascii_img.WELCOME)
    print(formatted_line)
    print(ascii_img.MENU_IMAGE)
    print(formatted_line)
    print('')
    option_1 = "1. Play"
    option_2 = "2. How to Play"
    option_3 = "3. Highscores"
    print(f'{option_1 : <27}{option_2 : ^26}{option_3 : >27}')
    print('')
    print(formatted_line)
    print('')
    choice = input("Select an option: ")
    valid_choice = ["1", "2", "3"]

    if choice not in valid_choice:
        print(Fore.RED+"Oh no! Invalid choice. Please try again."+Fore.RESET)
        time.sleep(FEEDBACK_TIME)
        return main_menu()
    else:
        return choice

# How to play


def how_to_play():
    """
    Provides instructions on how to play Medical Hangman.
    """
    clear_terminal()

    print(formatted_line)
    print()
    print_mid("Be attentive to the instructions for playing Medical Hangman")
    print()
    print(formatted_line)

    print_bold_light_green_text(ascii_img.HOW_TO_PLAY)
    print()
    print_mid("The goal of Medical Hangman is to solve the hidden word.\n")
    print_mid("Choose category: bone, organ, disease, condition, or radiology")
    print_mid("_ _ _ _ _ _ _  _ _ _ _ _ _ _\n")
    print_mid("Guess one letter at a time.\n")
    print_mid("If your guess is correct:")
    print_mid("the letter will appear in the word.\n")
    print_mid("M E D _ C A _  H A _ _ M A _\n")
    print_mid("If your guess is incorrect:")
    print_mid("the game stage will advance.\n")
    print_mid("After 7 wrong guesses:")
    print_mid("the game ends with a Hangman fracture!\n")
    print_mid("M E D I C A L  H A N G M A N")
    print('\n')

    bottom_input()

# Function to take a validated player name input


def take_player_name():
    """
    Takes a validated player name input.
    """
    while True:
        name = input("\nEnter your player name: ")
        
        if not name:
            print(Fore.RED + "You must enter a name. Please try again." + Fore.RESET)
            time.sleep(FEEDBACK_TIME)
        elif not name.isalpha():
            print(Fore.RED+"Invalid name. Please enter a valid name containing only letters."+Fore.RESET)
            time.sleep(FEEDBACK_TIME)
        else:
            return name

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
        guess = input(Style.BRIGHT + Fore.LIGHTBLUE_EX + "\nTAKE A GUESS: " + Style.RESET_ALL + Fore.RESET).upper()
        
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

# Function to update the game display


def update_game_display(attempts, hidden_word, missed_letters, category_name):
    """
    Update the game display based on the current game state.

    This function takes the current number of attempts, the hidden word,
    the list of missed letters, and the category name as inputs and updates
    the visual representation of the game display accordingly. It prints
    the hangman image, hidden word, missed letters, and other relevant information.
    """
    clear_terminal()

    print_bold_light_green_text(ascii_img.MEDICAL)
    print(formatted_line)
    print(ascii_img.HANGMAN[7 - attempts])
    print(formatted_line)
    print('')

    word_length = calculate_word_length(hidden_word)
    print_mid(Fore.RED + f"This word has {word_length} letters\n" + Fore.RESET)
    print(Style.BRIGHT + f"Hidden {category_name} word:", hidden_word + Style.RESET_ALL)
    print('')
    print(formatted_line)
    print('')
    print_mid(f"{attempts} attempts left\n")
    print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "Missed letters: "+ Fore.RESET + Style.RESET_ALL, ", ".join(missed_letters))

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
            name = take_player_name()
            
            clear_terminal()
            
            print(formatted_line)
            print('')
            print_mid(f"Welcome {name}! Get ready to play Medical Hangman, where you'll guess medical terms.\n")
            print(formatted_line)
            time.sleep(FEEDBACK_TIME)
                     
            while True:
                game_over = False
                print_bold_light_green_text(ascii_img.CATEGORIES)
                print('')
                for idx, category in enumerate(categories, start=1):
                    formatted_category = Style.BRIGHT + f"{idx})" + Fore.LIGHTCYAN_EX + f" {category[0]}" + Fore.RESET + Style.RESET_ALL
                    print(formatted_category)
                    
                    if idx < len(categories):
                        print('')
                        
                category_choice = input("\nChoose a category by entering the corresponding number: ")
                time.sleep(FEEDBACK_TIME)
                
                clear_terminal()

                if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
                    category_name = categories[int(category_choice) - 1][0]
                    selected_word = select_random_word_from_sheet(SHEET, int(category_choice))
                    hidden_word = create_hidden_word(selected_word)

                    missed_letters = [] # Reset the missed letters for a new game round

                    attempts = 7  # Maximum number of attempts
             
                    print_bold_light_green_text(ascii_img.MEDICAL)
                    print(formatted_line)
                    print(ascii_img.HANGMAN[7 - attempts])
                    print(formatted_line)
                    print('')

                    word_length = calculate_word_length(hidden_word)
                    print_mid(Fore.RED + f"This word has {word_length} letters\n" + Fore.RESET)
                    print(Style.BRIGHT + f"Hidden {category_name} word:", hidden_word + Style.RESET_ALL)
                    print('')
                    print(formatted_line)
                    print('')
                    print_mid(f"{attempts} attempts left\n")
                    print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "Missed letters: "+ Fore.RESET + Style.RESET_ALL, ", ".join(missed_letters))
                                   
                    while '_' in hidden_word and attempts > 0:
                        guess = take_guess()
                        
                        if guess in missed_letters or guess in hidden_word:
                            print(Fore.LIGHTYELLOW_EX + "\nYou've already guessed that letter. Try again with a different letter." + Fore.RESET)
                        else:
                            hidden_word, correct_guess = check_guess(selected_word, hidden_word, guess)
                        
                            if correct_guess:
                                print(Fore.GREEN + "\nCorrect guess!" + Fore.RESET)
                            else:
                                print(Fore.RED + "\nIncorrect guess!" + Fore.RESET)
                                # Check if the guess is not a duplicate or already revealed
                                if guess not in missed_letters and guess not in hidden_word:
                                    missed_letters.append(guess)
                                    attempts -= 1
                        
                        time.sleep(FEEDBACK_TIME)
                                
                        update_game_display(attempts, hidden_word, missed_letters, category_name)

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
                    print(Fore.RED + "Invalid category choice. Please select a valid option." + Fore.RESET)
        
        elif choice == "2":
            how_to_play()
        elif choice == "3":
            print("Highscores: ...")   # Add highscores
        
         
if __name__ == "__main__":
    start_game()