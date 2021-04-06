import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import calendar
from gspread_formatting import *

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
mainSheet = client.open("MedMePi").sheet1

def Get_Current_Day_Time():
    current_date = datetime.today()
    ddate = str(current_date)[:10]
    sDate = ddate.split("-")
            
    currentDay = sDate[2]
    currentMonth = sDate[1]
    currentAll = currentDay + ' ' + currentMonth + ' 2020'
    currentWeekday = findDay(currentAll)
    
    currentTime = str(current_date)[11:16]
    currentHour = currentTime[:2]
    currentMin = currentTime[3:]
    return currentWeekday, currentTime, currentHour, currentMin

def findDay(date): 
    born = datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[born])

def Read_Database(currentDay):
    
    if currentDay == "Monday":
        colValues = mainSheet.col_values(2)
        colNumber = 2
    elif currentDay == "Tuesday":
        colValues = mainSheet.col_values(3)
        colNumber = 3
    elif currentDay == "Wednesday":
        colValues = mainSheet.col_values(4)
        colNumber = 4
    elif currentDay == "Thursday":
        colValues = mainSheet.col_values(5)
        colNumber = 5
    elif currentDay == "Friday":
        colValues = mainSheet.col_values(6)
        colNumber = 6
    elif currentDay == "Saturday":
        colValues = mainSheet.col_values(7)
        colNumber = 7
    elif currentDay == "Sunday":
        colValues = mainSheet.col_values(8)
        colNumber = 8
    return colValues, colNumber

def Check_Pill_Time(cDay, cHour, cMin, cPills):
    colValues, colNumber = Read_Database(cDay)
    
    amTime = colValues[1]
    locA = amTime.find(":")
    amHour = amTime[:locA]
    amMin = amTime[locA+1:]
    amTaken = colValues[3]
    
    
    pmTime = colValues[2]
    locP = pmTime.find(":")
    pmHour = pmTime[:locP]
    pmMin = pmTime[locP+1:]
    pmTaken = colValues[4]

    expectedBefore = colValues[5]
    expectedMiddle = colValues[6]
    expectedAfter = colValues[7]
    
    print(str(cDay) + " " + str(cHour) + ":" + str(cMin) + '\n')
    print("AM:  ", amHour, ':', amMin, "  | ", amTaken)
    print("PM: ", pmHour, ':', pmMin, "  | ", pmTaken)
    
    pillTime_flag = False
    
    if((int(cHour) == int(amHour)) and (int(cMin) == int(amMin))):
        print('\n' + "TAKE PILL")
        pillTime_flag = True
        if(int(cPills) == (int(expectedMiddle))):       
            mainSheet.update_cell(4, colNumber, "Yes")
            cellToUpdate = Get_Cell_Format(4, colNumber)
            Colour_Green(cellToUpdate)
            
            mainSheet.update_cell(5, colNumber, "No")
            cellToUpdate = Get_Cell_Format(5, colNumber)
            Colour_Red(cellToUpdate)
        return pillTime_flag, expectedMiddle
        
    elif((int(cHour) == int(pmHour)) and (int(cMin) == int(pmMin))):
        print('\n' + "TAKE PILL")
        pillTime_flag = True
        if(int(cPills) == int(expectedAfter)):      
            mainSheet.update_cell(4, colNumber, "Yes")
            cellToUpdate = Get_Cell_Format(4, colNumber)
            Colour_Green(cellToUpdate)
            
            mainSheet.update_cell(5, colNumber, "Yes")
            cellToUpdate = Get_Cell_Format(5, colNumber)
            Colour_Green(cellToUpdate)
        return pillTime_flag, expectedAfter



    if(int(cPills) == int(expectedBefore)):      
        mainSheet.update_cell(4, colNumber, "No")
        cellToUpdate = Get_Cell_Format(4, colNumber)
        Colour_Red(cellToUpdate)
        
        mainSheet.update_cell(5, colNumber, "No")
        cellToUpdate = Get_Cell_Format(5, colNumber)
        Colour_Red(cellToUpdate)
        
    elif(int(cPills) == (int(expectedMiddle))):       
        mainSheet.update_cell(4, colNumber, "Yes")
        cellToUpdate = Get_Cell_Format(4, colNumber)
        Colour_Green(cellToUpdate)
        
        mainSheet.update_cell(5, colNumber, "No")
        cellToUpdate = Get_Cell_Format(5, colNumber)
        Colour_Red(cellToUpdate)
               
    elif(int(cPills) == int(expectedAfter)):      
        mainSheet.update_cell(4, colNumber, "Yes")
        cellToUpdate = Get_Cell_Format(4, colNumber)
        Colour_Green(cellToUpdate)
        
        mainSheet.update_cell(5, colNumber, "Yes")
        cellToUpdate = Get_Cell_Format(5, colNumber)
        Colour_Green(cellToUpdate)
        

    if(int(cHour) < int(amHour) or (int(cHour) == int(amHour) and int(cMin) < int(amMin))):
        return pillTime_flag, expectedBefore
    
    elif(int(amHour) < int(cHour) < int(pmHour) or (int(cHour) == int(pmHour) and int(cMin) < int(pmMin)) or
     (int(cHour) == int(amHour) and int(cMin) > int(amMin))):
        return pillTime_flag, expectedMiddle

    elif((int(cHour) > int(pmHour)) or (int(cHour) == int(pmHour) and int(cMin) > int(pmMin))):
        return pillTime_flag, expectedAfter

    
def get_Email_Sizes():
    oldConf = mainSheet.cell (2,10).value
    oldReq = mainSheet.cell(2,11).value
    oldReset = mainSheet.cell(2,12).value
    return oldConf, oldReq, oldReset


def get_Set_Weekday_Column_Number(setDate):
    setWeekday = findDay(setDate)
    if setWeekday == "Monday":
        column = 2
    elif setWeekday == "Tuesday":
        column = 3
    elif setWeekday == "Wednesday":
        column = 4
    elif setWeekday == "Thursday":
        column = 5
    elif setWeekday == "Friday":
        column = 6
    elif setWeekday == "Saturday":
        column = 7
    elif setWeekday == "Sunday":
        column = 8 
    return column

def Get_Expected_Weight(pills):
    switcheroo = {
        0:0.0,
        1:1.2,
        2:2.4,
        3:3.6,
        4:4.8,
        5:6.0,
        6:7.2,
        7:8.4,
        8:9.6,
        9:10.8,
        10:12.0,
        11:13.4,
        12:14.6,
        13:15.8,
        14:17.0
    }
    return switcheroo.get(pills, "Invalid amount of pills")


def Update_Spreadsheet_Cell(row, column, value):
    mainSheet.update_cell(row, column, value)


def Reset_Pills_Taken():
    for row in range (4,6):
        for column in range (2,9):
            mainSheet.update_cell(row, column, "No")
            cellToUpdate = Get_Cell_Format(row, column)
            Colour_Red(cellToUpdate)


def Get_Cell_Format(row, column):
    col_switcher = {
        1:"A",
        2:"B",
        3:"C",
        4:"D",
        5:"E",
        6:"F",
        7:"G",
        8:"H"
    }
    colStr = col_switcher.get(column, "Invalid column")
    cell = colStr + str(row)
    return cell


def Colour_Green(updateCell):
    greenFormat = cellFormat(backgroundColor=color(0.0, 0.8, 0.0))
    format_cell_ranges(mainSheet, [(updateCell, greenFormat)])

def Colour_Red(updateCell):
    redFormat = cellFormat(backgroundColor=color(0.8, 0.0, 0.0))
    format_cell_ranges(mainSheet, [(updateCell, redFormat)])



    
    

