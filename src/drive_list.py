from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
    ]


def drive_list(file_name = None):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
    # If there are no (valid) credentials available, let the user log in.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        results = service.files().list().execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return
        if file_name == '':
            print('\n Printing all Files:')
            for item in items:
                print(f"Name: {item['name']}")
                print(f"ID: {item['id']}")
                print(f"mimeType : {item['mimeType']}\n")
        else:       
            print(f"\nGetting infor for file: {file_name}")
            for item in items:
                if item['name'] == file_name:
                    print(f"Name: {item['name']}")
                    print(f"ID: {item['id']}")
                    print(f"mimeType : {item['mimeType']}\n")       

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    file_name = input("File name: ")
    drive_list(file_name)