import requests
import random
import os

API_URL = "https://wordle.votee.dev:8000/random"
WORD_FILE = "words_alpha.txt"
WORD_LENGTH = 5

def load_word_list(filename, word_length):
    with open(filename, "r") as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == word_length and line.strip().isalpha()]
    if not words:
        raise ValueError(f"No {word_length}-letter words found in {filename}")
    return words

def guess_word(word, seed, size=WORD_LENGTH):
    params = {"guess": word, "size": size, "seed": seed}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def is_correct(result):
    return all(slot['result'] == 'correct' for slot in result)

def filter_word_list(word_list, guess, feedback):
    new_list = []
    for word in word_list:
        match = True
        # First pass: check 'correct'
        for i, slot in enumerate(feedback):
            if slot['result'] == 'correct':
                if word[i] != guess[i]:
                    match = False
                    break
        if not match:
            continue
        # Second pass: check 'present' and 'absent'
        for i, slot in enumerate(feedback):
            if slot['result'] == 'present':
                if guess[i] not in word or word[i] == guess[i]:
                    match = False
                    break
            elif slot['result'] == 'absent':
                # For 'absent', ensure the letter is not present unless already confirmed by 'correct' or 'present'
                # Count how many times guess[i] is marked present/correct
                num_in_guess = sum(1 for s in feedback if s['guess'] == guess[i] and s['result'] in ('correct', 'present'))
                num_in_word = word.count(guess[i])
                if num_in_word > num_in_guess:
                    match = False
                    break
        if match:
            new_list.append(word)
    return new_list

def play_random_wordle():
    word_list = load_word_list(WORD_FILE, WORD_LENGTH)
    attempts = 0
    used_words = set()
    seed = random.randint(0, 1000000000)  # Use a random seed for this puzzle

    print(f"Using seed: {seed}")

    # Optionally, start with a strong opener
    starter = "raise" if "raise" in word_list else random.choice(word_list)
    guess = starter

    while True:
        attempts += 1
        used_words.add(guess)
        result = guess_word(guess, seed)
        print(f"Attempt {attempts}: {guess} -> {[slot['result'] for slot in result]}")

        if is_correct(result):
            print(f"Solved in {attempts} attempts! The word was: {guess}")
            break

        # Filter possible words based on result
        word_list = filter_word_list(word_list, guess, result)
        if not word_list:
            print("No possible words left! Exiting.")
            break
        # Pick next guess (could be random, or implement a strategy)
        guess = random.choice([w for w in word_list if w not in used_words])

if __name__ == "__main__":
    if not os.path.exists(WORD_FILE):
        print(f"Error: {WORD_FILE} not found in the current directory.")
    else:
        play_random_wordle()
