import streamlit as st
import pickle
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
st.title('# ADD YOUR TASK')
credentials = None
@st.cache
def fetch_and_clean_data():
    cred = flow.run_local_server()
    return cred

if credentials == None :
    credentials = fetch_and_clean_data()
service = build("calendar", "v3", credentials=credentials)


## GET
result = service.calendarList().list().execute()


##ADD EVENTS
from datetime import datetime, timedelta
name = st.text_input('Name of event')
d = st.date_input("Date of event",datetime.now(),)
start = st.time_input('Time start', datetime.now())
start_time = datetime.combine(d,start)
end = st.time_input('Time end', datetime.now())

if end < start:
    st.error('Are you a time traveller ', icon="🤔")
else:
    end_time = datetime.combine(d, end)

timezone = 'Asia/Saigon'
repeat= st.selectbox(
    'Tag',
    ('Study', 'Play', 'Other'))

prio = st.slider('Priority', 1, 3, 1)
st.checkbox('Autoplan')
submit = st.button('submit')

if submit:
    event = {
      'summary': name,
      'location': place,
      'description': des ,
       'priotity' :prio,
      'start': {
        'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
      },
      'end': {
        'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
      },

    }
    event = service.events().insert(calendarId='primary', body=event).execute()

