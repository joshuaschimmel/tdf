import json
from datetime import datetime
import pandas as pd
import pytz

# load data into python dict
with open('data.json', 'r') as f:
    data = json.load(f)

# create pandas df
df = pd.DataFrame.from_dict(data['data'])

# Constants for timezones
DST_TRANSITION = '2022-10-30 02:00:00'
MADRID_TZ = pytz.timezone('Europe/Madrid')
# flag for switch between timezones
dst_transitioned = False

def convertTime(timestring):
    """Transforms timestring from madrid time to UTC.

    :param timestring: local timestring
    :type timestring: String
    :return: iso-timestring in UTC
    :rtype: String
    """
    global dst_transitioned
    # create naive datetime object
    naive_datetime = datetime.fromisoformat(timestring)
    # normalize using timezone
    local_datetime = MADRID_TZ.localize(
        naive_datetime, 
        is_dst=dst_transitioned
    )
    # create utc datetime object
    utc_datetime = local_datetime.astimezone(pytz.UTC)
    # extract iso string
    utc_string = utc_datetime.isoformat()
    
    # check if transition-date has been reached
    # allow first date passing the transition to still be executed w/o dst
    if(not dst_transitioned and timestring >= DST_TRANSITION):
        dst_transitioned = True
        
    return utc_string

# apply convert function to every element in column
df['fecha_completa'] = df['fecha_completa'].apply(convertTime)

# export to csv
df.to_csv('data.csv')