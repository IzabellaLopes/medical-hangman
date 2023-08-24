# Imports
import os
import time
import math
import gspread
from google.oauth2.service_account import Credentials
import random
from colorama import init, Fore, Style
import ascii_img

# Colorama
init()

BOLD = Style.BRIGHT
BOLD_GREEN = Style.BRIGHT + Fore.LIGHTGREEN_EX
GREEN = Fore.LIGHTGREEN_EX
BOLD_BLUE = Style.BRIGHT + Fore.LIGHTBLUE_EX
BOLD_MAGENTA = Style.BRIGHT + Fore.LIGHTMAGENTA_EX
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.LIGHTCYAN_EX
RESET = Style.RESET_ALL

# Constants
TERMINAL_WIDTH = 80
FEEDBACK_TIME = 1
HANGMAN_STAGES = 7
FORMATTED_LINE = YELLOW + "-+" * 40 + RESET
SCORE_RANGE = 5

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

# Open the 'highscores' Google Sheets
SCORE_SHEET = SHEET.worksheet('highscores')

# Game Variables
missed_letters = []
start_time = time.time()

# Utility Functions


def clear_terminal():
    """
    Clears the terminal.
    """

    os.system('cls' if os.name == 'nt' else "printf '\033c'")


def print_mid(*args):
    """
    Print the given text centered within a line of width 80 characters.
    """
    centered_texts = [f"{text:^{TERMINAL_WIDTH}}" for text in args]
    print(*centered_texts)


def print_header(ascii_image):
    """
    Prints the provided ASCII image as a header along with a formatted line.

    Args:
        ascii_image (str): The ASCII image to be printed as the header.
    """
    print(BOLD_GREEN + ascii_image + RESET)
    print(FORMATTED_LINE)


def bottom_input():
    """
    Prints the formatted line and waits for user input
    before returning to the menu.
    """
    print(FORMATTED_LINE)
    print()
    input(BOLD_GREEN
          + "Press ENTER to return to the menu..."
          + RESET)
    main_menu()

# Game Menu


def main_menu():
    """
    Displays the game menu and processes the user's choice.

    Returns:
        str: The user's choice (1, 2, or 3).
    """
    clear_terminal()

    print_header(ascii_img.WELCOME)
    print(BOLD + ascii_img.MENU_IMAGE + RESET)

    options = [
        "1. Play",
        "2. How to Play",
        "3. Highscores"
    ]

    print(BOLD_GREEN
          + " ".join(option.center(26) for option in options)
          + RESET)
    print(FORMATTED_LINE)

    choice = input(BOLD + "\nSelect an option: " + RESET)
    valid_choice = ["1", "2", "3"]

    if choice not in valid_choice:
        print(RED + "Oh no! Invalid choice. Please try again." + RESET)
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

    print_header(ascii_img.HOW_TO_PLAY)

    print_mid("The goal of Medical Hangman is to solve the hidden word.\n")
    print_mid("Choose category: BONE, ORGAN, DISEASE OR CONDITION, "
              "or RADIOLOGY\n")
    print_mid("Guess one letter at a time.\n")
    print_mid("If your guess is correct: "
              "the letter will appear in the word.\n")
    print_mid("M E D _ C A _  H A _ _ M A _\n")
    print_mid("If your guess is incorrect: "
              "the game stage will advance.\n")
    print_mid("After 7 wrong guesses: "
              "the game ends with a Hangman's fracture!\n")
    print_mid("M E D I C A L  H A N G M A N")

    bottom_input()

# Highscores


def highscores():
    """
    Displays the Top 5 highscores table.
    """

    score_data = SCORE_SHEET.get_all_values()
    # Sorts data by the second column (highscores)
    # in descending order.
    score_sorted = sorted(score_data, key=lambda x: int(x[1]), reverse=True)
    draw_table(score_sorted[:5])


def draw_table(scores):
    '''
    Draws score table with data from highscores().
    '''
    rank = 1
    rank_h = 'RANK'
    name_h = 'NAME'
    score_h = 'SCORE'

    header_format = f'{rank_h : ^6}{name_h : ^34}{score_h : ^10}'

    clear_terminal()

    print_header(ascii_img.HIGHSCORES)

    print()
    print_mid("Top 5 Highscores\n")
    print_mid(header_format)
    print_mid("-+" * 25)

    for line in scores:
        row = f'{rank : ^6}{line[0] :^34}{line[1] : ^10}'
        print_mid(row)
        print_mid('-' * 50)
        rank += 1

    print()

    bottom_input()


def calculate_score(start_time, end_time, game_word, player_lives):
    """
    Calculates the player's score based on game parameters.

    Parameters:
        start_time (float): The start time of the game.
        end_time (float): The end time of the game.
        game_word (str): The word used in the game.
        player_lives (int): The number of lives the player had.

    Returns:
        int: The calculated score.
    """
    seconds = math.floor(end_time - start_time)
    base_score = (len(game_word) * 500) + (player_lives * 1000)
    time_factor = max(1, 10 - seconds // 10)
    final_score = math.ceil(base_score / time_factor)
    return final_score


def save_score_to_sheet(name, score):
    """
    Saves the player's score to the 'highscores' worksheet
    in the Google Sheets.

    Parameters:
        name (str): The player's name.
        score (int): The player's score.
    """
    score_data = [name, str(score)]
    SCORE_SHEET.append_row(score_data)

# Function to take a validated player name input


def player_name():
    """
    Takes a validated player name input.

    Returns:
        str: The player's name.
    """
    while True:
        name = input(BOLD
                     + "\nEnter your player name: "
                     + RESET)

        if not name:
            print(RED
                  + "You must enter a name. Please try again."
                  + RESET)
            time.sleep(FEEDBACK_TIME)
        elif not name.replace(" ", "").isalpha():
            print(RED
                  + "Please enter a valid name containing only letters."
                  + RESET)
            time.sleep(FEEDBACK_TIME)
        else:
            return name

# Function to display categories and get player's choice


def choose_category(name, categories):
    """
    Display available categories and let the player choose one.
    """
    clear_terminal()

    print(FORMATTED_LINE)
    print()
    print_mid(f"Welcome {name}!")
    print()
    print_mid(" Prepare for a round of Medical Hangman. "
              "Select your medical word category now!\n")
    print(FORMATTED_LINE)
    time.sleep(FEEDBACK_TIME)
    print_header(ascii_img.CATEGORIES)
    print()

    for idx, category in enumerate(categories, start=1):
        formatted_category = (BOLD
                              + f"{idx})"
                              + CYAN
                              + f" {category[0]}"
                              + RESET)
        print(formatted_category)

        if idx < len(categories):
            print()

    category_choice = input(BOLD
                            + "\nEnter the category number: "
                            + RESET)
    return category_choice

# Function to select a random word from a specified column
# in a Google Sheets worksheet


def select_random_word_from_sheet(sheet, column_number):
    """
    Selects a random word from a specified column in a Google Sheets worksheet.

    Returns:
        str or None: Randomly selected word or None if the word list is empty.
    """
    WORD_SHEET = sheet.worksheet('word_list')

    # Retrieve the values from the specified column
    # in the 'word_list' worksheet
    words = WORD_SHEET.col_values(column_number)

    if not words:
        return None

    random_word = random.choice(words)
    return random_word

# Function to create a hidden word


def create_hidden_word(word):
    """
    Creates a formatted string of underscores to match
    the length of the input word.
    Adds spaces between letters for compound words,
    and regular spaces for spaces between words.
    """
    formatted_hidden_word = ' '.join(['_' if char != ' ' else ' '
                                      for char in word])
    return formatted_hidden_word

# Function to take a validated guess input from the user


def take_guess():
    """
    Takes a validated guess input from the user.
    """
    while True:
        guess = input(f"{BOLD_BLUE}\nTAKE A GUESS: {RESET}").upper()

        if len(guess) != 1 or not guess.isalpha():
            print(RED + "Invalid guess. Please enter a single letter." + RESET)
        else:
            return guess

# Function to check if the guessed letter is in the word
# and updates the hidden word


def check_guess(word, hidden_word, guess):
    """
    Checks if the guessed letter is in the word and
    updates the hidden word accordingly.
    """
    if guess in hidden_word or guess in missed_letters:
        return hidden_word, False

    correct_guess = False
    updated_hidden_word = list(hidden_word)

    for i in range(len(word)):
        if word[i] == guess:
            if (updated_hidden_word[i * 2] == '_' or
               updated_hidden_word[i * 2] == ' '):
                updated_hidden_word[i * 2] = guess
            correct_guess = True

    if not correct_guess and guess not in missed_letters:
        missed_letters.append(guess)

    return ''.join(updated_hidden_word), correct_guess

# Function to calculate the number of letters in a word without spaces


def calculate_word_length(word):
    """
    Calculate the number of letters in a word without spaces.
    """
    return len(word.replace(" ", ""))

# Function to update the game display


def update_game_display(hidden_word, missed_letters,
                        category_name, hangman_stage):
    """
    Update the game display based on the current game state.

    This function takes the hidden word, the list of missed letters,
    the category name, and the hangman stage as inputs and updates
    the visual representation of the game display accordingly.
    It prints the hangman image, hidden word, missed letters,
    and other relevant information.
    """
    clear_terminal()

    print_header(ascii_img.MEDICAL)

    if hangman_stage == 7:
        colored_hangman_stage = (RED
                                 + ascii_img.HANGMAN[hangman_stage]
                                 + RESET)
        print(colored_hangman_stage)
    else:
        print(ascii_img.HANGMAN[hangman_stage])

    print(FORMATTED_LINE)

    word_length = calculate_word_length(hidden_word)
    print_mid(f"This word has {word_length} letters\n")
    print(BOLD_GREEN
          + f"Hidden {category_name} word:", hidden_word
          + RESET)
    print()
    print(FORMATTED_LINE)
    print(BOLD_MAGENTA
          + "Missed letters: "
          + RESET
          + ", ".join(missed_letters)
          + RESET)

# Function to handle game over logic


def handle_game_over():
    """
    Handles the game over logic by prompting the player to play again,
    see highscores, or exit.
    """
    while True:
        print(BOLD_GREEN + "Would you like to play again?" + RESET)
        play_again = input(BOLD_GREEN
                           + "Please enter 'y' for yes, 'n' for no, "
                           "or 'h' to see the highscores: "
                           + RESET)
        if play_again.lower() == "y":
            clear_terminal()
            return True
        elif play_again.lower() == "n":
            print_mid("\nThank you for playing Medical Hangman!")
            time.sleep(FEEDBACK_TIME)
            return False
        elif play_again.lower() == "h":
            print(GREEN + "\nLoading highscores..." + RESET)
            time.sleep(FEEDBACK_TIME)
            highscores()
        else:
            print(RED
                  + "\nInvalid choice. Please enter 'y' to play again, "
                  "'n' to exit, or 'h' to see highscores."
                  + RESET)


def display_game_result(result, category_name,
                        selected_word, attempts, start_time, name):
    """
    Display the game result to the player based on whether they won or lost.

    Parameters:
        result (str): The result of the game, either "won" or "lost".
        category_name (str): The name of the chosen category.
        selected_word (str): The word that was selected for the game.
        attempts (int): The number of attempts the player had.
        start_time (float): The start time of the game.
        name (str): The name of the player.

    The function calculates and displays the player's score, final word,
    number of incorrect guesses, completion time, and provides feedback
    about the result of the game.
    """
    clear_terminal()

    if result == "won":
        print_header(ascii_img.WELL_DONE)
        colored_image = CYAN + ascii_img.SAFE + RESET
    else:
        print_header(ascii_img.GAME_OVER)
        colored_image = RED + ascii_img.HANGMAN[7] + RESET

    print(colored_image)
    print(FORMATTED_LINE)

    score = calculate_score(start_time, time.time(), selected_word, attempts)
    seconds = math.floor(time.time() - start_time)

    print(BOLD
          + f"You've {result} the hidden {category_name} word that was "
          f"{selected_word}."
          + RESET)
    print()
    print(BOLD_BLUE + f"FINAL SCORE: {score}")
    print("Factors considered for your score:")
    print(f"Word Length: {calculate_word_length(selected_word)} / "
          f"Number of Incorrect Guesses: {7 - attempts} / "
          f"Completion Time: {seconds}s")
    print("A higher score means you did well by guessing "
          "accurately and quickly.")
    print(Style.RESET_ALL)
    save_score_to_sheet(name, score)


def main():
    """
    Main function to run the Medical Hangman game
    with different word categories.

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
            name = player_name()

            while True:
                clear_terminal()

                category_choice = choose_category(name, categories)

                if category_choice.isdigit() and \
                        1 <= int(category_choice) <= len(categories):
                    category_name = categories[int(category_choice) - 1][0]
                    selected_word = select_random_word_from_sheet(
                        SHEET, int(category_choice))
                    hidden_word = create_hidden_word(selected_word)

                    missed_letters = []  # Reset missed letters for a new game

                    attempts = 7  # Maximum number of attempts
                    hangman_stage = 7 - attempts
                    start_time = time.time()

                    update_game_display(
                            hidden_word,
                            missed_letters,
                            category_name,
                            hangman_stage
                    )

                    while '_' in hidden_word and attempts > 0:
                        guess = take_guess()

                        if guess in missed_letters or guess in hidden_word:
                            print(YELLOW
                                  + "You've already guessed that letter."
                                  + RESET)
                        else:
                            hidden_word, correct_guess = check_guess(
                                selected_word, hidden_word, guess)

                            if correct_guess:
                                print(GREEN
                                      + "Correct guess!"
                                      + RESET)
                            else:
                                print(RED + "Incorrect guess!" + RESET)
                                # Check if the guess is not a duplicate
                                # or already revealed
                                if guess not in missed_letters and \
                                   guess not in hidden_word:
                                    missed_letters.append(guess)
                                    attempts -= 1

                        time.sleep(FEEDBACK_TIME)
                        hangman_stage = 7 - attempts
                        update_game_display(
                            hidden_word,
                            missed_letters,
                            category_name,
                            hangman_stage
                        )

                    # Check for game over conditions
                    if '_' not in hidden_word:
                        display_game_result("won",
                                            category_name,
                                            selected_word,
                                            attempts,
                                            start_time,
                                            name)
                    elif attempts == 0:
                        display_game_result("lost",
                                            category_name,
                                            selected_word,
                                            attempts,
                                            start_time,
                                            name)

                    if handle_game_over():
                        continue
                    else:
                        return
                else:
                    print(RED
                          + "Invalid category choice. "
                          "Please select a valid option."
                          + RESET)
                    time.sleep(FEEDBACK_TIME)

        elif choice == "2":
            how_to_play()
        elif choice == "3":
            highscores()


if __name__ == "__main__":
    main()
