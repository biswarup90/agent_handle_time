import pandas as pd
from category_encoders import TargetEncoder
from sklearn.preprocessing import OneHotEncoder
from constants.constants import *


def encoder():
    df_train = pd.read_csv('../data/{0}/engineered_data_train.csv'.format(SOURCE))
    df_test = pd.read_csv('../data/{0}/engineered_data_test.csv'.format(SOURCE))
    for cols in TARGET_ENCODING_COLS:
        encoder = TargetEncoder(smoothing=2)
        df_train['{0}_encoded'.format(cols)] = encoder.fit_transform(df_train[cols], df_train[Y])
        df_test['{0}_encoded'.format(cols)] = encoder.transform(df_test[cols], df_test[Y])

    ohe_encoder = OneHotEncoder(categories='auto', sparse_output=False, handle_unknown='ignore')

    X_train = ohe_encoder.fit_transform(
        df_train[OHE_COLS])
    X_train = pd.DataFrame(X_train, columns=ohe_encoder.get_feature_names_out())
    df_train = pd.concat([df_train, X_train], axis=1)

    X_test = ohe_encoder.transform(
        df_test[OHE_COLS])
    X_test = pd.DataFrame(X_test, columns=ohe_encoder.get_feature_names_out())
    df_test = pd.concat([df_test, X_test], axis=1)

    df_train = df_train.drop(DROP_COLS_ENCODER, axis=1)
    df_test = df_test.drop(DROP_COLS_ENCODER, axis=1)

    print(df_train.info())
    print(df_test.info())

    df_train.to_csv('../data/{0}/encoded_data_train.csv'.format(SOURCE), index=False)
    df_test.to_csv('../data/{0}/encoded_data_test.csv'.format(SOURCE), index=False)


encoder()
