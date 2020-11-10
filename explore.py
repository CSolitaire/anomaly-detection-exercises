################################################# Imports #################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
################################################# Split df ################################################# 

def split_df(df):
    '''
    This function splits our dataframe in to train, validate, and test
    '''
    # split dataset
    train_validate, test = train_test_split(df, test_size = .2, random_state = 123)
    train, validate = train_test_split(train_validate, test_size = .3, random_state = 123)
    return train, validate, test  

################################################# Computer Entropy ################################################# 

def compute_entropy(series):
    'This function computes entropy (variability) inside of a feature'
    counts = series.value_counts()
    if len(counts)==1:
        ent = 0
    else:
        value, counts = np.unique(series, return_counts=True)
        ent = entropy(counts, base=None)
    return ent

################################################# Histogram Function #################################################

def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    plt.rc('figure', figsize=(11, 9))
    plt.rc('font', size=13)
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='blue', ec='black')
    plt.suptitle('Numeric Column Distributions')
    plt.tight_layout()
    plt.show()

################################################# Upper and Lower Bounds IQR Function ################################################# 

def get_lower_and_upper_bounds(s, k): 
    'This function takes in a pandads series and a k value to return lower and upper bounds' 
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    lower_bound = q1 - k * iqr
    return upper_bound, lower_bound

################################################# Upper and Lower Emperical Formula ################################################# 

def sigma_outliers(df_col, sigma = 3):
    'This Functions calculates the z-score, applies that to an upper and lower bound, and returns those values'
    # Calculate z-score
    zscore =abs((df_col).mean()) / (df_col.std())
    # Calculate upper bound
    upper_bound = (zscore * sigma) + df_col.mean()
    # Calculate lower bound
    lower_bound = df_col.mean() - (zscore * sigma) 
    return upper_bound, lower_bound

"""
for col in df:
    print(col)
    upper_bound, lower_bound = sigma_outliers(df[col])
    print('lower bound:', lower_bound)
    print('upper bound:', upper_bound,"\n")
"""


################################################# Hardcore Outliers and IQR As Columns #################################################


###################################### STEP #1

def get_upper_outliers(s, k):  
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.
    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k): # Call This Function First
    '''
    Add a column with the suffix _outliers for all the numeric columns
    in the given dataframe.
    '''
    # outlier_cols = {col + '_outliers': get_upper_outliers(df[col], k)
    #                 for col in df.select_dtypes('number')}
    # return df.assign(**outlier_cols)
    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)
    return df

# add_upper_outlier_columns(X_train_explore, k=1.5) ** This is how to call the function

###################################### STEP #2 
# In the next cell type the following

#This text prints information regrding the outlier columns created
'''
add_upper_outlier_columns(df, k=1.5)    
outlier_cols = [col for col in df if col.endswith('_outliers')]
for col in outlier_cols:
    print('~~~\n' + col)
    data = df[col][df[col] > 0]
    print(data.describe())
'''
###################################### STEP #3

# This function deletes the added columns
'''
train = train[train.columns.drop(list(train.filter(regex='_outliers')))]
'''

################################################# Chort ID Function #################################################

def cohort_id(df, year, month, day, hour):
    'This function takes in a dataframe and parameters to return a df that identifies cohort ID'
    df = df[df.year == year]
    df = df[df.month == month]
    df = df[df.day == day]
    df = df[df.hour == hour]
    return df

################################################# Data Science Page Hit Counter Function #################################################

def ds_page_hit_counter(ds):
    ds_curriculum = pd.DataFrame({'fundimentals': [ds.page_viewed.str.contains('fundamentals').sum()],
                              'stats': [ds.page_viewed.str.contains('stats').sum()],
                              'sql': [ds.page_viewed.str.contains('sql').sum()],
                              'python': [ds.page_viewed.str.contains('python').sum()],
                              'regression': [ds.page_viewed.str.contains('regression').sum()],
                              'classification': [ds.page_viewed.str.contains('classification').sum()],
                              'clustering': [ds.page_viewed.str.contains('python').sum()],
                              'time_series': [ds.page_viewed.str.contains('time').sum() | ds.page_viewed.str.contains('series').sum()],
                              'anomoly_detection': [ds.page_viewed.str.contains('anomoly').sum() | ds.page_viewed.str.contains('detection').sum()],
                              'natural_language': [ds.page_viewed.str.contains('nlp').sum()],
                              'distributed_machine_learning': [ds.page_viewed.str.contains('distributed').sum()],
                              'storytelling': [ds.page_viewed.str.contains('story').sum() | ds.page_viewed.str.contains('telling').sum()],
                              'advanced_topics': [ds.page_viewed.str.contains('advanced').sum() | ds.page_viewed.str.contains('topics').sum()]})
    return ds_curriculum

################################################# WebDev Page Hit Counter Function #################################################