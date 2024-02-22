from datetime import datetime, timedelta

def create_months_for_overview():
    #create a list of months for the next 12 months
    months = {}
    current_month = datetime.now().replace(day=1)
    for i in range(13):
        months[current_month.strftime("%m-%Y")] = []
        current_month = current_month.replace(day=1)
        current_month += timedelta(days=31)
    return months

def add_onboardings_to_months(months, onboarding_list):
    #Add onboarding to the correct month
    for onboarding in onboarding_list:
        if onboarding.months is not None:
            for month in onboarding.months:
                if month.strftime("%m-%Y") in months:
                    months[month.strftime("%m-%Y")].append(onboarding)
    return months


def create_list_of_employees(months):
    employees = []
    for month in months:
        for onboarding in months[month]:
            if onboarding.cr_agent is not None:
                employees.append(onboarding.cr_agent)
            if onboarding.cr_agent2 is not None:
                employees.append(onboarding.cr_agent2)
    return list(set(employees))