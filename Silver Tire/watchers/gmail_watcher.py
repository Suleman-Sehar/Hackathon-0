import time
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    token_path = Path('token.json')
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())           # ← this line needs 'Request' import
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    print("Gmail Watcher Ready - Checking every 2 min...")

    while True:
        try:
            results = service.users().messages().list(userId='me', q='is:unread is:important').execute()
            messages = results.get('messages', [])
            for msg in messages:
                full = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = {h['name']: h['value'] for h in full['payload']['headers']}
                content = f"From: {headers.get('From')}\nSubject: {headers.get('Subject')}\nSnippet: {full.get('snippet')}"
                Path('Needs_Action').mkdir(exist_ok=True)
                (Path('Needs_Action') / f"GMAIL_{msg['id']}.md").write_text(content)
                print(f"New Gmail saved: GMAIL_{msg['id']}.md")
        except Exception as e:
            print(e)
        time.sleep(120)

if __name__ == "__main__":
    main()
