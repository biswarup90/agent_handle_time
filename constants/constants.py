SOURCE = 'lion_king'
NOT_NULL = ['connectedCount', 'connectedDuration', 'agent', 'Queue', ] if SOURCE == 'maersk' else []
OUTLIER_COLS = ['connectedDuration', 'holdDuration', 'queueDuration', 'ringingDuration', 'IVRDuration'] if SOURCE == 'maersk' else ['connectedDuration']
IMPUTER = {"skill": "Blank"} if SOURCE == 'maersk' else {"contactReason": "Blank", "selfserviceCount": 0,
                                                         "selfserviceDuration": 0, "rs": "Blank", "ms": "Blank",
                                                         "routingType": "Blank"}
DROP_COLS_IMPUTER = ['id', 'Contact Reason', 'Sub Channel Type', 'Skills', 'Connected Duration', 'Hold Duration',
                     'Queue Duration',
                     'Ringing Duration', 'IVR Duration', 'End Time', 'Channel Type'] if SOURCE == 'maersk' else [
    'matchedSkills', 'id', 'endedTime', 'connectedCount', 'requiredSkills', 'lastQueue', 'contributors', 'ms', 'lastTeam']
TARGET_ENCODING_COLS = ['origin', 'Queue', 'agent', 'skill', 'team'] if SOURCE == 'maersk' else ['origin', 'queue',
                                                                                                 'agent', 'destination', 'team']
Y = 'connectedDuration'
OHE_COLS = ['destination'] if SOURCE == 'maersk' else ['contactReason', 'channelSubType', 'contactReason',
                                                       'isHandledByPreferredAgent', 'channelType', 'routingType']
DROP_COLS_ENCODER = ['origin', 'destination', 'agent', 'skill', 'Queue', 'Team'] if SOURCE == 'maersk' else ['origin',
                                                                                                             'destination',
                                                                                                             'queue',
                                                                                                             'agent',
                                                                                                             'channelSubType',
                                                                                                             'contactReason',
                                                                                                             'channelType',
                                                                                                             'isHandledByPreferredAgent',
                                                                                                             'routingType', 'team']
TOP_COLS = ['connectedDuration', 'agent_encoded',
            'origin_encoded', 'skill_encoded',
            'queue_encoded', 'team_encoded'] if SOURCE == 'maersk' else ['connectedDuration', 'agent_encoded',
                                                                         'origin_encoded', 'destination_encoded',
                                                                         'queue_encoded', 'channelType_telephony', 'channelType_email', 'channelType_chat']
BOX_COX_LAMBDA = 0.6