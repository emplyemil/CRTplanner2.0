from jsonpath_ng import parse
from modules.employee_class import Employee
from modules.onboarding_class import Onboarding

def json_parser(selector, source):
    jsonpath_expression = parse(selector)
    for match in jsonpath_expression.find(source):
        return match.value

def parse_employee(employee_json):
    firstname = json_parser('relations[0].user.firstName', employee_json)
    lastname = json_parser('relations[0].user.lastName', employee_json)
    email = json_parser('relations[0].user.email', employee_json)
    if email == None:
        return None
    employee = Employee(firstname, lastname, email)
    return employee

def parse_onboarding(onboarding_json, stage):
    onboarding_id = json_parser('[0].id', onboarding_json)
    name = json_parser('[0].text', onboarding_json)
    solution = json_parser('[1].relations[0].department.title', onboarding_json)
    partner = json_parser('[2].options[0].optionTitle.localization[0].value', onboarding_json)
    start_date = json_parser('[3].date', onboarding_json)
    end_date = json_parser('[3].date2', onboarding_json)
    cr_agent = parse_employee(onboarding_json[4])
    cr_agent_two = parse_employee(onboarding_json[5])

    onboarding = Onboarding(onboarding_id, name, solution, partner, start_date, end_date, cr_agent, cr_agent_two, stage)
    return onboarding