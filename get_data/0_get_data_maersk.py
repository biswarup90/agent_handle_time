import requests
from auth.get_bearer_token import get_bearer_token
import pandas as pd
from util.utils import compute_skills_diff, get_queue_and_agent, delete_cols, diagnostics, agent_queue_diagnostics, \
    extract_skills, extract_seconds
import json
import datetime as dt

files = ['../data/January_ES.xlsx', '../data/February_ES.xlsx',
         '../data/March_ES.xlsx', '../data/April_ES.xlsx',
         '../data/May_ES.xlsx', '../data/June_ES.xlsx', '../data/July_ES.xlsx',
         '../data/August_ES.xlsx', '../data/September_ES.xlsx',
         '../data/October_ES.xlsx', '../data/November_ES.xlsx', '../data/December_ES.xlsx']
q_files = ['../data/FQN_January_ES.xlsx', '../data/FQN_February_ES.xlsx',
         '../data/FQN_March_ES.xlsx', '../data/FQN_April_ES.xlsx',
         '../data/FQN_May_ES.xlsx', '../data/FQN_June_ES.xlsx', '../data/FQN_July_ES.xlsx',
         '../data/FQN_August_ES.xlsx', '../data/FQN_September_ES.xlsx',
         '../data/FQN_October_ES.xlsx', '../data/FQN_November_ES.xlsx', '../data/FQN_December_ES.xlsx']
files_csv = ['../data/January_ES.csv', '../data/February_ES.csv',
             '../data/March_ES.csv', '../data/April_ES.csv',
             '../data/May_ES.csv', '../data/June_ES.csv', '../data/July_ES.csv',
             '../data/August_ES.csv', '../data/September_ES.csv',
             '../data/October_ES.csv', '../data/November_ES.csv', '../data/December_ES.csv']


def merge_files():
    csv_list = []

    for i in range(12):
        df = pd.read_excel(q_files[i])
        df.to_csv(files_csv[i])

    for i in range(12):
        csv_list.append(pd.read_csv(files_csv[i]))

    csv_merged = pd.concat(csv_list, ignore_index=True)
    csv_merged.to_csv('../data/all_q_data.csv', index=False)


def process_data():
    df = pd.read_csv('../data/all_data.csv')
    print(df.info())
    df = df.drop_duplicates()
    df = agent_queue_diagnostics(df)
    #extract_skills(df)
    df['skill'] = df['Skills'].str.split(r'(?:<|<=|>|>=|=)', expand=True)[0]
    # df['holdDuration'] = pd.to_datetime(df['Hold Duration']).dt.total_seconds()
    # df2 = df[df['ID'] == 'b673e5357ff54449b4140c6c537790ca']
    df = extract_seconds(df, 'Connected Duration', 'connectedDuration')
    df = extract_seconds(df, 'Hold Duration', 'holdDuration')
    df = extract_seconds(df, 'Queue Duration', 'queueDuration')
    df = extract_seconds(df, 'Ringing Duration', 'ringingDuration')
    df = extract_seconds(df, 'IVR Duration', 'IVRDuration')
    # 3print(df2)

    df = df.rename({'Created Time': 'createdTime', 'Origin': 'origin', 'Destination': 'destination', 'Hold Count': 'holdCount',
               'IVR Count': 'IVRCount', 'Connected Count': 'connectedCount', 'Queue Count': 'queueCount', 'contributors': 'agent'}, axis=1)
    print(df.info())
    print(df.head(5))
    df.to_csv('../data/data0.csv', index=False)


def test():
    date = '21/06/2022 13:07'
    x = dt.datetime.strptime(date, "%d/%m/%Y %H:%M")
    print(x)


process_data()
