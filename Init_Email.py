import imaplib, smtplib, http.client, urllib
import time, requests, bs4

username = "falconhoofpi@gmail.com"
password = "ImSorryJohn69"


def Read_Config_Email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select("inbox")
    retcode, response = mail.search(None, "SUBJECT","Conf")

    for i in response[0].split():
        tpe, data = mail.fetch(i,'(RFC822)')

    strEmail = str(data) 
    f3 = strEmail.find("Test")+5
    strDate = strEmail[f3:f3+10].split(",")
    day, month, hhmm = strDate[:]
    confsize = len(strEmail)
    hours = hhmm[:2]
    mins = hhmm[2:]

    return day, month, hours, mins, confsize

def Read_Request_Email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username,password)
    mail.select("inbox")
    retcode, response = mail.search(None, "SUBJECT", "Request")
    for i in response[0].split():
        tpe, data = mail.fetch(i,'(RFC822)')
    strEmail = str(data)
    requestSize = len(strEmail)
    return requestSize

def Read_Reset_Email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username,password)
    mail.select("inbox")
    retcode, response = mail.search(None, "SUBJECT", "Reset")
    for i in response[0].split():
        tpe, data = mail.fetch(i,'(RFC822)')
    strEmail = str(data)
    resetSize = len(strEmail)
    return resetSize

def Send_Request_Email(emailContent):
    msg = 'Subject: {}\n\n{}'.format("Requested Schedule", emailContent)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(username, password)
    s.sendmail(username, username, msg)
    s.quit()

