import requests
import json
import sys
import datetime
import calendar
from requests.exceptions import HTTPError


def compute_old_epoch_time(totalDays):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days=totalDays)
    a = tod - d
    epoch_time = (calendar.timegm(a.timetuple()))
    return epoch_time * 1000


# Token
auth_token = "eyJhbGciOiJSUzI1NiJ9.eyJjbHVzdGVyIjoiUEY4NCIsInByaXZhdGUiOiJleUpqZEhraU9pSktWMVFpTENKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVpHbHlJbjAuLjBLOHFTbFlCWU9HWTJTT1NRZHRtQ1EuTWZfMzh4Tmo2UTNsTFRSOGlFdnBqeHl2ZkVlN0ZkMzl4NWpwUDZROUQydkpiWGJNdVRkMDczeGU5bk1Td2JWNXctcl8yWTBwQVBZTFRhYkRnU1JfLXdsU2JmSHEwbHQwYmE0TkpqTVZfMVlUVks0UGhDaVJxR1BLNEZ5aVdsUXlJSjd1NWJPT0lXS1hobmltbi11QzhXdUtLM3ljaEdndGMxSXowaTRURk9uSFlNWDl6OENKNF9oRDROY3RxSURoWTFoUnE2djA3QS1Nak8yUVJqd21FR1k5SzI5U2VTTnhER1JaR2NrYXJPU20ycmJCSldvZ01LTHRGU1E1SVNvM1VoZVBybkF5LVBHRldLbmI3b1lLY1lUYl9EV0hjakpqdExHeVozX1ZPOVFBWXRuV1J2d0M5OHZpRi1SYjd1aVBSdVJlRTktSWxWNGJhdXpFLXBXQ2taM3NXTGR3eDdtb2VwVDVNZDJWZEVTTUlSSDZEOUtUeTNMWU54WHZVeDNqdDZUNzk1NnIyNXdSU19jVWh4bVJHM3VWS2NubnM1RjJaZXR5RnZmdVdSY3pqYktMbGNfeTEtaUJkdjdTNmxWTEdoTm9BcUpTU2NKYk9tMFFxa1RNSUlFY1loc3I2ajBXYlVWY19VUTkxM0tYVGx3UmlOUlJJYjQ5QnliWkU4dVouMU1iNzVxMWRheDBOdDc5T01lYlk0QSIsInVzZXJfdHlwZSI6InVzZXIiLCJ0b2tlbl9pZCI6IkFhWjNyME5UUXpaamcwWW1JdE5qRTJOQzAwWXpVeUxXRmtNbU10T0dVeE4yVTJNVE0zTURRNE1EQmhZbU01WWpjdE5EazAiLCJyZWZlcmVuY2VfaWQiOiJjZjc5NjBmOS04MWEzLTQ3YzEtOGI0ZC1kYjRkZjEwNDIzN2MiLCJpc3MiOiJodHRwczpcL1wvaWRicm9rZXIud2ViZXguY29tXC9pZGIiLCJ1c2VyX21vZGlmeV90aW1lc3RhbXAiOiIyMDIyMDYyMjA1MzkyNy4xOTdaIiwicmVhbG0iOiJjMWU1OTI1OC0yOWUxLTQyZDctYmZhNy04NGFiMjY2MzJiNDYiLCJjaXNfdXVpZCI6IjE4OTQwZWIwLTg3ZWYtNDk4NC1hMTViLTFjMDI4NDQ5ODdkNSIsInRva2VuX3R5cGUiOiJCZWFyZXIiLCJleHBpcnlfdGltZSI6MTY3Mzk5NTcyNTAzMCwiY2xpZW50X2lkIjoiQ2E0M2EwNzVlOWJiMzMxYTEzMWNkYzJjOGMzN2ZlYTBkYTgyNDQ3MWVhNTAyMGIyMDVkMzBlMmQyOTVlOGU5ZDUifQ.Tc7bx6JxwY319dmq0I7Pfd2yuqvAAl0vqa1R5GLGPlf9l5qFFrGKoQnxQSg2BiRGbkcLY1i2r--1lS83__doN0XhCK4IfeAwKzk3aFvXETkhs8LSclUnrQB1Q0AG7HHtvKejIW8BXsR_Betj4MAwiQUa0zXtj0OiK4bvBvogFAwTvuZ6ibve15qp-LcKphw2t3DPwUnz8m8_CljMnR-AwMBLn2BGE5Q2DUQtdXbtpxunHMAJSm557YufB43mtcjLfXLi7_xTOWwsNWxMpPyxMeCSKCwsIu7MXMKY8t8aVmCxQXnjBwE4sMP3ai-M7COiqYE-B6gDbKfuO_xEEd12YA"

# Define age for deletion according to media type
telephony_old_record_delete_ts = compute_old_epoch_time(14)
chat_social_old_record_delete_ts = compute_old_epoch_time(14)
email_old_record_delete_ts = compute_old_epoch_time(60)

print(
    f'Epoch time for deletion. Telephony {telephony_old_record_delete_ts}, Chat {chat_social_old_record_delete_ts}, Email {email_old_record_delete_ts}')

headers = {"Content-Type": "application/json", 'Authorization': 'Bearer ' + auth_token}


def log(line):
    try:
        log_file = open("cleanup_summary.txt", "a")
        log_file.write(line + "\n")
        log_file.close()
    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit()


def cleanup_org_interactions(org, media_type, media_manager, timestamp):
    api_url = "https://core-helpdesk-bff.produs1.ciscoccservice.com/core-helpdesk/v1/kafkaCleanup"
    payload = {
        'orgId': org,
        'topic': 'ur-msgStream-InteractionStateStore-changelog',
        'timestamp': timestamp,
        'mediaType': media_type,
        'mediaManager': media_manager
    }

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        print('Cleanup response status code: ' + str(response.status_code))

        if (response.status_code != 200):
            print('Error Failed to do interaction cleanup for org ' + org)
            sys.exit(0)

        print('Response json: ' + response.text)
        log(f'Cleanup of {org} and {media_type} result: {response.text}')


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        sys.exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit()


def cleanup_org(org):
    api_url = "https://core-helpdesk-bff.produs1.ciscoccservice.com/core-helpdesk/v1/active-records"
    print("Getting active interactions for org " + org)

    payload = {
        'orgId': org,
        'topic': 'ur-msgStream-InteractionStateStore-changelog',
        'timestamp': telephony_old_record_delete_ts
    }

    # write_file_name = org + '_interactions.txt'

    # try:
    #     response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    # except HTTPError as http_err:
    #     print(f'HTTP error occurred: {http_err}')
    #     sys.exit()
    # except Exception as err:
    #     print(f'Other error occurred: {err}')
    #     sys.exit()
    # print ("Saving interactions to file ")
    # interactions_file = open(write_file_name, "w")
    # intFileData = json.dumps(response.json())
    # interactions_file.write(intFileData)
    # interactions_file.close()

    # intFile =  open(write_file_name, "r")
    # intFileData = json.load(intFile)

    # if len(intFileData["data"]) > 0:
    #     print('interactions count for org ' + org + ' is ' + str( len(intFileData["data"] )) )

    print('deleteing voice interactions...')
    cleanup_org_interactions(org, 'telephony', 'vmm', telephony_old_record_delete_ts)
    print('deleteing chat interactions...')
    cleanup_org_interactions(org, 'chat', 'cmm', chat_social_old_record_delete_ts)
    print('deleteing social interactions...')
    cleanup_org_interactions(org, 'social', 'digitalmm', chat_social_old_record_delete_ts)
    print('deleteing email interactions...')
    cleanup_org_interactions(org, 'email', 'emm', email_old_record_delete_ts)


with  open("orgs.txt", "r") as file1:
    total_orgs = len(file1.readlines())
    file1.seek(0)
    total = 1
    for org_id in file1:
        print(f"Cleanup {total} out of {total_orgs}")
        cleanup_org(org_id.strip())
        total += 1
        #break