import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import http.client
import datetime

def lambda_handler(event, context):

    credentialsObject = {
        "installed": {
        "client_id": "*************.apps.googleusercontent.com",
        "project_id": "quickstart-*************",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "************************",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }
    tokensObject = {
        "token": "*************************************************************************************************",
        "refresh_token": "**********************************************************************************************************",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "***********************************.apps.googleusercontent.com",
        "client_secret": "*********************",
        "scopes": ["https://www.googleapis.com/auth/spreadsheets.readonly"],
        "expiry": "2021-04-12T09:43:06.121345Z"
        }

    slackID = "slackID"
    rotaNametoSlackID = {
        "Wafa Zaidan": { slackID: "********"},
    }

    PERSONAL_ACCESS_TOKEN= "*****************************",      
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SAMPLE_SPREADSHEET_ID = "*****************************",
    SAMPLE_RANGE_NAME = 'New'

    def main():
        creds = None
        creds = Credentials.from_authorized_user_info(tokensObject, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsObject, SCOPES)
                creds = flow.run_local_server(port=0)

        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        return values


    def getNamesOnSuport(values):

        formattedDateToday = datetime.date.strftime(datetime.datetime.today(), "%d/%m/%Y")
        peopleOnSuport = ""
        for i in values:
            if i[0] == formattedDateToday:
                for name in rotaNametoSlackID:
                    if i[1] in name:
                        jsOnSupportSlackID = rotaNametoSlackID[name]["slackID"]
                        peopleOnSuport+= f"<@{jsOnSupportSlackID}>"
                        return peopleOnSuport
        

    def postMessageToSlack(message):
        slackConnection = http.client.HTTPSConnection("hooks.slack.com")
        headers = {"Content-Type": "application/json"}
        data = "{'text':'"+message+"'}"
        slackConnection.request(
            "POST",
            f"/services/{PERSONAL_ACCESS_TOKEN}",
            data,
            headers
        )

    sheetData = main()
    peopleOnSuport = getNamesOnSuport(sheetData)
    rotaMessage = f"On the support rota this week {peopleOnSuport} :superhero: Good luck! :fire: :bomb: " if peopleOnSuport else 'No one is on support this week!' 

    print(rotaMessage)
    postMessageToSlack(rotaMessage)

    return {
        'statusCode': 200,
        'body': "hi"
        }


lambda_handler('','')