import requests
from auth.get_bearer_token import get_bearer_token
import pandas as pd
from util.utils import compute_skills_diff, get_queue_and_agent_and_team, delete_cols, diagnostics, agent_queue_diagnostics, extract_skills
import json

def hit_url(orgId, fromTimestamp, toTimeStamp, cursor, bearer_token):
    url = "https://api.qaus1.ciscoccservice.com/search"

    payload = "{\"query\":\"{\\n  taskDetails(\\n    from: 1654061960000 #26 June 22\\n    to: 1662523428257 #25 Dec 22\\n    filter: { and: [{ isActive: { equals: false } }\\n    { transferCount: { equals: null } }\\n    { direction: { equals: \\\"inbound\\\" } }\\n { connectedCount: {equals: 1}}\\n    { connectedDuration: {notequals: null}} ] }\\n    pagination : {\\n        cursor : \\\""+cursor+"\\\"\\n    }\\n  ) {\\n    tasks {\\n      id \\nmatchedSkills\\nlastTeam{\\n    id\\n}requiredSkills \\ncreatedTime \\nendedTime \\norigin \\ndestination \\ncontactReason \\nchannelSubType \\nchannelType\\nholdCount \\nholdDuration \\nselfserviceCount \\nselfserviceDuration \\nconnectedCount \\nconnectedDuration \\nringingDuration \\nqueueDuration \\nqueueCount \\nroutingType\\nisHandledByPreferredAgent\\nlastQueue{ \\n  id\\n} \\ncontributors{ \\n  id \\n} \\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    #payload = "{\"query\":\"{\\n  taskDetails(\\n    from: " + fromTimestamp + " #26 June 22\\n    to: " + toTimeStamp + " #25 Dec 22\\n    filter: { and: [{ isActive: { equals: false } }\\n    { transferCount: { equals: null } }\\n    { direction: { equals: \\\"inbound\\\" } }] }\\n    pagination : {\\n        cursor : \\\"0\\\"\\n     }\\n  ) {\\n    tasks {\\n      id\\n      matchedSkills\\n      requiredSkills\\n      channelType\\n      createdTime\\n      endedTime\\n      origin\\n      destination\\n      contactReason\\n      terminationType\\n      channelSubType\\n      #isActive\\n      totalDuration\\n      #csatScore\\n      #blindTransferCount\\n      #conferenceCount\\n      #conferenceDuration\\n      #consultCount\\n      #consultDuration\\n      #holdCount\\n      #holdDuration\\n      selfserviceCount\\n      selfserviceDuration\\n      connectedCount\\n      connectedDuration\\n      #consultToQueueCount\\n      #consultToQueueDuration\\n      #transferCount\\n      wrapupDuration\\n      ringingDuration\\n      queueDuration\\n      #queueCount\\n      lastQueue {\\n        id}\\n      contactHandleType\\n      contributors {\\n          id\\n      }\\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    #print(payload)
    headers = {
        'X-ORGANIZATION-ID': orgId,
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, data=payload)

def query_data(orgId, fromTimestamp, toTimeStamp):
    bearer_token = get_bearer_token()
    response = hit_url(orgId, fromTimestamp, toTimeStamp, "0", bearer_token).json()['data']['taskDetails']

    data = response['tasks']
    print(data)
    with open('../data/l/data1.json', 'w') as f:
        json.dump(data, f)
    while(response['pageInfo']['hasNextPage'] == True):
        response = hit_url(orgId, fromTimestamp, toTimeStamp, str(response['pageInfo']['endCursor']), bearer_token).json()['data']['taskDetails']
        print(response['tasks'])

        data.extend(response['tasks'])
        with open('../data/l/data1.json', 'w') as f:
            json.dump(data, f)

    return data


def convert_data_to_df():
    #query_data("348adfa2-b8f0-405c-a516-da004eefde5f", 1654061960000, 1675575560000)
    df = pd.read_json('../data/l/data.json')
    df = agent_queue_diagnostics(df)
    #diagnostics(df)
    df = compute_skills_diff(df)
    df = get_queue_and_agent_and_team(df)
    df = extract_skills(df)

    #df = delete_cols(df)

    print(df.info())
    df.to_csv('../data/l/data0.csv', index=False)

def merge_files():
    csv_list = []
    csv_list.append(pd.read_csv('../data/l/backup/data.csv'))
    csv_list.append(pd.read_csv('../data/l/backup/data1.csv'))
    csv_merged = pd.concat(csv_list, ignore_index=True)
    csv_merged.to_csv('../data/l/all_data.csv', index=False)
#query_data("348adfa2-b8f0-405c-a516-da004eefde5f", 1654061960000, 1675575560000)
#print(get_bearer_token())
#convert_data_to_df()
merge_files()