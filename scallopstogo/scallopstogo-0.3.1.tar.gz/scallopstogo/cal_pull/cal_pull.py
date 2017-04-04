import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

class GoogleService(object):
    '''
    class connects to google apis and then has several methods that connect to google cal api

    __init__ needs:
        storage (str), service_type (str), version_type (str)
    '''

    def __init__(self, storage, service_type, version_type):
        self.storage = storage
        self.service_type = service_type
        self.version_type = version_type
        self.google_service = self.get_google_service()

    def get_google_service(self):
        '''
        function takes json storage variable and returns calendar api connection
        ex. for calendar: service_type: calendar, version_type: v3
        '''
        storage = self.storage
        # parse json from storage key
        storage = json.loads(storage.replace('\n', ''))

        access_token = storage['access_token']
        client_id = storage['client_id']
        client_secret = storage['client_secret']
        refresh_token = storage['refresh_token']
        expires_at = storage['token_response']['expires_in']
        user_agent = storage['user_agent']
        token_uri = storage['token_uri']

        # auth to google, this function will return a refresh token
        cred = client.GoogleCredentials(access_token, client_id, client_secret,
                                        refresh_token, expires_at, token_uri, user_agent,
                                        revoke_uri="https://accounts.google.com/o/oauth2/token")
        http = cred.authorize(Http())
        cred.refresh(http)
        service = build(self.service_type, self.version_type, credentials=cred)

        return service

    def get_entity_busy_status(self, start, end, entity_list):
        '''
        check if something is busy, if busy then true if not false
        requires gcal service, start and end time, and list of people you want to get
        the busy status of

        returns: times where the entity(person) is busy in their respective calendar
        '''

        item_list = [{'id':e} for e in entity_list]

        body = {
            "timeMin": start + 'Z',
            "timeMax": end + 'Z',
            "timeZone": 'US/Central',
            #           "items": [{"id": entity}]
            "items": item_list
            }

        return self.google_service.freebusy().query(body=body).execute()

    def get_events(self, calendar, start, end, num_events, time_zone_str='America/Chicago'):
        '''
        get all available events in the time frame

        inputs:
        calendar - str of google cal
        start / end - str need to be in google cal time format
        num_events - the max number of events desired to be returned
        time_zone_str - time zone of cal

        return df of event ids
        '''

        events_result = self.google_service.events().list(calendarId=calendar, timeMin=start, timeMax=end,
                                                          timeZone=time_zone_str, maxResults=num_events,
                                                          singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        event_list = []
        if not events:
            print 'No upcoming events found.'
        else:
            for event in events:
        # get event ids and other info about meeting
                event_id = event['id']
                if 'summary' in event:
                    event_sum = event['summary']
                else:
                    event_sum = 'could not get summary'
                if 'description' in event:
                    event_desc = event['description']
                else:
                    event_desc = 'could not get description'
                start_time = event['start'].get('dateTime')
                end_time = event['end'].get('dateTime')
                if 'attendees' in event:
                    event_attendees = event['attendees']
                else:
                    event_attendees = 'could not get attendees'
                if 'location' in event:
                    location = event['location']
                else:
                    location = 'no room currently booked'

                event_stats = [event_id, event_sum, event_desc, start_time, end_time, location, event_attendees]
                event_list.append(event_stats)
        # shove into dataframe if events_list not empty
        try:
            df_events = pd.DataFrame(event_list, columns=['event_id', 'summary', 'description', 'start_time',\
                                                          'end_time', 'location', 'event_attendees'])
        except KeyError:
            df_events = pd.DataFrame()

        return df_events

    def add_sub_attendees_to_cal(self, calendar, event_list, to_change, add_to_cal=True):
        '''
        function takes list of events and adds everyone to the event ids in df

        calendar - str google calendar
        event_list - list of event ids to add or subtract
        to_change - email addresses that need to be changed
        add_to_cal - boolean add or subtract (default=True)

        returns list of emails that failed to be added to event
        '''

        failed_to_drop_list = []
        for i in range(0, len(event_list)):
            event = self.google_service.events().get(calendarId=calendar, eventId=event_list[i]).execute()

            # if there are existing attendees keep them, if not add to dict
            if add_to_cal is True:
                try:
                    event['attendees'] += to_change
                except KeyError:
                    event['attendees'] = to_change
            else:
                for email_dict in to_change:
                    try:
                        # gets the position in the list
                        email_pos = next(index for (index, d) in enumerate(event['attendees']) \
                                        if d['email'] == email_dict['email'])
                        # delete from attendees
                        event['attendees'].pop(email_pos)
                    except:
                        failed_to_drop_list.append(email_dict['email'])

            updated_event = self.google_service.events().update(calendarId=calendar, sendNotifications=True,
                                                                eventId=event['id'], body=event).execute()

        return failed_to_drop_list
