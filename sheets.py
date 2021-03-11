import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def gSheetsConnect(fileName):
    #Connects to the cloud with credentials file (creds.json)
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    #Pulls up the specific sheet and stores data in sheet variable
    sheet = client.open(fileName).sheet1
    return sheet

def append(sheet,values):
    data = sheet.get_all_records()
    sheet.insert_row([len(data)+1,str(datetime.datetime.now())[:22]] + values, len(data)+2)

def getTime(sheet):
    col = sheet.col_values(2)
    return(col[1:])

def getData1(sheet):
    col = sheet.col_values(3)
    return(col[1:])


if __name__ == "__main__":
    sheet = gSheetsConnect("cloudNoiseData")
    #append(sheet,["22", "22"])
    #print(getTime(sheet))
    print(getData1(sheet))
"""
#Get all data in a sheet
data = sheet.get_all_records()
#Get all data in row X in a sheet
row = sheet.row_values(1)
#Get all data in column X in a sheet
col = sheet.col_values(1)
#Get data in a specific cell (1,1)
cell = sheet.cell(1,1).value
"""
