################################################# Imports #################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
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

################################################# Vanilla IQR Function ################################################# 

def get_lower_and_upper_bounds(s, k): 
    'This function takes in a pandads series and a k value to return lower and upper bounds' 
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    lower_bound = q1 - k * iqr
    return upper_bound, lower_bound

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