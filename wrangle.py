################################### Imports ################################################
import pandas as pd
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
    df = df.fillna(0)
    # Add Ada to df
    ada_list =[349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,372,375,346]
    df['cohort_id'] = np.where((df.user_id.isin(ada_list)),30,df.cohort_id) 
    # Add Bash to df
    bash_list = [713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,731,736,744,782]
    df['cohort_id'] = np.where((df.user_id.isin(ada_list)),60,df.cohort_id) 
    return df
