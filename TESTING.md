# Medical Hangman

![Heroku](documentation/home-page.png)


[Medical Hangman Live Page](https://medical-hangman-9035ef835c7a.herokuapp.com/)

---

## CONTENTS

- [Medical Hangman](#medical-hangman)
  - [CONTENTS](#contents)
  - [AUTOMATED TESTING](#automated-testing)
    - [CI Python Linter](#ci-python-linter)
    - [W3C Validator](#w3c-validator)
    - [Lighthouse](#lighthouse)
  - [MANUAL TESTING](#manual-testing)
    - [Testing User Stories](#testing-user-stories)
    - [Full Testing](#full-testing)

To ensure the accuracy, readability, and adherence to coding standards of the Medical Hangman Game, a rigorous validation process was conducted. By integrating the CI Python Linter into the development pipeline, I automated the assessment of my code for syntax errors, style inconsistencies, and other potential problems. This proactive approach aimed to identify and address issues early in development, minimizing the risk of bugs reaching the final product.

---

## AUTOMATED TESTING

### CI Python Linter

The Medical Hangman game has been thoroughly tested using the CI Python Linter, and the results indicate that the code is error-free and meets the required coding standards. The testing process included analyzing both the run.py and ascii_img.py files for any potential issues.

- **run.py**
![CI Linter - run.py](testing/pep8-run.png)

- **ascii_img.py**
![CI Linter - ascii.py](testing/pep8-ascii.png)

### W3C Validator

The validation for layout.html shows no errors when passing through the official [W3C validator](https://validator.w3.org/).

- **W3C Validator**
![W3C](testing/w3c.png)

### Lighthouse

I utilized Lighthouse, a tool available in the Chrome Developer Tools, to assess the performance, accessibility, best practices, and SEO aspects of the website.

- **Lighthouse**
![Lighthouse](testing/lighthouse.png)

---

## MANUAL TESTING

### Testing User Stories

`First Time Visitors`

| **GOALS** | **HOW ARE THEY ACHIEVED?**|
| :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| To gain a clear understanding of how the game is played and its connection to medical terminology. | Navigate to the "How to Play" section to receive step-by-step instructions on playing the Medical Hangman Game. You'll find a detailed breakdown of gameplay mechanics, such as choosing categories, making guesses, and progressing through the game. |
| The opportunity to explore and select from various available categories that align with your interests. | When you begin, you'll be prompted to select a category that intrigues you the most. The game provides options like "BONE," "ORGAN," "DISEASE OR CONDITION," and "RADIOLOGY." This variety ensures a tailored experience that aligns with your medical interests.|
| An engaging and interactive interface that guides you through the gameplay process. | The game boasts an intuitive and interactive interface, designed to lead you through each exciting round. The interface incorporates ASCII art and visual elements to enhance the experience and make the gameplay both informative and entertaining.|

`Returning Visitors`

| **GOALS** | **HOW ARE THEY ACHIEVED?**|
| :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Challenge Yourself: Engage in new game rounds to enhance scores across medical term categories. | Challenge: Select varied categories to test skills and adapt guessing strategies. |
| Enjoy and Learn: Continue enjoying game entertainment while reinforcing medical vocabulary. | Enjoyment: Immersive gameplay with engaging visuals enriches medical vocabulary.|
| Compare and Compete: Look forward to comparing high scores with past achievements and other players. | Comparison: Track high scores, measure progress, and compete for leaderboard supremacy.|

`Frequent Visitors`

| **GOALS** | **HOW ARE THEY ACHIEVED?**|
| :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Exploration and Mastery | Delve into diverse categories, aiming for better scores with each visit. |
| Leaderboard Recognition | Attain a spot on the highscores leaderboard, working to sustain or enhance rankings.|
| Social Engagement | Share accomplishments with peers, fostering friendly rivalry and camaraderie among players.|

---

### Full Testing

Comprehensive testing was conducted by family and friends, and no issues were reported during gameplay.

| Feature                                   | Expected Outcome                                                                                                                                                                                              | Testing Performed                                                                                                                                                                                                      | Result                                                                                                                                                                                                                                 | Pass/Fail |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| Game Menu | Display a menu with options to Play, How to Play, and Highscores| Tested each menu option for correct display and functionality| Menu options and navigation work as expected| Pass      |
| How to Play	| Show instructions on how to play the game| Selected the "How to Play" option and verified instructions were displayed | Instructions for gameplay are clear and accurate| Pass      |
| Highscores Display	| Display the top 5 highscores from the 'highscores' worksheet | Accessed the Highscores option and confirmed the display of top 5 highscores | Highscores are correctly fetched and displayed| Pass      |
Game Initialization	| Initialize game variables like missed letters and start time | Observed game variables at the start of each round | Game variables are properly initialized | Pass |
Guessing Mechanism | Allow players to input guesses and handle correct/incorrect guesses | Entered various guesses and monitored game response | Correctly handling player guesses and updating the game state | Pass |
Game Completion	| Handle game completion conditions (win/loss) and display results | Played games to both win and lose, checked displayed results | Game correctly identifies win/loss and displays corresponding results | Pass |
Score Calculation	| Calculate player scores based on word length, incorrect guesses, and completion time | Played games with different parameters and checked calculated scores | Score calculation based on specified parameters | Pass |
Save Highscores	| Save player's name and score to the 'highscores' worksheet | Played games, entered name, and checked if scores were saved | Player names and scores are properly saved in the 'highscores' worksheet | Pass |
Play Again	| Prompt player to play again or exit after a game ends | Finished games and selected different play again options | Play again options correctly navigate to desired actions | Pass |
Category Selection	| Allow players to select a category for gameplay | Chose different categories and checked if corresponding words were selected | Player can select categories and corresponding words are chosen | Pass |
Input Validation	| Validate user inputs for name, category selection, and guesses | Entered different inputs and verified if validation works | Input validation prevents invalid inputs | Pass |
Game Display Updates	| Update game display with hidden word, missed letters, and hangman stages | Played games, made guesses, and observed display updates | Display updates accurately reflect game state changes | Pass |
Game Over Handling	| Handle game over scenarios by allowing players to play again, view highscores, or exit | Finished games and selected different game over options | Game over options allow appropriate actions | Pass |