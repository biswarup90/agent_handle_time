SOURCE = 'l'
NOT_NULL = ['connectedCount', 'connectedDuration', 'agent', 'Queue'] if SOURCE == 'm' else ['agent',
                                                                                            'connectedDuration']
NOT_NULL_EWT = ['connectedCount', 'connectedDuration', 'agent', 'Queue'] if SOURCE == 'm' else ['queueDuration']

#ORG_ID = '5a54948f-aeb3-4cb9-884d-f4440be66a6c' #rtms_qa
#ORG_ID = '348adfa2-b8f0-405c-a516-da004eefde5f' #lion king
#ORG_ID = '467dcff4-6c01-4615-afd3-c2b83f53e969' # simonmed imaging
#ORG_ID = '40751215-5fe2-46f3-8ce2-0b1cb55c1c5c'
#ORG_ID = '4df9bd96-7288-44a1-9f1c-40e2038d35b0' #Continental Money Exchange
#ORG_ID = 'b7299b4e-59e5-4d38-a80f-42ad8f6d6672'
ORG_ID = '9f468f32-7cef-40c2-80c5-6c8f4b2dd58b' #Springfield Clinic
DATA_SOURCE = 'prod/' + ORG_ID




OUTLIER_COLS = ['connectedDuration', 'holdDuration', 'queueDuration', 'ringingDuration',
                'IVRDuration'] if SOURCE == 'm' else ['connectedDuration']
IMPUTER = {"skill": "Blank"} if SOURCE == 'm' else {"contactReason": "Blank", "selfserviceCount": 0,
                                                    "selfserviceDuration": 0, "rs": "Blank", "ms": "Blank",
                                                    "routingType": "Blank", "origin": "Blank"}
DROP_COLS_IMPUTER = ['id', 'Contact Reason', 'Sub Channel Type', 'Skills', 'Connected Duration', 'Hold Duration',
                     'Queue Duration',
                     'Ringing Duration', 'IVR Duration', 'End Time', 'Channel Type'] if SOURCE == 'm' else [
    'matchedSkills', 'id', 'endedTime', 'connectedCount', 'requiredSkills', 'lastQueue', 'contributors', 'ms',
    'lastTeam', 'contactReason']
TARGET_ENCODING_COLS = ['origin', 'Queue', 'agent', 'skill', 'team'] if SOURCE == 'm' else ['origin', 'queue',
                                                                                            'agent', 'destination',
                                                                                            'team']
Y = 'connectedDuration'
OHE_COLS = ['destination'] if SOURCE == 'm' else ['channelSubType',
                                                  'isHandledByPreferredAgent', 'channelType', 'routingType']
DROP_COLS_ENCODER = ['origin', 'destination', 'agent', 'skill', 'Queue', 'Team'] if SOURCE == 'm' else ['origin',
                                                                                                        'destination',
                                                                                                        'queue',
                                                                                                        'agent',
                                                                                                        'channelSubType',
                                                                                                        'channelType',
                                                                                                        'isHandledByPreferredAgent',
                                                                                                        'routingType',
                                                                                                        'team']
TOP_COLS = ['connectedDuration', 'agent_encoded',
            'origin_encoded', 'skill_encoded',
            'queue_encoded', 'team_encoded'] if SOURCE == 'm' else ['connectedDuration', 'agent_encoded',
                                                                    'origin_encoded', 'destination_encoded',
                                                                    'queue_encoded', 'team_encoded', 'holdCount']
UNWANTED_COLS = ['selfserviceDuration', 'ringingDuration', 'destination_encoded', 'queueDuration',
                 'createdTime_hour', 'createdTime_day', 'createdTime_year', 'createdTime_month', 'createdTime_week',
                 'createdTime_minute', 'createdTime_dayofweek',
                 'queueCount', 'selfserviceCount']

BOX_COX_LAMBDA = 0.6
EWT_COLS = ['createdTime', 'origin', 'destination', 'channelSubType', 'channelType',
            'selfserviceCount', 'selfserviceDuration',
            'queueDuration', 'routingType', 'isHandledByPreferredAgent', 'queue', 'rs']
IMPUTER_EWT = {"skill": "Blank"} if SOURCE == 'm' else {"contactReason": "Blank", "selfserviceCount": 0,
                                                        "selfserviceDuration": 0, "rs": "Blank", "routingType": "Blank",
                                                        "origin": "Blank"}
Y_EWT = 'queueDuration'
OUTLIER_COLS_EWT = ['queueDuration']
NOT_NULL_EWT = ['queueDuration', 'queue']
TARGET_ENCODING_COLS_EWT = ['origin', 'Queue', 'agent', 'skill', 'team'] if SOURCE == 'm' else ['origin', 'queue',
                                                                                                'destination']
OHE_COLS_EWT = ['destination'] if SOURCE == 'm' else ['channelSubType',
                                                      'isHandledByPreferredAgent', 'channelType', 'routingType']

DROP_COLS_ENCODER_EWT = ['origin', 'destination', 'agent', 'skill', 'Queue', 'Team'] if SOURCE == 'm' else ['origin',
                                                                                                            'destination',
                                                                                                            'queue',
                                                                                                            'channelSubType',
                                                                                                            'channelType',
                                                                                                            'isHandledByPreferredAgent',
                                                                                                            'routingType']

DROP_COLS_EWT = ["destination_encoded",
                 "origin_encoded", "isHandledByPreferredAgent_False", "createdTime_year", "selfserviceCount", "routingType_queueBasedRouting", "channelSubType_broadcloud", "createdTime_month"]

TOP_COLS_EWT = ['connectedDuration', 'agent_encoded',
                'origin_encoded', 'skill_encoded',
                'queue_encoded', 'team_encoded'] if SOURCE == 'm' else ['queueDuration',
                                                                        'origin_encoded', 'destination_encoded',
                                                                        'queue_encoded', 'channelType_telephony',
                                                                        'channelType_email', 'channelType_chat']

TOP_COLS_DEBUGGING = ['agent_encoded', 'team_encoded', 'queue_encoded', 'Operator', 'T2', 'holdCount',
                      'connectedDuration']
RF_FEATURE_IMP = ['agent_encoded', 'origin_encoded', 'holdDuration', 'team_encoded', 'holdCount', 'skillDiff',
                  'queue_encoded', 'connectedDuration'] if DATA_SOURCE == 'prod/467dcff4-6c01-4615-afd3-c2b83f53e969' else ['origin_encoded', 'agent_encoded', 'holdDuration', 'holdCount', 'team_encoded', 'queue_encoded', 'connectedDuration']
