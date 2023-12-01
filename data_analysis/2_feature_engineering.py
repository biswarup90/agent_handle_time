import pandas as pd
from constants.constants import *

def engineered():
    df_train = pd.read_csv('../data/{0}/imputed_data_train.csv'.format(DATA_SOURCE))
    df_test = pd.read_csv('../data/{0}/imputed_data_test.csv'.format(DATA_SOURCE))

    if SOURCE == 'm':
        df_train['createdTime'] = pd.to_datetime(df_train['createdTime'], format='%d/%m/%Y %H:%M')
    df_train['createdTime'] = pd.to_datetime(df_train['createdTime'], unit='ms')

    df_train['createdTime_year'] = df_train['createdTime'].dt.year
    df_train['createdTime_month'] = df_train['createdTime'].dt.month
    df_train['createdTime_week'] = df_train['createdTime'].dt.week
    df_train['createdTime_day'] = df_train['createdTime'].dt.day
    df_train['createdTime_hour'] = df_train['createdTime'].dt.hour
    df_train['createdTime_minute'] = df_train['createdTime'].dt.minute
    df_train['createdTime_dayofweek'] = df_train['createdTime'].dt.dayofweek

    if SOURCE=='l':
        df_train_skills = df_train['rs'].str.get_dummies(sep=',')
        df_train = pd.concat([df_train, df_train_skills], axis=1).drop('rs', 1)
    #df_train = df_train.drop('rs', 1)
    df_train = df_train.drop(['createdTime'], axis=1)
    print(df_train.info())

    if SOURCE == 'm':
        df_test['createdTime'] = pd.to_datetime(df_test['createdTime'], format='%d/%m/%Y %H:%M')
    df_test['createdTime'] = pd.to_datetime(df_test['createdTime'], unit='ms')

    df_test['createdTime_year'] = df_test['createdTime'].dt.year
    df_test['createdTime_month'] = df_test['createdTime'].dt.month
    df_test['createdTime_week'] = df_test['createdTime'].dt.week
    df_test['createdTime_day'] = df_test['createdTime'].dt.day
    df_test['createdTime_hour'] = df_test['createdTime'].dt.hour
    df_test['createdTime_minute'] = df_test['createdTime'].dt.minute
    df_test['createdTime_dayofweek'] = df_test['createdTime'].dt.dayofweek

    if SOURCE=='l':
        df_test_skills = df_test['rs'].str.get_dummies(sep=',')
        df_test = pd.concat([df_test, df_test_skills], axis=1).drop('rs', 1)
    #df_test = df_test.drop('rs', 1)

    df_test = df_test.drop(['createdTime'], axis=1)
    print(df_test.info())

    df_train.to_csv('../data/{0}/engineered_data_train.csv'.format(DATA_SOURCE), index=False)
    df_test.to_csv('../data/{0}/engineered_data_test.csv'.format(DATA_SOURCE), index=False)
    #print(df['agent'].value_counts(normalize=True))
    #print(df['queue'].unique())
    #print(len(df['agent'].unique()))

    #print(df[''].value_counts())


engineered()