import tkinter as tk
from datetime import datetime

class NewYearTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("New Year Countdown")
        self.root.geometry("800x300")
        self.root.configure(bg='black')

        self.time_label = tk.Label(root, font=('Arial', 48), fg='white', bg='black')
        self.time_label.pack(expand=True)

        self.status_label = tk.Label(root, font=('Arial', 18), fg='white', bg='black')
        self.status_label.pack(expand=True)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        if now.month == 12 and now.day == 31:
            # seconds_left = 3600 - (now.minute * 60 + now.second)
            seconds_left = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
            
            if seconds_left <= 0:
                self.time_label.config(text="00:00:00", fg='red')
                self.status_label.config(text="HAPPY NEW YEAR!", fg='yellow')
            else:
                hours = seconds_left // 3600
                minutes = (seconds_left % 3600) // 60
                seconds = seconds_left % 60
                current_time = now.strftime("%H:%M:%S")
                self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02} | {current_time}", fg='orange')
                self.status_label.config(text="Time left | Current Time\n\nGMT +7 | BKK, TH")


        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = NewYearTimer(root)
    root.mainloop()
