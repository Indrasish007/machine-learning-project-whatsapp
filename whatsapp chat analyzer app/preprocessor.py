import pandas as pd
import re
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({"user_message":message,"message_date":dates})
    df["message_date"]=pd.to_datetime(df["message_date"], format='%d/%m/%y, %H:%M - ') #what if the user inputted wrong format
    df.rename(columns={'message_date' : 'date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    df["year"]=df["date"].dt.year
    df["month"]=df["date"].dt.month_name()
    df["day"]=df["date"].dt.day
    df["hour"]=df["date"].dt.hour
    df["minute"]=df["date"].dt.minute
    return df