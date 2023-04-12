import requests
import json
import sys
import datetime
import calendar
import time
import traceback
from os.path import exists
import os
from requests.exceptions import HTTPError

dc = "prodanz1"
log_file_name = f"analysis_summary_{dc}.log"
# log_file_name = "check.log"

# Helpdesk Token (Taken from browser network tab)
auth_token = "Bearer eyJhbGciOiJSUzI1NiJ9.eyJjbHVzdGVyIjoiUEY4NCIsInByaXZhdGUiOiJleUpqZEhraU9pSktWMVFpTENKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVpHbHlJbjAuLnZDZDVWNkxlbzVmcHdiWTNzRGhsdmcuaHlOUmZhN3Y2SlFucGVBS2ZJa1EtLTFsYmduSFkzenA2RGtUSGdjVzZTX01NaU5YV1dZamFWaXZ4alh1R25xbDdJTnpVdlNNWjNwR1lCUWJjbzNFaUNGZ3pITVgydmNsUW40MjZvLXBxU2NUWVo5ZjRRS2UtQUdHczFmdVhoU2lPV2xCbTBQa1UzRlNlSnd4azlLY2tKUG1iR18yMUpJQmZ1LXU1ZmZZMVc4RmxTa2JMcmVOeUloWlNKM2RBMXhaMGoyaHNBRFlMOW1UYzhnSEM1QVpFdWRvOVhKVUwxSldFWGZ6NUwtRFdSZ2tFOXcxSXZ3aDVJZFVYQjY5eVJLak0wYUtabC15N0hOTXkxeV9LVHVzRjBuT0x1d3M5ZFZKbUVrOU9HRVFsb3FwRmc2NXI0ektuS3VHQzJ6OUZHcTNOVnZzcTFUeEV1Ymt0dVNrc1p3RFRxc1ZPNVhDbVBKU3Nnci1feWRoTzVSRWhseU9YbUFMSVNxdmVVNW9iZGVTT2JKM2xRVW5aNTZxdjIzd2IxbElXYUtSVWhheGI0bDVOaXhNeW9XVDFVR1ZsUHY0UjdrOXFJYTZFVUdlWWJBZ0F6WmFxcFJnZGMyajFOcWlBeXNvMkpyeUduaml2UmhKblFYU2VXVFZOVTJyemVXY0hneFNZejc0TE1wNnBKRlF3YmRuM01fd2FmQlhoOTZ5QWVMT0d0ZExWSUE4aFVZYmNKd0ZJYVhtVGJqT0tVZE1fbE02M0F5c2F3dUpBOVlUZGRIaWxDczh2ckswOGo5OHhSc3AxN2VuN1FhMXA3YkNSc05aLWljXy1fT2EtWVdIMDh1dXZyLVRrNEJ3RWRiSkgtN2tqZzNZcWgwN1dqbGZaRmp3bVY5TV9pd2dwdTg4bjhBWW1pb3ltSXctTWhFdHVDZGZuSFY2NFlwNWc0SlpzTkdneXpHcGFFcEV0UVlYaFExSzI2RTh1VElUOXFxYjNFdUdXTnVFM1lRS0pQQ3JEZkJMTVZubzYtRUxjanl3ZnZVM2lpSUdmNkhVTVdQTlF1Z0tOS2dGUE5qbWlWeW1sRjVHUFJTWXRNRHlBbHNSYkFnUW5DQkdieFBQQlg2VDBKdmZDT2tlYTBfcGVrZ1NqOTVSdXh0MVM0SFM3c0w5U2xQTTMwUXMxZW9pa3hPOF9OYW5IVGVmNGtNbmluTWlLT0VKYzdrR0NFUE4xYUhpSUdTV0xIajB1elViV2EybVVPYXRtN0tGd2ZoU0lTSW90cUVrdE93dFZIRGkxYnhLWDctZTVqZ3JuM3B6dVpLM1VPeTZJdy5LVWhTeFJzWE5QdGQzZTJ5dmdQcS1nIiwidXNlcl90eXBlIjoidXNlciIsInRva2VuX2lkIjoiQWFaM3IwWWpoaE9UUm1OalV0WmpJNE55MDBNV0kyTFdFek1qTXRaV05pTXpZeE9HUmhObVJpTkRCbU16ZzNabVF0TmpaaCIsInJlZmVyZW5jZV9pZCI6ImExNTkwM2E0LWRkZDItNGVkNC04ODEwLTZhODhiMDI1NDYyOSIsImlzcyI6Imh0dHBzOlwvXC9pZGJyb2tlci53ZWJleC5jb21cL2lkYiIsInVzZXJfbW9kaWZ5X3RpbWVzdGFtcCI6IjIwMjIwOTE3MDA1NTAxLjIxN1oiLCJyZWFsbSI6IjFlYjY1ZmRmLTk2NDMtNDE3Zi05OTc0LWFkNzJjYWUwZTEwZiIsImNpc191dWlkIjoiOTVjNDUxZGQtMzhhZC00NjE2LWI4YTEtZmQ0OGY4NThjNjcxIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImV4cGlyeV90aW1lIjoxNjc4NzU3MDIwMjk2LCJjbGllbnRfaWQiOiJDYTQzYTA3NWU5YmIzMzFhMTMxY2RjMmM4YzM3ZmVhMGRhODI0NDcxZWE1MDIwYjIwNWQzMGUyZDI5NWU4ZTlkNSJ9.FvHo4OfXbnGNWz5Mee0XHBgr4Lwy-NQoSNuXEBy0HHZpmFJMC-xrAbXn6q3pBEsa6MUwPAWXJ7b7JYDXAZqi2a5m1FrEsXnW8poYeISbMYZpPU0Cow6ZBJ2PcktPzQTtUFDue2fKf57dEA63ugD-EeeY0b_QqxQnWWDECId1kb7Gt6N9n_F89IL2fa7wp2E7p-C-Ov1WR17X3B0HI5_RPJY3Q3alMH5Jy9R4RS9dsOnVleCOJxq-4uxnC02zFXldQShspaWaPWwXJkyye_jy_awdMKOz3PAlaC4V7CXk7qY655K-r2-ia2VPRdyDlmM64yl_76PaRQmn_ggfvtNsgw"
headers = {"Content-Type": "application/json", 'Authorization': auth_token}
mediaMap = {'telephony': 'vmm', 'chat': 'cmm', 'social': 'digitalmm', 'email': 'emm'}


def compute_old_epoch_time(totalDays):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days=totalDays)
    a = tod - d
    epoch_time = (calendar.timegm(a.timetuple()))
    return epoch_time * 1000


# Define age for stuck interactions according to media type
telephony_stuck_interation_max_age = compute_old_epoch_time(14)


def toDate(timestampMillis):
    return datetime.datetime.fromtimestamp(timestampMillis / 1000)


def toTimestamp(dateStr):
    return int(datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)


def log(line):
    try:
        log_file = open(log_file_name, "a")
        now = datetime.datetime.now()
        logLine = now.strftime('%Y-%m-%d %H:%M:%S ') + line + "\n"
        log_file.write(logLine)
        print(logLine)
        log_file.close()
    except Exception as err:
        print(f'Error occurred while writing to log file: {err}')
        sys.exit()


def joinLines(value):
    return ''.join(value.splitlines())


def getFileName(intr, org, suffix):
    return org + os.sep + intr + "_" + suffix + ".json"


def getFileData(fileName):
    if exists(fileName):
        fileHandle = open(fileName, "r")
        data = fileHandle.read()
        fileHandle.close
        return data
    else:
        return None


def writeToFile(dirName, fileName, content):
    try:
        if (not exists(dirName)):
            os.mkdir(dirName)
        file_h = open(fileName, "w")
        file_h.write(content)
        file_h.close()
    except Exception as err:
        print(f'Error occurred while writing to file: {fileName} - {err}')
        sys.exit()


def getLadderLog(intr, org):
    fileName = getFileName(intr, org, "ladder")
    ladderLogFromFile = getFileData(fileName)
    if ladderLogFromFile != None:
        if ladderLogFromFile == "":
            return None
        else:
            # log (f"ladder log from file {ladderLogFromFile}")
            return ladderLogFromFile

    log("Making API Call for Ladder Log")

    url = f"https://core-helpdesk-bff.{dc}.ciscoccservice.com/core-helpdesk/v1/ladderLogs"

    try:
        headers_addl = {"X-ORGANIZATION-ID": org}
        headers_addl.update(headers)
        params = {"interactionId": intr}
        response = requests.get(url, params=params, headers=headers_addl)

        if (response.status_code != 200):
            log(f'ERROR {str(response.status_code)} response. Failed to get interaction {intr}.')
            return None
        else:
            jsonResponse = json.loads(response.text)
            # log(f'{intr}-LadderLog: {jsonResponse}')
            if len(jsonResponse["logs"]) == 0:
                # log("No Ladder Log")
                writeToFile(org, fileName, "")
                return None
            else:
                # log("Ladder Log exists - " + str(len(jsonResponse["logs"])))
                writeToFile(org, fileName, response.text)
                return response.text

    except HTTPError as http_err:
        log(f'ERROR HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        log(f'ERROR unexpected error occurred: {err}')
        return None


def getInteractionInfo(org, intr):
    fileName = getFileName(intr, org, 'detail')
    interactionData = getFileData(fileName)
    if interactionData != None:
        if interactionData == "":
            return None
        else:
            # log (f"interaction detail from file {interactionData}")
            return json.loads(interactionData)

    url = f"https://ur.{dc}.ciscoccservice.com/ur/v1/interaction/{intr}"

    try:
        headers_addl = {"X-ORGANIZATION-ID": org}
        headers_addl.update(headers)
        params = {"interactionId": intr}
        response = requests.get(url, params=params, headers=headers_addl)

        if (response.status_code != 200):
            log(f'ERROR {str(response.status_code)} response. Failed to get interaction {intr}.')
            writeToFile(org, fileName, "")
            return None
        else:
            jsonResponse = json.loads(response.text)
            writeToFile(org, fileName, response.text)
            # log(f'{intr}-detail: {jsonResponse}')
            return jsonResponse

    except HTTPError as http_err:
        log(f'ERROR HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        log(f'ERROR unexpected error occurred: {err}')
        return None


def analyzeInteraction(intrDetail, intr, org, mediaType, timeFull):
    # log(f'To analyze interaction {intr}. Created on {timeFull} - {intrDetail}')
    return getLadderLog(intr, org)


def analyzeInteraction2(org, intr, aggregatedResults):
    ladderLog = getLadderLog(intr, org)
    intrDetail = getInteractionInfo(org, intr)
    state = None
    flowName = None
    contactDeleteFound = False
    contactEndedFound = False
    conversationEndedFound = False
    wrapupApplicable = False
    agentWrappedUp = None
    analysisSummary = ''
    investigationSG = 'CORE'
    createdTime = None
    if ladderLog:
        if ladderLog.find('vmm->>ur: ConversationEnded') > 0:
            conversationEndedFound = True
        else:
            analysisSummary += 'VMM did not send conversation ended. '
            investigationSG = 'VMM'

        if ladderLog.find('flowcontrol->>ur: ContactDelete') > 0:
            contactDeleteFound = True
        else:
            analysisSummary += 'Flow did not send contact delete. '

        if ladderLog.find('flowcontrol->>ur: FCR(ContactEnded)') > 0:
            contactEndedFound = True
        if ladderLog.find('flowcontrol->>ur: FCR(AgentWrapup)') > 0:
            wrapupApplicable = True
            if ladderLog.find('flowcontrol->>ur: FCR(AgentWrappedUp)') > 0:
                agentWrappedUp = True
                analysisSummary += 'Agent did wrapped up. '
            else:
                agentWrappedUp = False
                investigationSG = 'NA'
                analysisSummary += 'Agent did not wrap up. '

    else:
        contactDeleteFound = contactEndedFound = wrapupApplicable = None
        analysisSummary += 'Ladder log not found. '
        investigationSG = 'NA'

    if (intrDetail):
        state = intrDetail['state']
        if (intrDetail['isFcManaged'] == True):
            flowName = intrDetail['callProcessingDetails']['workflowName']
        else:
            flowName = 'Not_FC_Managed'
        if intrDetail['createdTimestamp'] == None:
            createdTime = ""
        else:
            createdTime = toDate(intrDetail['createdTimestamp']).strftime('%d-%b-%Y %H:%M:%S')

    else:
        analysisSummary += 'Interaction detail not found from UR. '

    aggregatedResults[intr] = {'Interaction': intr, 'Created Time': createdTime, 'State': state,
                           'Next level investigation': investigationSG,
                           'Analysis Summary': analysisSummary, 'ContactDelete Found': contactDeleteFound,
                           'ContactEnded Found': contactEndedFound, 'conversationEnded Found': conversationEndedFound,
                           'Wrapup Applicable': wrapupApplicable, 'Wrapup Done': agentWrappedUp, 'Flow Name': flowName}

    log(f'Analysis of interaction {intr} => {aggregatedResults[intr]}')


def get_interactions_by_org_aqm(org):
    api_url = f"https://aqm.{dc}.ciscoccservice.com/aqm/v1/organization/{org}/contact"

    headers_addl = {"x-organization-Id": org}
    headers_addl.update(headers)
    oldInteractionsCount = 0

    try:
        response = requests.get(api_url, headers=headers_addl)

        if (response.status_code != 200):
            log(f'ERROR {str(response.status_code)} response. Failed to load interactions for {org}.')
            return 0
        else:
            log(f'SUCCESS 200 response for retrieving all active contacts for org {org}')
            jsonResponse = json.loads(response.text)
            totalInteractions = len(jsonResponse)
            for intrObj in jsonResponse:
                timeFull = intrObj["createdTimestamp"]
                timestamp = toTimestamp(timeFull)
                oldInteraction = False
                if (intrObj["mediaType"] == "telephony" and timestamp < telephony_stuck_interation_max_age):
                    oldInteraction = True
                # elif (intrObj["mediaType"] == "chat" and timestamp < chat_social_old_record_delete_ts) :
                #     oldInteraction = True
                # elif (intrObj["mediaType"] == "email" and timestamp < email_old_record_delete_ts) :
                #     oldInteraction = True
                # elif (intrObj["mediaType"] == "social" and timestamp < chat_social_old_record_delete_ts) :
                #     oldInteraction = True

                if (oldInteraction):
                    analysisOk = analyzeInteraction(intrObj, intrObj["interactionId"], org, intrObj["mediaType"],
                                                    timeFull)
                    #                 log(f'Interaction: {intrObj["interactionId"]}, timeFull: {timeFull}, timestamp: {timestamp}, \
                    # timeFullAgain: {toDate(timestamp)}, mediaType: {intrObj["mediaType"]}, deleteStatus ? {deleteOk}')
                    if analysisOk:
                        oldInteractionsCount += 1
                        break  # DONT CONTINUE - CHECK THE SINGLE INTERACTION

            log(f"{oldInteractionsCount} interactions out of total {totalInteractions} active interactions were analyzed")
            return oldInteractionsCount


    except HTTPError as http_err:
        log(f'ERROR HTTP error occurred: {http_err}')
        return 0
    except Exception as err:
        log(f'ERROR unexpected error occurred: {err}')
        return 0


def analyzeInteractionsInAQMStore():
    totalInteractionsProcessed = 0
    with  open("orgs.txt", "r") as file1:
        total_orgs = len(file1.readlines())
        file1.seek(0)
        total = 1
        for org_id in file1:
            org = org_id.strip()
            log(f"{total} out of {total_orgs} orgs. Analyzing interactions in ORG {org}...")
            totalInteractionsProcessed += get_interactions_by_org_aqm(org)
            total += 1
    log(f"{totalInteractionsProcessed} stuck interactions had been processed across all orgs")


def logResultsToCsv(orgId, results):
    csvFileName = f'AnlysisSummary-Org-{orgId}.csv'
    try:

        csvFile = open(csvFileName, "w")
        isFirst = True
        headerRow = ''

        for interaction in results:
            rowData = ''
            for key in results[interaction]:
                if (isFirst):
                    headerRow += key + ', '
                rowData += str(results[interaction][key]) + ', '

            if (isFirst):
                csvFile.write(headerRow + '\n')
                isFirst = False

            csvFile.write(f"{rowData}\n")

        csvFile.close()
        log(f"Interaction analysis written to csv file {csvFileName}")
    except Exception as err:
        log(f'ERROR unexpected error occurred: {err}')
        traceback.print_exc()


# CSV file of interactions
def analyzeInteractionsFetchedFromURStore():
    totalInteractionsProcessed = 0
    orgId = "b053b74b-d73e-4a19-9e02-bc4f6641949c"
    results = {}
    count = 0
    log(f"Analyzing interactions for org {orgId}")
    with  open("interactions.csv", "r") as file1:
        interactions = file1.read().split(", ")
        log(f'Total interactions: {len(interactions)}')
        for interaction in interactions:
            analyzeInteraction2(orgId, interaction.strip(), results)
            count = count + 1
            if count == 1:
                exit(0)

    logResultsToCsv(orgId, results)
    # log (f'agg => {results}')


log("")
log("INTERACTION ANALYSIS STARTED")

# analyzeInteractionsInAQMStore()
analyzeInteractionsFetchedFromURStore()

log("INTERACTION ANALYSIS COMPLETE")