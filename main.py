import json, requests, os
from keepalive import keep_alive

history = set()
webhook = os.environ['webhookkeygg']
token = os.environ['token']
source_channel_id = '1198622584229597295'
api_url = 'https://discord.com/api/v9'
headers = {
    'Authorization': token,
    'Content-Type': 'application/json'
}

def send(messages):
    payload = {
    'content': messages
}

    # Make a POST request to the webhook URL
    response = requests.post(webhook, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print('Failed to send message:', response.status_code, response.text)

def handle_message(message):
    global history
    id = message.get('id') 
    if id not in history:
        ping = '.script'
        content = message.get('content')
        attachments = message.get('attachments', [])
        is_plaintext_message = not attachments and content.strip()
        if is_plaintext_message:
            if ping in content:
                message_content = content
                send("<@&1179047887783612487>")
            else:
                message_content = content
        else:
            attachments = message.get('attachments', [])
            for attachment in attachments:
                message_content = attachment.get('url')
        send(message_content)
        history.add(id)
    else:
        print("I've alr sent it")

    # Function to get messages from the source channel
def get_messages():
    params = {
        'limit': 1  # Update to retrieve the last 5 messages
    }
    response = requests.get(
        f'{api_url}/channels/{source_channel_id}/messages',
        headers=headers,
        params=params
    )
    if response.status_code == 200:
        messages = response.json()
        for message in messages:
            handle_message(message)      
    else:
        print(f'Failed to fetch messages: {response.text}')
while True:
    get_messages()
