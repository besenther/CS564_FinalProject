import requests
import time

session = requests.Session()

# Function to login to Pastebin
def login_to_pastebin(api_dev_key, username, password):
    data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password
    }

    response = session.post("https://pastebin.com/api/api_login.php", data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to create a paste on Pastebin
def create_paste(api_user_key, text, title="Untitled"):
    data = {
        'api_dev_key': api_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_expire_date': '10M',
        'api_paste_code': text,
        'api_paste_name': title
    }
    response = session.post("https://pastebin.com/api/api_post.php", data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Your Pastebin API Developer Key
api_key = "oI_hBDSnHFHmlCcY_TPqeLmV1GCCxu4E"
# Your Pastebin username and password
username = "frequency2612"
password = "cs564_project"

text_to_upload = None

# Login to Pastebin
api_user_key = login_to_pastebin(api_key, username, password)
if api_user_key:
    print("Successfully logged in to Pastebin.")
else:
    print("Failed to log in to Pastebin.")

# Example: Create a paste
if api_user_key:
    text_to_upload = input()
    paste_title = f"Command {time.ctime()}"
    paste_url = create_paste(api_user_key, text_to_upload, paste_title)
    if paste_url:
        print("Paste uploaded successfully. URL:", paste_url)
    else:
        print("Failed to upload paste.")

session.cookies.clear()