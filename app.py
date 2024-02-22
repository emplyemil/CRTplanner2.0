from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer as timer

import modules.cookie_scrapper as cookie_scrapper
import modules.requests as RequestAPI
import modules.data_processing as processing
import modules.create_dataframes as dataframes

#Only enable this for debugging purposes
DEBUGGING=False

def _multithreading(func, args, workers=5):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

def get_data():
    # retrieve session cookie by login on crt.emply.com
    cookies = cookie_scrapper.get_cookie()
    # make web request to get all the stages with customer
    customer_stage_list = RequestAPI.get_stages(cookies)
    # takes ids and stage names
    onboarding_args = [(entry[2], entry[0]) for entry in customer_stage_list]

    onboarding_list = _multithreading(RequestAPI.get_full_onboarding, onboarding_args)

    months = processing.create_months_for_overview()
    months_onboarding = processing.add_onboardings_to_months(months, onboarding_list)

    employee_list = processing.create_list_of_employees(months_onboarding)

    df = dataframes.create_onboarding_dataframe(onboarding_list)
    df2 = dataframes.create_dataframe(months_onboarding, employee_list)

    return df, df2, dataframes.export_to_excel(df,df2)


def run_application():
    #Start of program
    if DEBUGGING:
        start = timer()
    
    get_data()

    if DEBUGGING:
        end = timer()
        print("Elapsed time: " + str(timedelta(seconds=end-start)))



run_application()