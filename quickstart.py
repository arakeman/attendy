import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-3aa3cf8e8cee.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ghA2W0tGvK0HSb55eER7UVBHwdjW5WUgcAaNYHmpy1E/')

worksheet = sh.get_worksheet(0)

values_list = worksheet.col_values(1)

print(values_list)
