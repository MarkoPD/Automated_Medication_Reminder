import Init_Gspread as gspread
import Init_Scale as scale
import Init_Email as mail
import Init_Arduino as arduino
import time

counter = 5
activeCounter = 0
activated_Flag = False

while True:
    counter = counter+1
    activeCounter = activeCounter+1
    if(counter % 6 == 0):
        print("Reading Mail . . .")
        setDay, setMonth, setHour, setMin, confSize = mail.Read_Config_Email()
        requestSize = mail.Read_Request_Email()
        resetSize = mail.Read_Reset_Email()
        print("Completed" + '\n')
        counter = 0
    else:       
        cDay, cTime, cHour, cMin = gspread.Get_Current_Day_Time()
        colValues, colNumber = gspread.Read_Database(cDay)
        currentPills, pillWeight = scale.get_Number_Of_Pills()
        pill_Flag, expectedPills = gspread.Check_Pill_Time(cDay, cHour, cMin, currentPills)
        expectedWeight = gspread.Get_Expected_Weight(int(expectedPills))

        currentStr = "Currently : " + str(currentPills) + " pills - " + str(pillWeight) + "g"
        expectedStr = "Expected  : " + str(expectedPills) + " pills - " + str(expectedWeight) + "g"
        Pill_Outcome = ('\n' + expectedStr + '\n' + currentStr + '\n')
        print(Pill_Outcome)

        setTime = setHour + ":" + setMin
        setDate = setDay + ' ' + setMonth + ' 2020'
        column = gspread.get_Set_Weekday_Column_Number(setDate)
        oldConf, oldRequest, oldReset = gspread.get_Email_Sizes()
        
        if(pill_Flag == True and activated_Flag == False):
            arduino.Activate_Alarm()
            activated_Flag = True
            activeCounter = 0
        elif(activeCounter > 2):
            arduino.Deactivate_Alarm()  
            if(pill_Flag != True):
                activated_Flag = False
            activeCounter = 0
        
        if (int(setHour) < 12):
            pillRow = 2
        elif (int(setHour) >= 12):
            pillRow = 3


        if(confSize > int(oldConf)):
            print("New Conf Mail" + "\n" + "____________________________________________" + "\n")
            gspread.Update_Spreadsheet_Cell(2, 10, confSize)
            gspread.Update_Spreadsheet_Cell(pillRow, column, setTime)
            
        if(requestSize > int(oldRequest)):
            print("New Request Mail" + "\n" + "____________________________________________" + "\n")
            gspread.Update_Spreadsheet_Cell(2, 11, requestSize)
            emailContent = colValues[0] + ":  " + colValues[1] + " "  + colValues[3] +  " |  " +colValues[2]+" "+colValues[4] + Pill_Outcome
            mail.Send_Request_Email(emailContent)
            
        if(resetSize > int(oldReset)):
            print("New Reset Mail" + "\n" + "____________________________________________" + "\n")
            gspread.Reset_Pills_Taken()
            gspread.Update_Spreadsheet_Cell(2, 12, resetSize )
        else:
            print("_____________________________________________" + "\n")
            
        time.sleep(2)
