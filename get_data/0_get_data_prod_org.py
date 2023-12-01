import requests
from auth.get_bearer_token import get_bearer_token_prod, get_bearer_token
import pandas as pd

from constants.constants import ORG_ID
from util.utils import compute_skills_diff, get_queue_and_agent_and_team, delete_cols, diagnostics, \
    agent_queue_diagnostics, extract_skills
import json

filenames = ['data', 'data1', 'data2', 'test', 'predictiondata']
def hit_url(orgId, cursor, bearer_token):
    url = "https://api.wxcc-us1.cisco.com/search"
    #url = "https://api.qaus1.ciscoccservice.com/search"

    #outbound
    #payload = "{\"query\":\"{\\n  taskDetails(\\n    from: 1672546847000 #30 Apr 23\\n    to: 1685420447000 #29 May 23\\n    filter: { and: [{ isActive: { equals: false } }\\n   { direction: { equals: \\\"inbound\\\" } }\\n    { queueCount: {equals: 1}}\\n    { queueDuration: {notequals: null}}\\n    ] }\\n    pagination : {\\n        cursor : \\\"" + cursor + "\\\"\\n    }\\n  ) {\\n    tasks {\\n      id \\nmatchedSkills\\nlastTeam{\\n    id\\n}\\nrequiredSkills \\ncreatedTime \\nendedTime \\norigin \\ndestination \\ncontactReason \\nchannelSubType \\nchannelType\\nholdCount \\nholdDuration \\nselfserviceCount \\nselfserviceDuration \\nconnectedCount \\nconnectedDuration \\nringingDuration \\nqueueDuration \\nqueueCount \\nroutingType\\nisHandledByPreferredAgent\\nconferenceDuration\\nlastQueue{ \\n  id\\n} \\ncontributors{ \\n  id \\n} \\nlastSite{\\n    id\\n}\\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    #inbound-aht
    payload = ("{\"query\":\"{\\n  taskDetails(\\n    "
               "from: 1696132391000 #1 OCT 23\\n    "
               "to: 1701322176000 #30 NOV 23\\n    "
               "filter: { and: [{ isActive: { equals: false } }\\n    "
               "{ transferCount: { equals: null } }\\n    "
               "{ queueCount: { equals: 1 } }\\n    "
               "{ agentToDnTransferCount: { equals: null } }\\n    "
               "{ agentToAgentTransferCount: { equals: null } }\\n    "
               "{ blindTransferCount: { equals: null } }\\n    "
               "{ direction: { equals: \\\"inbound\\\" } }\\n    "
               "{ connectedCount: {equals: 1}}\\n    "
               "{ connectedDuration: {notequals: null}}\\n    ] }\\n    "
               "pagination : {\\n        cursor : \\\"")+cursor+("\\\"\\n    }\\n  )"
                                                                 " {\\n    tasks {\\n      "
                                                                 "id \\nmatchedSkills\\nlastTeam{\\n    "
                                                                 "id\\n}\\nrequiredSkills \\ncreatedTime \\nendedTime \\norigin \\ndestination \\ncontactReason \\nchannelSubType \\nchannelType \\nselfserviceCount \\nselfserviceDuration \\nconnectedCount \\nconnectedDuration \\nringingDuration \\nqueueDuration \\nqueueCount \\nroutingType\\nisHandledByPreferredAgent\\nconferenceDuration\\nlastQueue{ \\n  id\\n} \\ncontributors{ \\n  id \\n} \\nlastSite{\\n    id\\n}\\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}")
    # inbound-ewt
    #payload = "{\"query\":\"{\\n  taskDetails(\\n    from: 1687113000000 #30 Apr 23\\n    to: 1687285799000 #29 May 23\\n    filter: { and: [{ isActive: { equals: false } }\\n    { direction: { equals: \\\"inbound\\\" } }\\n    { queueCount: {equals: 1}}\\n    { queueDuration: {notequals: null}}\\n    ] }\\n    pagination : {\\n        cursor : \\\"" + cursor + "\\\"\\n    }\\n  ) {\\n    tasks {\\n      id \\nmatchedSkills\\nlastTeam{\\n    id\\n}\\nrequiredSkills \\ncreatedTime \\nendedTime \\norigin \\ndestination \\ncontactReason \\nchannelSubType \\nchannelType\\nholdCount \\nholdDuration \\nselfserviceCount \\nselfserviceDuration \\nconnectedCount \\nconnectedDuration \\nringingDuration \\nqueueDuration \\nqueueCount \\nroutingType\\nisHandledByPreferredAgent\\nconferenceDuration\\nlastQueue{ \\n  id\\n} \\ncontributors{ \\n  id \\n} \\nlastSite{\\n    id\\n}\\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    #payload = "{\"query\":\"{\\n  taskDetails(\\n    from: 1687113000000 #26 June 22\\n    to: 1687285799000 #25 Dec 22\\n    filter: { or: [\\n        { id: { equals: \\\"1ee0585b-adc5-426b-bf1e-ad8b675648c0\\\" } }\\n        { id: { equals: \\\"2c086f3f-5fec-4b73-91e2-3d230d00e835\\\" } }\\n        { id: { equals: \\\"430d9ab1-adc7-4c30-b8e9-7d42c3a6fc51\\\" } }\\n        { id: { equals: \\\"b172e74c-22c9-4a93-9e81-36f28c952a01\\\" } }\\n        { id: { equals: \\\"48a26934-6ca7-4617-9be3-451a35914b6c\\\" } }\\n     ] }\\n    pagination : {\\n        cursor : \\\"0\\\"\\n    }\\n  ) {\\n    tasks {\\n      id \\nmatchedSkills\\nlastTeam{\\n    id\\n}\\nisActive\\nrequiredSkills \\ncreatedTime \\nendedTime \\norigin \\ndirection\\nqueueCount\\ndestination \\ncontactReason \\nchannelSubType \\nchannelType\\nholdCount \\nholdDuration \\nselfserviceCount \\nselfserviceDuration \\nconnectedCount \\nconnectedDuration \\nringingDuration \\nqueueDuration \\nqueueCount \\nlastSite{\\n    id\\n}\\nroutingType\\nisHandledByPreferredAgent\\nlastQueue{ \\n  id\\n} \\ncontributors{ \\n  id \\n} \\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    # payload = "{\"query\":\"{\\n  taskDetails(\\n    from: " + fromTimestamp + " #26 June 22\\n    to: " + toTimeStamp + " #25 Dec 22\\n    filter: { and: [{ isActive: { equals: false } }\\n    { transferCount: { equals: null } }\\n    { direction: { equals: \\\"inbound\\\" } }] }\\n    pagination : {\\n        cursor : \\\"0\\\"\\n     }\\n  ) {\\n    tasks {\\n      id\\n      matchedSkills\\n      requiredSkills\\n      channelType\\n      createdTime\\n      endedTime\\n      origin\\n      destination\\n      contactReason\\n      terminationType\\n      channelSubType\\n      #isActive\\n      totalDuration\\n      #csatScore\\n      #blindTransferCount\\n      #conferenceCount\\n      #conferenceDuration\\n      #consultCount\\n      #consultDuration\\n      #holdCount\\n      #holdDuration\\n      selfserviceCount\\n      selfserviceDuration\\n      connectedCount\\n      connectedDuration\\n      #consultToQueueCount\\n      #consultToQueueDuration\\n      #transferCount\\n      wrapupDuration\\n      ringingDuration\\n      queueDuration\\n      #queueCount\\n      lastQueue {\\n        id}\\n      contactHandleType\\n      contributors {\\n          id\\n      }\\n    }\\n    pageInfo {\\n        hasNextPage \\n        endCursor\\n    }\\n  }\\n}\",\"variables\":{}}"
    # print(payload)
    headers = {
        'X-ORGANIZATION-ID': orgId,
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, data=payload)


def query_data(orgId, filename):
    bearer_token = get_bearer_token_prod()
    response = hit_url(orgId, "0", bearer_token).json()['data']['taskDetails']

    data = response['tasks']
    print(data)
    with open('../data/prod/{0}/{1}.json'.format(orgId, filename), 'w') as f:
        json.dump(data, f)
    while response['pageInfo']['hasNextPage']:
        response = hit_url(orgId, str(response['pageInfo']['endCursor']), bearer_token).json()['data']['taskDetails']
        print(response['tasks'])

        data.extend(response['tasks'])
        with open('../data/prod/{0}/{1}.json'.format(orgId, filename), 'w') as f:
            json.dump(data, f)

    return data


def convert_data_to_df(orgId, filename):
    df = pd.read_json('../data/prod/{0}/{1}.json'.format(orgId, filename))
    #df = df[df['channelType'] == 'telephony']
    df = agent_queue_diagnostics(df)
    print("Compute skills")
    # diagnostics(df)
    df = compute_skills_diff(df)
    print("get queue and agent and team")
    df = get_queue_and_agent_and_team(df)
    print("extract skills")
    df = extract_skills(df)

    # df = delete_cols(df)

    #print(df['agent'])
    df.to_csv('../data/prod/{0}/{1}.csv'.format(orgId, filename), index=False)


def merge_files(orgId):
    csv_list = [pd.read_csv('../data/prod/{0}/data0.csv'.format(orgId)), pd.read_csv('../data/prod/{0}/data1.csv'.format(orgId))]
    csv_merged = pd.concat(csv_list, ignore_index=True)
    csv_merged.to_csv('../data/prod/{0}/data.csv'.format(orgId), index=False)


def test():
    with open('../data/prod/467dcff4-6c01-4615-afd3-c2b83f53e969/data.json') as data_file:
        data = json.load(data_file)
        print(data)

#query_data(ORG_ID, filenames[0])
convert_data_to_df(ORG_ID, filenames[0])
#test()
#print(get_bearer_token_prod())
#merge_files(orgId)

