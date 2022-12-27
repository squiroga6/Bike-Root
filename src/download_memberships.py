from __future__ import print_function

import pandas as pd
import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

import sys
sys.path.append(".")
from src.utils import clean_members_table

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
    ]


def download_memberships():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    file_id = "1UIiIBY83__1hE-pR3nvNJE0a-mDhPqyR3YMpSBo_gco"
    file_name = "bike_root_memberships"

    try:
        # get response from api
        service = build('drive', 'v3', credentials=creds)
        request = service.files().export_media(fileId=file_id,mimeType="text/csv")
        response = request.execute()

        # parse response into csv
        s=str(response,'utf-8')
        data = io.StringIO(s) 
        df=pd.read_csv(data, dtype={'Student Number':'str'})

        # clean and export
        df = clean_members_table(df)
        df.to_csv(f"data/{file_name}.csv",index=False)

        return df

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    download_memberships()