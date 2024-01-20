from flask import Flask, request, jsonify, Response
# import requests
# from bs4 import BeautifulSoup
import sys
from ultils.api_stock import get_refresToken_cookiesFrame, get_stock
from ultils.process_data import process_excel
from datetime import datetime, date
# from api.upload_drive import upload_drive

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# import pathlib
# from flask_apscheduler import APScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.events import EVENT_JOB_MISSED
# from apscheduler.triggers.combining import AndTrigger
# from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.triggers.cron import CronTrigger

sys.path.insert(1, "ultils")

app = Flask(__name__)
app.config['SECRET_KEY'] = "dandan"

def remove_file_os(file_name):
  if os.path.exists(file_name):
    os.remove(file_name)

def create_excel_file(DF):
    excel_name = datetime.now().strftime("%d-%m-%Y")
    file_name = "stock-"+excel_name+".xlsx"
    DF.to_excel(file_name, engine="xlsxwriter",engine_kwargs={'options': {'strings_to_numbers': True}} )
    # upload_drive(["stock-"+excel_name+".xlsx"])
    main_pro(file_name)
    remove_file_os(file_name)


def call_stock(): 
  token_cookie = get_refresToken_cookiesFrame()
  data = get_stock(token_cookie["requestToken"], token_cookie["cookie"])
  DF_Stock = process_excel(data)
  create_excel_file(DF_Stock)
  return DF_Stock

@app.route("/")
def home():
    call_stock()
    return "Data"

# If modifying these scopes, delete the file token.json.
SCOPES = [
  #  "https://www.googleapis.com/auth/drive.metadata.readonly"
   "https://www.googleapis.com/auth/drive"
   ]


def main_pro(file_name):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    folder_id = "1eJf3NV5DEBx0Xkvh2tOgsZz8QOh6qeal"
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(
        file_name, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", resumable=True
    )

    response = (
          service.files()
          .list(
              q="'{}' in parents and trashed=false".format(folder_id)
          )
          .execute()
      )
    print("get data stock", response.get("files", []))
    
    for file in response.get("files", []):
       if file["name"] == file_name:
          service.files().update(fileId=file["id"], body={'trashed': True}).execute()


    # Call the Drive v3 API
    results = (
        service.files()
        # .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    

    print(f'File ID: "{results.get("id")}".')

    
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


def my_job(text):
    call_stock()
    dt = datetime.now().replace(hour=17, minute=41, second=00, microsecond=00)
    print(text, str(datetime.now()))


if __name__ == "__main__":
    app.run(debug=True)