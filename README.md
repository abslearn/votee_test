# votee_test

# Wordle API Solver

This project is an **automated Wordle solver** that interacts with the [Wordle API](https://wordle.votee.dev:8000/redoc) to efficiently solve Wordle-like puzzles.  
It uses feedback from each guess to filter possible words and maximize solving speed.

## Features

- **Automated guessing** using the `/random` API endpoint.
- **Efficient filtering** of possible words based on feedback.
- **Consistent puzzle solving** using a fixed random seed.
- Uses a local `words_alpha.txt` file as the word list (one word per line, 5-letter words only).

## Requirements

- Python 3.7+
- `requests` library

## Setup

1. **Clone or download this repository.**
2. **Download `words_alpha.txt`** (a list of English words, e.g. from [dwyl/english-words](https://github.com/dwyl/english-words)) and place it in the same directory as the script.
3. **Install dependencies:**
   ```bash
   pip install requests
   ```

## Usage

Run the solver script:
```bash
python wordle_solver.py
```
- The script will print each guess and the feedback from the API.
- It will stop when the correct word is found.

## How It Works

- The script loads all 5-letter words from `words_alpha.txt`.
- It selects a random puzzle by generating a random seed and uses this seed for all API requests, ensuring the same target word is used for each guess.
- After each guess, it filters the word list based on the API's feedback:
  - **correct**: Letter is in the correct position.
  - **present**: Letter is in the word but not in this position.
  - **absent**: Letter is not in the word (with care for duplicate letters).
- The next guess is chosen from the remaining possible words.

## Example Output

```
Using seed: 123456789
Attempt 1: raise -> ['absent', 'present', 'absent', 'absent', 'correct']
Attempt 2: table -> ['correct', 'absent', 'absent', 'present', 'correct']
...
Solved in 4 attempts! The word was: table
```

## API Reference

This project uses the `/random` endpoint of the [Wordle API](https://wordle.votee.dev:8000/redoc):

- **Endpoint:** `GET /random`
- **Parameters:**
  - `guess` (string, required): The guessed word.
  - `size` (integer, optional): Word length (default: 5).
  - `seed` (integer, optional): The puzzle seed. Use the same seed for all guesses to solve the same puzzle.
- **Response:** Array of objects, one per letter, with:
  - `slot`: Position (0-based)
  - `guess`: The guessed letter
  - `result`: `"correct"`, `"present"`, or `"absent"`

## Customization

- To use a different starting word, edit the `starter` variable in the script.
- To solve the daily puzzle instead, adapt the script to use the `/daily` endpoint.

## License

MIT

---

**Happy solving!**  
Let me know if you need more advanced strategies or want to extend this project.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/4919392/3ab00c71-302b-4b5d-9e42-5f9281007baa/openapi.json

---
Answer from Perplexity: pplx.ai/share
