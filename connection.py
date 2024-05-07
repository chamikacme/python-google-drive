from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

# Replace with your downloaded JSON key file path
credentials_file = 'mineral-music-336402-85521bbea9ba.json'

# Define the scopes required by your application
scopes = ['https://www.googleapis.com/auth/drive']

# Use the downloaded credentials to authenticate
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
http = credentials.authorize(Http())

# Build the Drive API service object
service = build('drive', 'v3', http=http)
