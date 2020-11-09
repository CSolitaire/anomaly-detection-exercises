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
    df['cohort_id'] = np.where((df.user_id.isin(bash_list)),60,df.cohort_id) 
    return df

def ds_df(df):
    'This function cleans the df and returns only ds cohorts'
    ds = df
    ds = ds[ds.cohort_id != 0]
    ds = ds[ds.cohort_id != 1]
    ds = ds[ds.cohort_id != 2]
    ds = ds[ds.cohort_id != 3]
    ds = ds[ds.cohort_id != 4]
    ds = ds[ds.cohort_id != 5]
    ds = ds[ds.cohort_id != 6]
    ds = ds[ds.cohort_id != 7]
    ds = ds[ds.cohort_id != 8]
    ds = ds[ds.cohort_id != 9]
    ds = ds[ds.cohort_id != 10]
    ds = ds[ds.cohort_id != 11]
    ds = ds[ds.cohort_id != 12]
    ds = ds[ds.cohort_id != 13]
    ds = ds[ds.cohort_id != 14]
    ds = ds[ds.cohort_id != 15]
    ds = ds[ds.cohort_id != 16]
    ds = ds[ds.cohort_id != 17]
    ds = ds[ds.cohort_id != 18]
    ds = ds[ds.cohort_id != 19]
    ds = ds[ds.cohort_id != 20]
    ds = ds[ds.cohort_id != 21]
    ds = ds[ds.cohort_id != 22]
    ds = ds[ds.cohort_id != 23]
    ds = ds[ds.cohort_id != 24]
    ds = ds[ds.cohort_id != 25]
    ds = ds[ds.cohort_id != 26]
    ds = ds[ds.cohort_id != 27]
    ds = ds[ds.cohort_id != 28] # Staff
    ds = ds[ds.cohort_id != 29]
    ds = ds[ds.cohort_id != 31]
    ds = ds[ds.cohort_id != 32]
    ds = ds[ds.cohort_id != 33]
    ds = ds[ds.cohort_id != 51]
    ds = ds[ds.cohort_id != 52]
    ds = ds[ds.cohort_id != 53]
    ds = ds[ds.cohort_id != 56]
    ds = ds[ds.cohort_id != 57]
    ds = ds[ds.cohort_id != 58]
    ds = ds[ds.cohort_id != 60]
    ds = ds[ds.cohort_id != 61]
    ds = ds[ds.cohort_id != 62]
    return ds

def webdev_df(df):
    'This function cleans the df and returns only wevdev cohorts'
    #webdev df
    webdev = df
    webdev = webdev[webdev.cohort_id != 30]
    webdev = webdev[webdev.cohort_id != 34]
    webdev = webdev[webdev.cohort_id != 55]
    webdev = webdev[webdev.cohort_id != 59]
    webdev = webdev[webdev.cohort_id != 28] # Staff
    return webdev