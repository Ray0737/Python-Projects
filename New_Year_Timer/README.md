# 🎆 New Year Countdown Timer

A New Year's Eve countdown timer available in two versions: a **Tkinter GUI** and a **terminal-based** display. Both are configured for GMT+7 (Bangkok, Thailand).

## 🔑 Key Features

| Feature | Description |
| :--- | :--- |
| **Dual Versions** | GUI window (`Timer.py`) and terminal (`Timer_Terminal.py`) |
| **Auto-detect Dec 31** | Automatically activates the countdown when the system date is December 31st; otherwise shows a regular clock |
| **Live Display** | Shows both the remaining time (`HH:MM:SS`) and the current time side-by-side |
| **Midnight Trigger** | Displays "HAPPY NEW YEAR!" in red/yellow when the countdown reaches zero |
| **Timezone** | Hardcoded for GMT+7 (Bangkok, TH) |

## 📁 Files

| File | Description |
| :--- | :--- |
| `Timer.py` | GUI version using Tkinter with a dark theme (800×300 window) |
| `Timer_Terminal.py` | Terminal version using `os.system('cls')` for a clean, updating display |

## 🚀 How to Run

```bash
# GUI Version
python Timer.py

# Terminal Version
python Timer_Terminal.py
```

## 📦 Compiling to `.exe`

```bash
pip install pyinstaller
pyinstaller --onefile --windowed "Timer.py"
```

The executable `Timer.exe` will be generated in the `dist/` folder.

## ⚠️ Deployment Note

Launch the application before 23:00 on December 31st to ensure the countdown is active and visible for the full final hour.
