import json
from datetime import datetime, timedelta

class Onboarding:
    def __init__(self, id, customer_name, solution, partner, start_date, end_date, cr_agent, cr_agent2, stage):
        self.id = id
        self.customer_name = customer_name
        self.solution = solution
        self.partner = partner
        self.stage = stage
        if start_date is not None:
            self.start_date = string_to_date(start_date)
        else:
            self.start_date = None
        if end_date is not None:
            self.end_date = string_to_date(end_date)
        else:
            self.end_date = None
        self.cr_agent = cr_agent
        self.cr_agent2 = cr_agent2
        self.months = self.get_working_months()

    def get_working_months(self):
        #Get months between start and end date
        if self.start_date is None or self.end_date is None:
            return None
        months = []
        current_month = self.start_date
        while current_month <= self.end_date:
            months.append(current_month)
            current_month = current_month.replace(day=1)
            current_month += timedelta(days=31)
        return months

    def __str__(self):
        return f'{self.customer_name} - {self.stage} - {self.months} - {self.cr_agent} and {self.cr_agent2}'

    def __eq__(self, other):
        return self.id == other.id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    

def string_to_date(date_string):
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')