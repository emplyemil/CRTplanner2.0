import requests
import streamlit as st
from modules.json_parser import parse_onboarding

isTestRun = False

AREA_ID = st.secrets["area_id" if not isTestRun else "test_area_id"]
PIPELINE_ID = st.secrets["pipeline_id" if not isTestRun else "test_pipeline_id"]
BATCH_URL = st.secrets["batch_url" if not isTestRun else "test_batch_url"]

stage_ids = [
    (st.secrets["stage1_id"], "Handover"),
    (st.secrets["stage2_id"], "CR Team"),
    (st.secrets["stage3_id"], "Kick off"),
    (st.secrets["stage4_id"], "Recruitment"),
    (st.secrets["stage5_id"], "Employees"),
    (st.secrets["stage6_id"], "Onboarding"),
    (st.secrets["stage7_id"], "Feedback and goals"),
    (st.secrets["stage8_id"], "Learning and job profiles"),
    (st.secrets["stage9_id"], "Training"),
    (st.secrets["stage10_id"], "Final session"),
    (st.secrets["stage11_id"], "Delivery Date")
]

API_KEY = st.secrets["api_key"]
FORM_ID = st.secrets["form_id"]
INSTANCE = st.secrets["instance"]

if isTestRun:
    stages = [(st.secrets["test_stage_id"], "Test Stage")]
else:
    stages = stage_ids

def make_webrequest(cookies, stageId):
    xsrf_token = next((cookie['value'] for cookie in cookies if cookie['name'] == 'XSRF-TOKEN'), None)
    cookies_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Xsrf-Token': xsrf_token,
        'Cookie': cookies_string,
    }

    payload = {
        "middlePipelineStages": False,
        "onboardingAreaId": AREA_ID,
        "onboardingPipelineId": PIPELINE_ID,
        "pipelineStageId": stageId,
        "searchCriterias": [],
        "searchText": None,
        "skip": 0,
        "take": 15,
    }

    response = requests.post(BATCH_URL, headers=headers, json=payload, verify=False)
    if response.status_code == 200:
        data = response.json()
        # Assuming 'data' is a list of dictionaries with 'firstName' and 'id'
        customers = [(entry['firstName'], entry['id']) for entry in data]
        return customers
    else:
        return []  # Return an empty list in case of an error
    

def get_stages(cookies):
    results = []
    for stage_id, stage_name in stage_ids:
        customers = make_webrequest(cookies, stage_id)
        for customer in customers:
            firstName, customerID = customer
            results.append((stage_name, firstName, customerID))
    return results

def make_APIrequest(url, method='GET'):
    try:
        return requests.get(url)
    except Exception as e:
        print(f'Retrying request...')
        make_APIrequest(url, method)

def get_full_onboarding(args):
    onboarding_id, stage = args
    url = f'https://api.emply.com/v1/{INSTANCE}/onboardings/{onboarding_id}/form-data/{FORM_ID}?apiKey={API_KEY}'
    response = make_APIrequest(url)
    onboarding_data = parse_onboarding(response.json(), stage)
    return onboarding_data