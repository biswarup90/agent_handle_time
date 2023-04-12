import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from util.utils import split_into_x_y, get_encoded_data

def kmeans(df_train, df_test):
    kmeans_model = KMeans(2)
    cluster_train = kmeans_model.fit_predict(df_train)
    cluster_test = kmeans_model.predict(df_test)
    df_train['cluster'] = pd.Series(cluster_train, index=df_train.index)
    df_test['cluster'] = pd.Series(cluster_test, index=df_test.index)

    return df_train, df_test


def split_into_cluster(df_train, df_test):
    df_train_0 = df_train[df_train['cluster'] == 0]
    df_train_1 = df_train[df_train['cluster'] == 1]

    df_test_0 = df_test[df_test['cluster'] == 0]
    df_test_1 = df_test[df_test['cluster'] == 1]

    return df_train_0, df_train_1, df_test_0, df_test_1


def split_into_x_y_with_cluster(df_train_0, df_train_1, df_test_0, df_test_1):
    columns = df_train_0.columns
    y_col = ['connectedDuration']
    x_col = list(set(columns) - set(y_col))

    x_train_0 = df_train_0[x_col]
    y_train_0 = df_train_0[y_col]

    x_train_1 = df_train_1[x_col]
    y_train_1 = df_train_1[y_col]

    x_test_0 = df_test_0[x_col]
    y_test_0 = df_test_0[y_col]

    x_test_1 = df_test_1[x_col]
    y_test_1 = df_test_1[y_col]

    return x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1


def simple_model_eval(m1):
    df_train, df_test = get_encoded_data()

    x_train, y_train, x_test, y_test = split_into_x_y(df_train, df_test)
    print("Training starting")
    m1.fit(x_train, np.ravel(y_train))
    print("Training over")
    return m1, x_train, y_train, x_test, y_test

def nn_model_eval(m1):
    df_train = pd.read_csv('../data/encoded_data_train.csv')
    df_test = pd.read_csv('../data/encoded_data_test.csv')

    x_train, y_train, x_test, y_test = split_into_x_y(df_train, df_test)
    print("Training starting")
    m1.fit(x_train, np.ravel(y_train), epochs=150, batch_size=10)
    print("Training over")
    return m1, x_train, y_train, x_test, y_test


def model_with_kmeans_eval(m1, m2):
    df_train = pd.read_csv('../data/encoded_data_train.csv')
    df_test = pd.read_csv('../data/encoded_data_test.csv')

    df_train, df_test = kmeans(df_train, df_test)
    df_train_0, df_train_1, df_test_0, df_test_1 = split_into_cluster(df_train, df_test)

    x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 = split_into_x_y_with_cluster(
        df_train_0,
        df_train_1,
        df_test_0,
        df_test_1)

    m1.fit(x_train_0, y_train_0)
    m2.fit(x_train_1, y_train_1)

    return m1, m2, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1
