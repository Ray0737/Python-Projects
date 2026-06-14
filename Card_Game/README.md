# 🃏 Card Game

A terminal-based multiplayer card game for 2–6 players. Features a full 52-card deck with shuffling, dealing, sorted hands, and turn-based play.

## 🔑 Key Features

| Feature | Description |
| :--- | :--- |
| **Dynamic Player Count** | Supports 1–6 players, with automatic fallback to 4 if input is invalid |
| **Full 52-Card Deck** | Standard deck with suits (Clubs, Diamonds, Hearts, Spades) and ranks (2–A) |
| **Sorted Hands** | Cards are sorted by rank then suit for easy readability |
| **Turn-Based Play** | Players take turns selecting cards from their hand |
| **Multi-Card Plays** | Play multiple cards at once using dash notation (e.g., `2c-2h`) |
| **Privacy Mode** | Screen clears between player turns to hide each player's hand from others |
| **Win Detection** | First player to empty their hand wins |

## 📁 Files

| File | Description |
| :--- | :--- |
| `card.py` | Complete game logic — deck generation, shuffling, dealing, sorting, and turn loop |

## 🃏 Card Notation

Cards use a 2-character format: `[Rank][Suit]`
- **Ranks:** `2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A`
- **Suits:** `c` (Clubs), `d` (Diamonds), `h` (Hearts), `s` (Spades)
- **Examples:** `2c` = 2 of Clubs, `Ah` = Ace of Hearts, `Ts` = 10 of Spades

## 🚀 How to Run

```bash
python card.py
```

Follow the on-screen prompts to set player count and take turns.

## ⚠️ Deployment Note

This is a terminal-only application. It uses `os.system('cls')` / `os.system('clear')` for screen clearing between turns.
