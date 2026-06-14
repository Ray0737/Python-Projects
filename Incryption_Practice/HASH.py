import hashlib
import json
import os
import base64

STATIC_SALT = "a_secure_static_salt_for_this_demo"
DATA_FILE = "user_data.json"

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
PURPLE = "\033[35m"
BLUE    = '\033[34m'

def load_users():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
users = load_users()
username = None 

def hash_sha256(password: str) -> str:
    return hashlib.sha256((STATIC_SALT + password).encode('utf-8')).hexdigest()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def login():
    global username
    while True:
        print(f"{RED}ステップ 0: ユーザー名を解読してください (ヒント: ☕ あなたのインスタグラムのユーザー名):{RESET}")
        u_input = input("ユーザー名: ")
        print(f"{RED}ステップ 1: パスワードを解読してください (ヒント: 🍜 あなたのゲームの答えの一つ):{RESET}")
        p_input = input("パスワード: ")
        
        if u_input in users:
            stored_password = users[u_input].get("password")
            
            if stored_password == hash_sha256(p_input):
                username = u_input
                print(f"{GREEN}ログイン成功！{RESET}")
                
                choice = input("Go to backend? (press enter): ").lower()
                if choice == "001872737":
                    reader()
                    show_stored_messages()
                else:
                    show_stored_messages()
                break 
            else:
                print(f"{RED}アクセス拒否。パスワードが正しくありません。{RESET}\n")
        else:
            print(f"ユーザー '{u_input}' が見つかりません。新規登録します...")
            register(u_input)
            break

def register(new_user):
    password = input("パスワードを作成してください: ")
    users[new_user] = {
        "password": hash_sha256(password),
        "messages": [] 
    }
    save_users(users)
    print(f"{GREEN}Registered!{RESET}")
    global username
    username = new_user
    login()

def reader():
    msg = input("Enter msg to save: ")

    msg_bytes = msg.encode('utf-8')
    base64_bytes = base64.b64encode(msg_bytes)
    encoded_msg = base64_bytes.decode('utf-8')
    
    users[username]["messages"].append(encoded_msg)
    save_users(users)
    show_stored_messages()
    msg_return()

def show_stored_messages():
    print(f"\n--- 保存済みメッセージ一覧 ---")
    text = "" 
    if username in users:
        msg_list = users[username].get("messages", [])
        for i, m in enumerate(msg_list, 1):
            decoded_bytes = base64.b64decode(m)
            decoded_msg = decoded_bytes.decode('utf-8')
            text += f"{i}. {decoded_msg}\n"
 
        if not text:
            print("No messages found.")
        else:
            print(text.strip())
    print("---------------------------\n")
    msg_return()

def msg_return():
    msg2 = input("他に伝えたいことはありますか？ (ps. please send the JSON file back too) ")
    users[username]["messages"].append(msg2)
    save_users(users)
    print("Saved.")

if __name__ == '__main__':
    if input(f"{GREEN}プログラムを開始しますか？(y/n): {RESET}").lower() == 'y':
        clear_console()
        login()
        print(f"{BLUE}先輩、改めてありがとうございました。本当にいつも優しくしてくれて感謝しています。{RESET}")
        




