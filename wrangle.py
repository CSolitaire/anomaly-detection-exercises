################################### Imports ################################################
import pands as pd
import numpy as np 

################################### Acquire ################################################

def read_csv():
    'This function reads in a csv and returns a df'
    df= pd.read_csv('anonymized-curriculum-access.txt', sep=" ", header=None)
    return df

################################### Wrangle ################################################

def ip_to_int(ip_ser):
    'This function takes an ip address and converts it into an int'
    ips = ip_ser.str.split('.', expand=True).astype(np.int16).values
    mults = np.tile(np.array([24, 16, 8, 0]), len(ip_ser)).reshape(ips.shape)
    return np.sum(np.left_shift(ips, mults), axis=1)

def wrangle_df(df):
    'This function transforms the raw df in to a df we can use to explore.  It adds datetime components and converts ip address to int'
    df.columns = ['date', 'time', 'page_viewed', 'user_id', 'cohort_id', 'ip']
    df["datetime"] = df["date"] + ' '+ df["time"]
    df['datetime'] = pd.to_datetime(df.datetime)
    df['year'] = df.datetime.dt.year
    df['month'] = df.datetime.dt.month
    df['day'] = df.datetime.dt.day
    df['hour'] = df.datetime.dt.hour
    df['weekday'] = df.datetime.dt.day_name()
    df = df.astype(object)
    df = df.set_index('datetime')
    df.drop(columns=['date', 'time'], inplace = True)
    df['int_ip'] = ip_to_int(df.ip)
    return df
