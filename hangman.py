import random


# -----------------------------
# Hangman ASCII Art
# -----------------------------
HANGMAN_STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
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


MAX_MISTAKES = 6


# -----------------------------
# Load Words
# -----------------------------
def load_words(filename="words.txt"):
    """Load valid English words from a text file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = [
                word.strip().lower()
                for word in file
                if word.strip().isalpha()
            ]

        if not words:
            raise ValueError("The word list is empty.")

        return words

    except FileNotFoundError:
        print("Error: words.txt was not found.")
        print("Please download the English word list and save it as 'words.txt'.")
        raise SystemExit


# -----------------------------
# Display Word
# -----------------------------
def display_word(secret_word, guessed_letters):
    """Return the word with unguessed letters hidden."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


# -----------------------------
# Display Game
# -----------------------------
def display_game(secret_word, guessed_letters, wrong_letters):
    """Display the current Hangman game state."""
    mistakes = len(wrong_letters)

    print("\n" + "=" * 45)
    print(HANGMAN_STAGES[mistakes])
    print("=" * 45)

    print("Word:", display_word(secret_word, guessed_letters))

    if wrong_letters:
        print("Wrong guesses:", " ".join(sorted(wrong_letters)).upper())
    else:
        print("Wrong guesses: None")

    print(f"Remaining attempts: {MAX_MISTAKES - mistakes}")
    print("=" * 45)


# -----------------------------
# Get Player Guess
# -----------------------------
def get_guess(guessed_letters):
    """Get and validate a single-letter guess."""
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue

        if not guess.isalpha():
            print("Please enter a valid alphabet letter.")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess.upper()}'. Try another letter.")
            continue

        return guess


# -----------------------------
# Victory Screen
# -----------------------------
def victory_screen(secret_word):
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
    print("\n" + "*" * 50)
    print("             GAME OVER")
    print("*" * 50)
    print(HANGMAN_STAGES[MAX_MISTAKES])
    print(f"The correct word was: {secret_word.upper()}")
    print("Better luck next time!")
    print("*" * 50)


# -----------------------------
# Main Game
# -----------------------------
def play_game(words):
    """Run one complete Hangman game."""
    secret_word = random.choice(words)

    guessed_letters = set()
    wrong_letters = set()

    print("\n" + "=" * 50)
    print("          HANGMAN WORD GUESSING GAME")
    print("=" * 50)
    print("Guess the hidden word one letter at a time.")
    print(f"You have {MAX_MISTAKES} incorrect attempts.")
    print("=" * 50)

    while True:
        display_game(secret_word, guessed_letters, wrong_letters)

        # Check if player has guessed the complete word
        if all(letter in guessed_letters for letter in secret_word):
            victory_screen(secret_word)
            break

        # Check if player has used all attempts
        if len(wrong_letters) >= MAX_MISTAKES:
            defeat_screen(secret_word)
            break

        guess = get_guess(guessed_letters)

        # Add guess to the set so duplicate guesses are prevented
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"✅ Good guess! '{guess.upper()}' is in the word.")
        else:
            # Because guessed_letters prevents duplicates,
            # each incorrect letter is penalized only once.
            wrong_letters.add(guess)
            print(f"❌ Sorry! '{guess.upper()}' is not in the word.")


# -----------------------------
# Program Entry Point
# -----------------------------
def main():
    words = load_words()

    while True:
        play_game(words)

        play_again = input("\nWould you like to play again? (y/n): ").strip().lower()

        if play_again != "y":
            print("\nThanks for playing Hangman! 👋")
            break


if __name__ == "__main__":
    main()
