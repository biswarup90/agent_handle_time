import pandas as pd
from sklearn.model_selection import train_test_split
from util.utils import get_unique_values_of_col
from constants.constants import *
def get_data():
    df = pd.read_csv('../data/{0}/data.csv'.format(DATA_SOURCE))
    print(df.info())

def imputation():
    df = pd.read_csv('../data/{0}/data.csv'.format(DATA_SOURCE))
    print((get_unique_values_of_col(df, "contactReason")))

    #Filter null
    df = filter_null(df)

    #remove outliers
    outlier_cols = OUTLIER_COLS
    for col in outlier_cols:
        df = remove_outliers(df, col, 0.9)

    #impute
    values = IMPUTER
    df = df.fillna(value=values)

    #Drop columns
    df.drop(DROP_COLS_IMPUTER, axis=1, inplace=True)

    #df = df[df['agent'] == 'c0451ecd-602a-4835-894d-486e61aade9f']
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    df_train.to_csv('../data/{0}/imputed_data_train.csv'.format(DATA_SOURCE), index=False)
    df_test.to_csv('../data/{0}/imputed_data_test.csv'.format(DATA_SOURCE), index=False)

    print(df.info())
    print(df_train.info())
    print(df_test.info())

def filter_null(df):
    for col in NOT_NULL:
        df = df.loc[df[col].notnull()]
    df = df.loc[df['connectedDuration']!=0]
    #df = df.loc[df['connectedDuration'] > 10000]
    #df = df.loc[df['connectedCount'] == 1]

    return df


def remove_outliers(df, col, percentile):
    q = df[col].quantile(percentile)
    df = df[df[col] < q]
    return df

imputation()
