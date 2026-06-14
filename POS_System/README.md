# ☕ Cafe POS System

A full-featured Point-of-Sale (POS) desktop application built with Python's Tkinter. Designed for small cafe/shop operations with complete transaction management.

## 🔑 Key Features

| Feature | Description |
| :--- | :--- |
| **User Authentication** | Login/Register system with credential validation |
| **Menu & Cart** | Dropdown item selector (Thai Tea, Milk Tea, Matcha, Drip Coffee) with quantity input and real-time cart display |
| **7% VAT Calculation** | Automatic tax calculation on every transaction |
| **Transaction Ledger** | Treeview table tracking Item, Status, Type, Timestamp, Notes, Staff, and Amount |
| **JSON Persistence** | Per-user data files (`{username}_pos_data.json`) for saving/loading transaction history |
| **CSV Export** | One-click export to `Sales_Report_YYYY-MM-DD.csv` for Excel compatibility |
| **Live Clock** | Real-time clock displayed in the bottom-right corner |
| **Staff Tracking** | Assign transactions to staff members (Ray, View, Gain) |

## 📁 Files

| File | Description |
| :--- | :--- |
| `GUI POS.py` | Main application — authentication, POS logic, and GUI |
| `UI.png` | Screenshot of the application interface |

## 🍵 Menu & Pricing

| Item | Price (THB) |
| :--- | ---: |
| Thai Tea | 45.00 |
| Milk Tea | 40.00 |
| Matcha | 55.00 |
| Drip Coffee | 60.00 |

## 🚀 How to Run

```bash
python "GUI POS.py"
```

**Test credentials:** `Test_user` / `0123`

## 📦 For Developers: Compiling to `.exe`

```bash
pip install pyinstaller
pyinstaller --onefile --windowed "GUI POS.py"
```

The executable `GUI POS.exe` will be generated in the `dist/` folder.

## ⚠️ Deployment Note

Please remove or replace all placeholder test accounts and credentials before deploying or sharing the application.
