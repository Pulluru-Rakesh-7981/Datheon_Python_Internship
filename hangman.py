"""Hangman - a console word guessing game.

How it works:
    1. A random word is chosen from 'words.txt'.
    2. The player guesses one letter at a time.
    3. Correct letters are revealed in the masked word (e.g. "_ A _ H E O N").
    4. Each NEW wrong letter adds a body part to the gallows.
    5. The player wins by revealing every letter, or loses after 6 mistakes.

Requirements:
    - Python 3
    - A file named 'words.txt' (one word per line) in the same folder.
"""

import random  # used for random.choice() to pick the secret word


# -----------------------------
# Hangman ASCII Art
# -----------------------------
# A list of 7 drawings. The index equals the number of mistakes made:
#   HANGMAN_STAGES[0] -> empty gallows (no mistakes)
#   HANGMAN_STAGES[6] -> complete hangman (game lost)
# Note: a single backslash is written as '\\' because '\' is an escape
# character inside normal Python strings.
HANGMAN_STAGES = [
    # Stage 0: empty gallows
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    # Stage 1: head
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    # Stage 2: body
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    # Stage 3: left arm
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    # Stage 4: right arm
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    # Stage 5: left leg
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    # Stage 6: right leg (game over)
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]


# Number of wrong guesses allowed before the player loses.
# It matches the last index of HANGMAN_STAGES (len(HANGMAN_STAGES) - 1).
MAX_MISTAKES = 6


# -----------------------------
# Load Words
# -----------------------------
def load_words(filename="words.txt"):
    """Load valid English words from a text file.

    Reads one word per line, converts it to lowercase, and keeps only
    entries made entirely of letters (no digits, spaces, or symbols).
    Exits the program with a helpful message if the file is missing.
    """
    try:
        # 'with' closes the file automatically, even if an error occurs.
        with open(filename, "r", encoding="utf-8") as file:
            # List comprehension: strip the newline, lowercase each line,
            # and skip anything that is not purely alphabetic (like blank lines).
            words = [
                word.strip().lower()
                for word in file
                if word.strip().isalpha()
            ]

        # Guard against an empty or unusable file.
        if not words:
            raise ValueError("The word list is empty.")

        return words

    except FileNotFoundError:
        # Friendly error instead of a long traceback.
        print("Error: words.txt was not found.")
        print("Please download the English word list and save it as 'words.txt'.")
        raise SystemExit  # stop the program cleanly


# -----------------------------
# Display Word
# -----------------------------
def display_word(secret_word, guessed_letters):
    """Return the word with unguessed letters hidden.

    Example: secret_word='python', guessed_letters={'p', 'o'}
             -> 'P _ _ _ O _'
    """
    # For every letter in the secret word:
    #   - show it (uppercase) if the player has guessed it
    #   - otherwise show an underscore
    # " ".join(...) puts a space between each character for readability.
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


# -----------------------------
# Display Game
# -----------------------------
def display_game(secret_word, guessed_letters, wrong_letters):
    """Display the current Hangman game state.

    Shows the gallows drawing, the masked word, the wrong guesses so far,
    and how many attempts are left.
    """
    # The number of wrong letters tells us which gallows picture to draw.
    mistakes = len(wrong_letters)

    print("\n" + "=" * 45)
    print(HANGMAN_STAGES[mistakes])  # pick the drawing that matches the mistakes
    print("=" * 45)

    print("Word:", display_word(secret_word, guessed_letters))

    if wrong_letters:
        # sorted() keeps wrong letters in alphabetical order.
        print("Wrong guesses:", " ".join(sorted(wrong_letters)).upper())
    else:
        print("Wrong guesses: None")

    print(f"Remaining attempts: {MAX_MISTAKES - mistakes}")
    print("=" * 45)


# -----------------------------
# Get Player Guess
# -----------------------------
def get_guess(guessed_letters):
    """Get and validate a single-letter guess.

    Keeps asking until the player enters one new alphabetic letter.
    Invalid or repeated input never costs the player an attempt.
    """
    while True:
        # strip() removes stray spaces; lower() makes 'A' and 'a' the same guess.
        guess = input("Enter a letter: ").strip().lower()

        # Must be exactly one character (rejects empty input and words).
        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue

        # Must be a letter (rejects digits and symbols).
        if not guess.isalpha():
            print("Please enter a valid alphabet letter.")
            continue

        # Must be new: repeats are rejected here, so they are never penalized.
        if guess in guessed_letters:
            print(f"You already guessed '{guess.upper()}'. Try another letter.")
            continue

        # All checks passed: this is a valid, new guess.
        return guess


# -----------------------------
# Victory Screen
# -----------------------------
def victory_screen(secret_word):
    """Show the 'you won' message and reveal the word."""
    print("\n" + "*" * 50)
    print("             🎉 YOU WON! 🎉")
    print("*" * 50)
    print(f"The word was: {secret_word.upper()}")
    print("Congratulations! You guessed the word!")
    print("*" * 50)


# -----------------------------
# Defeat Screen
# -----------------------------
def defeat_screen(secret_word):
    """Show the 'game over' message, the full hangman, and the secret word."""
    print("\n" + "*" * 50)
    print("             GAME OVER")
    print("*" * 50)
    print(HANGMAN_STAGES[MAX_MISTAKES])  # the final, complete drawing
    print(f"The correct word was: {secret_word.upper()}")
    print("Better luck next time!")
    print("*" * 50)


# -----------------------------
# Main Game
# -----------------------------
def play_game(words):
    """Run one complete Hangman game (from word selection to win/loss)."""
    # Step 3 of the approach: choose the secret word at random.
    secret_word = random.choice(words)

    # Two sets keep track of the player's guesses:
    #   guessed_letters -> EVERY letter tried (right or wrong); used to
    #                      reveal letters and to block duplicate guesses
    #   wrong_letters   -> only the incorrect letters; its size is the
    #                      number of mistakes
    # Sets are ideal here: fast lookups and no duplicate entries.
    guessed_letters = set()
    wrong_letters = set()

    # Welcome banner and rules.
    print("\n" + "=" * 50)
    print("          HANGMAN WORD GUESSING GAME")
    print("=" * 50)
    print("Guess the hidden word one letter at a time.")
    print(f"You have {MAX_MISTAKES} incorrect attempts.")
    print("=" * 50)

    # Main loop: runs until the player wins or loses (both use 'break').
    while True:
        # Show the current state at the start of every turn.
        display_game(secret_word, guessed_letters, wrong_letters)

        # Win check: every letter of the secret word has been guessed.
        if all(letter in guessed_letters for letter in secret_word):
            victory_screen(secret_word)
            break

        # Loss check: the player has used up all allowed mistakes.
        if len(wrong_letters) >= MAX_MISTAKES:
            defeat_screen(secret_word)
            break

        # Ask for a validated, never-before-used letter.
        guess = get_guess(guessed_letters)

        # Record the guess so it can't be entered again.
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"✅ Good guess! '{guess.upper()}' is in the word.")
        else:
            # Only wrong letters are added to wrong_letters, and each letter
            # can only be guessed once, so each mistake is penalized once.
            wrong_letters.add(guess)
            print(f"❌ Sorry! '{guess.upper()}' is not in the word.")


# -----------------------------
# Program Entry Point
# -----------------------------
def main():
    """Load the word list, then keep playing until the user quits."""
    words = load_words()  # load once; reuse for every round

    while True:
        play_game(words)

        # Anything other than 'y' ends the program.
        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()

        if play_again != "y":
            print("\nThanks for playing Hangman! 👋")
            break


# Run main() only when this file is executed directly,
# not when it is imported as a module.
if __name__ == "__main__":
    main()
