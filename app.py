import os
import sys
import json
import gspread 
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from oauth2client.service_account import ServiceAccountCredentials
import requests
import re
from flask import Flask, request

app = Flask(__name__)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-3aa3cf8e8cee.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13s-lbQkkcJfS-ENGFv3fVUDfsbIltJDkQ5F320fA1Wo/')

timesh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hAhmiyyryzhi139LAbusNCGusMd5k0E13OjPyVHTaeE/')


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    #get metadata
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    r = requests.get("https://graph.facebook.com/v2.6/" + sender_id + "?fields=first_name,last_name&access_token=" + os.environ["PAGE_ACCESS_TOKEN"])
                    
                    #add validation
                    first_name = r.json()["first_name"]
                    last_name = r.json()["last_name"]
                    
                    pst_tz = timezone('US/Pacific')
                    utc_dt = pytz.utc.localize(datetime.utcnow())
                    pst_dt = pst_tz.normalize(utc_dt.astimezone(pst_tz))
                    myTime = pst_dt.strftime("%H:%M:%S")
                    strTime = str(myTime).split(":")

                    if "text" in messaging_event["message"].keys():
                        message_text = messaging_event["message"]["text"]  # the message's text
                        approved = ["Alexander Rakeman", "Jennifer Dai", "Sunny Zhang", "Riley Mangubat", "Iris Sun"]
                        if (first_name + " " + last_name) in approved:
                            if message_text == "Start" or message_text == "start":
                                fifteen = pst_dt + timedelta(minutes = 15)
                                timesheet = timesh.get_worksheet(0)
                                row = timesheet.row_values(1)
                                startTime = datetime.strptime(row[0], "%m%d%Y %H:%M:%S")
                                counter = int(row[1])

                                if pst_dt < pst_tz.localize(startTime):
                                    send_message(sender_id, ("Hi " + first_name + ", attendance session " + str(counter) + " is already active."))
                                else:
                                    if startTime.day == fifteen.day:
                                        counter = counter + 1
                                    else:
                                        counter = 1
                                    timesheet.delete_row(1)
                                    timesheet.insert_row([fifteen.strftime("%m%d%Y %H:%M:%S"), counter], 1)
                                    send_message(sender_id, ("Hi " + first_name + ", I have started taking attendance number " + counter + ". This session will expire at " + fifteen.strftime("%I:%M:%S") + "."))
                            else:
                                send_message(sender_id, ("Hi " + first_name + ", please send \'Start\' to begin an attendance session."))
                        else:
                            message_text = re.sub('\W+','', message_text)
                            send_message(sender_id, ("Sorry, I don't understand \'" + message_text + "\'"))

                    elif "attachments" in messaging_event["message"].keys(): #sending location
                        if "title" in messaging_event["message"]["attachments"][0].keys():
                            title = messaging_event["message"]["attachments"][0]["title"]
                            if "Location" in title and "Pinned" not in title:
                                coordinates =  messaging_event["message"]["attachments"][0]["payload"]["coordinates"]
                                lat = coordinates["lat"]
                                lon = coordinates["long"]
                                correctLocation = 0
                                correctDate = pst_dt.weekday()
                                if correctDate == 6: 
                                    correctDate = 1
                                else:
                                    correctDate = 0
                                
                                if lat >= 37.875221 and lat <= 37.876219 and lon >= -122.259733 and -122.258767:
                                    correctLocation = 1

                                correctStartTime = 0
                                timesheet = timesh.get_worksheet(0)
                                row = timesheet.row_values(1)
                                startTime = datetime.strptime(row[0], "%m%d%Y %H:%M:%S")
                                print(pst_dt)
                                print(pst_tz.localize(startTime))

                                if pst_dt < pst_tz.localize(startTime):
                                    correctStartTime = 1
                                    myDate = pst_dt.strftime("%m/%d/%Y")
                                    addDate = pst_dt.strftime("%m%d%Y") 
                                    titles = [w.title for w in sh.worksheets()]
                                    worksheet = sh.get_worksheet(len(sh.worksheets())-1)
                                    if not addDate in titles:
                                        sh.add_worksheet(addDate, 14, 1)
                                        worksheet = sh.get_worksheet(len(sh.worksheets())-1)
                                    else:
                                        index = titles.index(addDate)
                                        worksheet = sh.get_worksheet(index)
                                    decision = correctDate + correctStartTime + correctLocation
                                    strD = "INCORRECT"
                                    if decision == 3:
                                        strD = "PRESENT"
                                    worksheet.insert_row([myDate, myTime, sender_id, first_name + " " + last_name + " " + row[1], title, lat, lon, correctStartTime, correctLocation, strD], len(worksheet.get_all_values()) + 1)
                                    send_message(sender_id, ("Thanks " + first_name + ", I have processed your attendance number " + row[1] + "!"))
                                else:
                                    send_message(sender_id, (first_name + ", attendance has not been taken yet."))
                            else:
                                send_message(sender_id, (first_name + ", please send your current location."))

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
