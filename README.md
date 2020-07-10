# MemPage
##### Simple website for posting images with comment sections and email password recovery

## Setup

Set variable `DATABASES` in `mempage/settings.py`

Class `GmailService` in `userapp/emails/myemail.py` is used for sending emails. You can either put your OAuth Client ID in `userapp/emails/credentials.json` or implement your own `GmailService.send_mail` method to make it work

Gmail API setup - https://developers.google.com/webmaster-tools/search-console-api-original/v3/quickstart/quickstart-python?authuser=3 