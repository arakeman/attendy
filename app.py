import os
import sys
import json
import gspread 
from datetime import datetime, timedelta
from pytz import timezone
import time
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

pst_tz = timezone('US/Pacific')

studentToRow = {
"suhani abdullah 1" : 2,
"suhani abdullah 2" : 3,
"suhani abdullah 3" : 4,
"kendra abellaneda 1" : 5,
"kendra abellaneda 2" : 6,
"kendra abellaneda 3" : 7,
"sunny aggarwal 1" : 8,
"sunny aggarwal 2" : 9,
"sunny aggarwal 3" : 10,
"jimi ajayi 1" : 11,
"jimi ajayi 2" : 12,
"jimi ajayi 3" : 13,
"yvette ankunda 1" : 14,
"yvette ankunda 2" : 15,
"yvette ankunda 3" : 16,
"daksh bhatia 1" : 17,
"daksh bhatia 2" : 18,
"daksh bhatia 3" : 19,
"sabrina cherny 1" : 20,
"sabrina cherny 2" : 21,
"sabrina cherny 3" : 22,
"aditya chopra 1" : 23,
"aditya chopra 2" : 24,
"aditya chopra 3" : 25,
"natalie chow 1" : 26,
"natalie chow 2" : 27,
"natalie chow 3" : 28,
"jennifer dai 1" : 29,
"jennifer dai 2" : 30,
"jennifer dai 3" : 31,
"akshat das 1" : 32,
"akshat das 2" : 33,
"akshat das 3" : 34,
"karan dhillon 1" : 35,
"karan dhillon 2" : 36,
"karan dhillon 3" : 37,
"charles ding 1" : 38,
"charles ding 2" : 39,
"charles ding 3" : 40,
"anthony diprinzio 1" : 41,
"anthony diprinzio 2" : 42,
"anthony diprinzio 3" : 43,
"liam ehrlich 1" : 44,
"liam ehrlich 2" : 45,
"liam ehrlich 3" : 46,
"jon epstein 1" : 47,
"jon epstein 2" : 48,
"jon epstein 3" : 49,
"brennan fahselt 1" : 50,
"brennan fahselt 2" : 51,
"brennan fahselt 3" : 52,
"arnav gautam 1" : 53,
"arnav gautam 2" : 54,
"arnav gautam 3" : 55,
"mudit goyal 1" : 56,
"mudit goyal 2" : 57,
"mudit goyal 3" : 58,
"tyler heintz 1" : 59,
"tyler heintz 2" : 60,
"tyler heintz 3" : 61,
"adithya iyengar 1" : 62,
"adithya iyengar 2" : 63,
"adithya iyengar 3" : 64,
"brian jue 1" : 65,
"brian jue 2" : 66,
"brian jue 3" : 67,
"sung kang 1" : 68,
"sung kang 2" : 69,
"sung kang 3" : 70,
"parisa khorram 1" : 71,
"parisa khorram 2" : 72,
"parisa khorram 3" : 73,
"daniela kim 1" : 74,
"daniela kim 2" : 75,
"daniela kim 3" : 76,
"jennifer kirby 1" : 77,
"jennifer kirby 2" : 78,
"jennifer kirby 3" : 79,
"ronen ke 1" : 80,
"ronen ke 2" : 81,
"ronen ke 3" : 82,
"rishi kolady 1" : 83,
"rishi kolady 2" : 84,
"rishi kolady 3" : 85,
"nikhil krishnan 1" : 86,
"nikhil krishnan 2" : 87,
"nikhil krishnan 3" : 88,
"anushri kumar 1" : 89,
"anushri kumar 2" : 90,
"anushri kumar 3" : 91,
"katarina lee 1" : 92,
"katarina lee 2" : 93,
"katarina lee 3" : 94,
"federico li 1" : 95,
"federico li 2" : 96,
"federico li 3" : 97,
"therese liwanag 1" : 98,
"therese liwanag 2" : 99,
"therese liwanag 3" : 100,
"riley shore mangubat 1" : 101,
"riley shore mangubat 2" : 102,
"riley shore mangubat 3" : 103,
"sergey mann 1" : 104,
"sergey mann 2" : 105,
"sergey mann 3" : 106,
"daryus medora 1" : 107,
"daryus medora 2" : 108,
"daryus medora 3" : 109,
"brian mickle 1" : 110,
"brian mickle 2" : 111,
"brian mickle 3" : 112,
"brian nguyen 1" : 113,
"brian nguyen 2" : 114,
"brian nguyen 3" : 115,
"nelli petikyan 1" : 116,
"nelli petikyan 2" : 117,
"nelli petikyan 3" : 118,
"sanjay raavi 1" : 119,
"sanjay raavi 2" : 120,
"sanjay raavi 3" : 121,
"rohit rajkumar 1" : 122,
"rohit rajkumar 2" : 123,
"rohit rajkumar 3" : 124,
"alexander rakeman 1" : 125,
"alexander rakeman 2" : 126,
"alexander rakeman 3" : 127,
"evan sheng 1" : 128,
"evan sheng 2" : 129,
"evan sheng 3" : 130,
"robert spragg 1" : 131,
"robert spragg 2" : 132,
"robert spragg 3" : 133,
"chase sturgill 1" : 134,
"chase sturgill 2" : 135,
"chase sturgill 3" : 136,
"iris sun 1" : 137,
"iris sun 2" : 138,
"iris sun 3" : 139,
"keshav thvar 1" : 140,
"keshav thvar 2" : 141,
"keshav thvar 3" : 142,
"nicole tsai 1" : 143,
"nicole tsai 2" : 144,
"nicole tsai 3" : 145,
"jessie wang 1" : 146,
"jessie wang 2" : 147,
"jessie wang 3" : 148,
"william wang 1" : 149,
"william wang 2" : 150,
"william wang 3" : 151,
"thomas warloe 1" : 152,
"thomas warloe 2" : 153,
"thomas warloe 3" : 154,
"serena wu 1" : 155,
"serena wu 2" : 156,
"serena wu 3" : 157,
"kenny yoo 1" : 158,
"kenny yoo 2" : 159,
"kenny yoo 3" : 160,
"sunny zhang 1" : 161,
"sunny zhang 2" : 162,
"sunny zhang 3" : 163,
"zhe zhang 1" : 164,
"zhe zhang 2" : 165,
"zhe zhang 3" : 166
}

students = studentToRow.keys()

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
                    json = r.json()
                    first_name = json["first_name"]
                    last_name = json["last_name"]
                    
                    utc_dt = pytz.utc.localize(datetime.utcnow())
                    pst_dt = pst_tz.normalize(utc_dt.astimezone(pst_tz))
                    myTime = pst_dt.strftime("%H:%M:%S")
                    strTime = str(myTime).split(":")

                    message_keys = messaging_event["message"].keys()

                    if "text" in message_keys:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        approved = ["Alexander Rakeman", "Sunny Zhang", "Surina Gulati", "Janet Dong", "Stephen Torres"]
                        if (first_name + " " + last_name) in approved:
                            if message_text == "Start" or message_text == "start":
                                fifteen = pst_dt + timedelta(minutes = 15)
                                timesheet = timesh.get_worksheet(0)
                                row = timesheet.row_values(1)
                                startTime = datetime.strptime(row[0], "%m%d%Y %H:%M:%S")
                                counter = int(row[1])

                                if pst_dt < pst_tz.localize(startTime):
                                    send_message(sender_id, ("Hi " + first_name + ", attendance session " + str(counter) + " is already active."))
                                    return "ok", 200
                                else:
                                    if startTime.day == fifteen.day:
                                        counter = counter + 1
                                    else:
                                        counter = 1
                                    timesheet.insert_row([fifteen.strftime("%m%d%Y %H:%M:%S"), counter], 1)
                                    timesheet.delete_row(2)
                                    send_message(sender_id, ("Hi " + first_name + ", I have started taking attendance number " + str(counter) + ". This session will expire at " + fifteen.strftime("%I:%M:%S") + "."))
                                    return "ok", 200
                            else:
                                send_message(sender_id, ("Hi " + first_name + ", please send \'Start\' to begin an attendance session."))
                        else:
                            message_text = re.sub('\W+','', message_text)
                            send_message(sender_id, ("Sorry, I don't understand \'" + message_text + "\'"))
                            return "ok", 200
                    elif "attachments" in message_keys: #sending location
                        if "title" in messaging_event["message"]["attachments"][0].keys():
                            title = messaging_event["message"]["attachments"][0]["title"]
                            if "Location" in title and "Pinned" not in title:
                                coordinates =  messaging_event["message"]["attachments"][0]["payload"]["coordinates"]
                                lat = coordinates["lat"]
                                lon = coordinates["long"]
                                correctLocation = 0
                                
                                #37.875654, -122.259302 
                                #x: 37.874406 -> 37.876520 y: -122.260423 -> -122.258215
                                if lat >= 37.874406 and lat <= 37.876520 and lon >= -122.260423 and lon <= -122.258215:
                                    correctLocation = 1

                                correctStartTime = 0
                                timesheet = timesh.get_worksheet(0)
                                row = timesheet.row_values(1)
                                startTime = datetime.strptime(row[0], "%m%d%Y %H:%M:%S")

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
                                    decision = correctStartTime + correctLocation
                                    strD = "INCORRECT"
                                    if decision == 2:
                                        strD = "PRESENT"

                                    keyLookup = first_name + " " + last_name + " " + row[1]
                                    keyLookup = keyLookup.lower()
                                    if worksheet.row_count < 180:
                                        worksheet.add_rows(180)

                                    i = 0
                                    if keyLookup in students:
                                        print("Match found for " + keyLookup)
                                        cell_list = worksheet.range( ('A' + str(studentToRow[keyLookup]) + ':J' + str(studentToRow[keyLookup])) )
                                        values = [myDate, myTime, sender_id, keyLookup, title, lat, lon, correctStartTime, correctLocation, strD]
                                        for i in range(0, 10):
                                            cell_list[i].value = values[i]
                                        worksheet.update_cells(cell_list)
                                    else:
                                        print("No match found for " + keyLookup)
                                        worksheet.append_row([myDate, myTime, sender_id, keyLookup, title, lat, lon, correctStartTime, correctLocation, strD])
                                    if keyLookup in worksheet.col_values(4):
                                        if correctLocation:
                                            send_message(sender_id, ("Thanks " + first_name + ", I have processed your attendance number " + row[1] + "!"))
                                        else:
                                            send_message(sender_id, (first_name + ", I have processed your attendance number " + row[1] + ", however your location was incorrect. Please connect to WiFi to try and get a more accurate location, or make sure the TA knows your location will be incorrect."))

                                    else: 
                                        send_message(sender_id, ("I was unable to complete your request. Please try again in a few minutes."))
                                    return "ok", 200
                                else:
                                    send_message(sender_id, (first_name + ", attendance has not been taken yet."))
                                    return "ok", 200
                            else:
                                send_message(sender_id, (first_name + ", please send your current location."))
                                return "ok", 200

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
