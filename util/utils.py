import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
from sklearn.decomposition import PCA
from scipy.special import boxcox
import numpy as np
from constants.constants import *


def compute_skills_diff(df):
    for index, row in df.iterrows():
        df_rs = pd.DataFrame(row['requiredSkills'], columns=['operand', 'name', 'intVal', 'strVal', 'boolVal'])
        df_ms = pd.DataFrame(row['matchedSkills'], columns=['name', 'intVal', 'strVal', 'boolVal'])

        skillDiff = 0.0

        for _, row in df_rs.iterrows():
            if ((row['intVal'] != None) and (not (pd.isna(row['intVal'])))):
                name = row['name']
                rs = row['intVal']
                for _, row_ms in df_ms.iterrows():
                    if (row_ms['name'] == name):
                        ms = row_ms['intVal']
                        # print("ms int_val", ms, "rs int_val", rs, " name rs ", row['name'], " name ms ",row_ms['name'])
                if (row['operand'] == 'gte'):
                    skillDiff += ms - rs
                    # print("skillDiff in gte: ", skillDiff, "ms int_val", ms, "rs int_val", rs, " name: ", row['name'])
                else:
                    skillDiff += rs - ms
                    # print("skillDiff in lte: ", skillDiff, "ms int_val", ms, "rs int_val", rs, " name: ", df_ms.iloc[index]['name'])

        df.loc[index, 'skillDiff'] = skillDiff
    return df


def extract_seconds(df, field, toField):
    for index, row in df.iterrows():
        seconds = 0
        if (pd.isna(row[field])):
            df.loc[index, toField] = 0
            continue
        durations = row[field].split(":")
        # print(durations)
        if len(durations) == 1:
            seconds = int(durations[0])
        elif len(durations) == 2:
            seconds = int(durations[0]) * 60 + int(durations[1])
        else:
            seconds = int(durations[0]) * 60 * 60 + int(durations[1]) * 60 + int(durations[2])
        # print(seconds)
        df.loc[index, toField] = seconds
    return df


def get_queue_and_agent_and_team(df):
    for index, row in df.iterrows():
        contributors_size = len(row['contributors'])

        df_queue = pd.DataFrame(row['lastQueue'], columns=['id'], index=[0])
        df_team = pd.DataFrame(row['lastTeam'], columns=['id'], index=[0])
        df_agent = pd.DataFrame(row['contributors'][contributors_size - 1], columns=['id'], index=[0])

        df.loc[index, 'queue'] = df_queue.iloc[0]['id']
        df.loc[index, 'agent'] = df_agent.iloc[0]['id']
        df.loc[index, 'team'] = df_team.iloc[0]['id']

    return df


def delete_cols(df):
    return df.drop(["requiredSkills", "lastQueue", "contributors"], axis=1)


def agent_queue_diagnostics(df):
    empty_agent = []
    empty_queue = []

    for index, row in df.iterrows():
        # print(row['Contributors'])
        contributors_size = len(row['contributors'])
        if ((contributors_size == 0)):
            empty_agent.append(row['id'])

    df = df[~(df.id.isin(empty_agent))]

    for index, row in df.iterrows():
        queue_size = len(row['lastQueue'])
        if queue_size == 0:
            empty_queue.append(row['id'])

    # print(empty_queue)
    df = df[~(df.id.isin(empty_queue))]
    return df


def diagnostics(df):
    for index, row in df.iterrows():
        contributors_size = len(row['contributors'])
        if contributors_size > 1:
            print(row['id'])
            print(row['createdTime'])


def extract_skills(df):
    if SOURCE == 'maersk':
        for index, row in df.iterrows():
            # print(row['Skills'])
            if (pd.isna(row['skills'])):
                continue
            skill = row['skills'].str.split(r'(?:<|<=|>|>=|=)', expand=True)[0]
            df.loc[index, 'skills'] = skill
            # print(skill)
        return df
    else:
        for index, row in df.iterrows():
            df_rs = pd.DataFrame(row['requiredSkills'], columns=['operand', 'name', 'intVal', 'strVal', 'boolVal'])
            df_ms = pd.DataFrame(row['matchedSkills'], columns=['name', 'intVal', 'strVal', 'boolVal'])
            rs = ','.join(df_rs.name.unique())
            ms = ','.join(df_ms.name.unique())
            df.loc[index, 'rs'] = rs
            df.loc[index, 'ms'] = ms
        return df


def get_unique_values_of_col(df, col):
    print(df[col].unique())


def get_engineered_data_train():
    df_train = pd.read_csv('../data/{0}/engineered_data_train.csv'.format(SOURCE))
    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', 15)
    df_train.info()
    return df_train


def get_encoded_data(shouldFilterCol=True):
    df_train = pd.read_csv('../data/{0}/encoded_data_train.csv'.format(SOURCE))
    df_train = df_train[TOP_COLS] if shouldFilterCol else df_train
    df_test = pd.read_csv('../data/{0}/encoded_data_test.csv'.format(SOURCE))
    df_test = df_test[TOP_COLS] if shouldFilterCol else df_test
    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', 15)
    df_train.info()
    return df_train, df_test


def get_encoded_data_test():
    df_test = pd.read_csv('../data/{0}/encoded_data_test.csv'.format(SOURCE))
    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', 15)
    return df_test


def split_into_x_y(df_train, df_test, isPCA=False, isTransformY=False):
    pca = PCA(n_components=10)
    columns = df_train.columns
    y_col = [Y]
    x_col = list(set(columns) - set(y_col))

    x_train = pca.fit_transform(df_train[x_col]) if isPCA else df_train[x_col]
    y_train = boxcox(df_train[y_col], 0.6) if isTransformY else df_train[y_col]  # stats.boxcox(df_train[y_col]) \

    x_test = pca.transform(df_test[x_col]) if isPCA else df_test[x_col]
    y_test = boxcox(df_test[y_col], 0.6) if isTransformY else df_test[y_col]  # stats.boxcox(df_test[y_col])

    return x_train, y_train, x_test, y_test


def split_into_channel(df):
    df_telephony = df[df['channelType_telephony'] == 1]
    df_email = df[df['channelType_email'] == 1]
    df_chat = df[df['channelType_chat'] == 1]

    return df_telephony, df_email, df_chat
