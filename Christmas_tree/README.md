# 🎄 Animated Christmas Tree

A terminal-based animated Christmas tree that uses ANSI color codes to create a twinkling, colorful ornament effect. Modified from an internet source.

## 🔑 Key Features

| Feature | Description |
| :--- | :--- |
| **ASCII Art Tree** | 7-row pine tree with a trunk, rendered in the terminal |
| **Random ANSI Colors** | Each `*` ornament is randomly assigned one of 6 colors (Red, Green, Yellow, Blue, Magenta, Cyan) on every frame |
| **Animation Loop** | The tree re-renders every 0.5 seconds, creating a twinkling light effect |
| **Graceful Exit** | Press `Ctrl+C` to cleanly stop the animation and reset terminal colors |

## 📁 Files

| File | Description |
| :--- | :--- |
| `Christmas Tree.py` | The complete animated tree script |

## 🚀 How to Run

```bash
python "Christmas Tree.py"
```

Press `Ctrl+C` to stop the animation.

## ⚠️ Deployment Note

This code outputs directly to the terminal using ANSI escape codes. It works best on terminals that support ANSI colors (most modern terminals on Windows, macOS, and Linux).
