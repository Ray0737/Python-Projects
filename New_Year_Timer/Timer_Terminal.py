import datetime
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
while True:
    now = datetime.datetime.now()
    
    if now.day == 31 and now.month == 12:
        seconds_until_midnight = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
        
        # Loop until midnight
        while seconds_until_midnight > 0:
            now = datetime.datetime.now()
            seconds_until_midnight = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
            
            hours = int(seconds_until_midnight / 3600) % 24
            minutes = int(seconds_until_midnight / 60) % 60
            seconds = int(seconds_until_midnight % 60)
            
            clear_console()
            print(f"Current Time: {now.hour:02}:{now.minute:02}:{now.second:02} | "
                  f"Countdown: {hours:02}:{minutes:02}:{seconds:02}")
            
            time.sleep(1)
            
        clear_console()
        print("\033[91mHappy New Year 2026!\033[0m")
        break 
    else:
        # Regular clock mode for any other day
        clear_console()
        print(f"Current Time: {now.hour:02}:{now.minute:02}:{now.second:02}")
        print("Waiting for December 31st...")
        time.sleep(1)
