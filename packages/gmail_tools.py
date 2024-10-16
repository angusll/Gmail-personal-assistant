import base64
import re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
else:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

# Save the credentials for the next run
with open("token.json", "w") as token:
    token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)


def remove_urls(text: str) -> str:
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    text = text.replace("\r", "").replace("\n", "")
    return url_pattern.sub(r"", text)


def clean_email(email_payload: dict) -> dict:
    subject = ""
    body = ""
    try:
        header = email_payload["payload"]["headers"]
        for x in header:
            if x["name"] == "Subject":
                subject = x["value"]

        if "parts" in email_payload["payload"].keys():
            for p in email_payload["payload"]["parts"]:
                if p["mimeType"] in ["text/plain"]:
                    body = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
        return {"subject": subject, "body": remove_urls(body)}
    except Exception as e:
        raise e


def list_labels():
    response = service.users().labels().list(userId="me").execute()
    return {d["id"]: d["name"] for d in response["labels"]}


def get_email_ids_in_label(label_id: str, day_filter: str = "1") -> list:
    label_name = label_list.get(label_id)
    print(label_name)
    return (
        service.users()
        .messages()
        .list(userId="me", labelIds=label_id, q=f"newer_than:{day_filter}d")
        .execute()["messages"]
    )


def get_email(id: str) -> dict:
    return service.users().messages().get(id=id, userId="me", format="full").execute()
