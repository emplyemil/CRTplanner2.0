import pandas as pd

def count_tasks_in_month(month, employee):
    count = 0.0
    for onboarding in month:
        if onboarding.cr_agent is not None and onboarding.cr_agent == employee:
            count += 1.0
        if onboarding.cr_agent2 is not None and onboarding.cr_agent2 == employee:
            count += 0.5
    return count

def create_dataframe(months, employee_list):
    #Create pandas dataframe where first row is months and first column is employees
    df = pd.DataFrame(index=employee_list, columns=months.keys())

    #Fill dataframe with number of tasks per month
    for month in months:
        for employee in employee_list:
            df.loc[employee, month] = count_tasks_in_month(months[month], employee)
            
    #Sum of tasks per month in last row
    df.loc['Total tasks per month'] = df.sum()

    return df

def create_onboarding_dataframe(list):
    customers = []
    for onboarding in list:
        customers.append(onboarding.customer_name)
    
    df = pd.DataFrame(index=customers,columns=['CR Agent', '2nd CR Agent', 'Start Date', 'End Date', 'Stage'])

    for onboard in list:
        customer = onboard.customer_name
        df.loc[customer, 'Stage'] = onboard.stage
        df.loc[customer, 'Start Date'] = "not defined"
        df.loc[customer, 'End Date'] = "not defined"
        if onboard.start_date is not None:
            df.loc[customer, 'Start Date'] = onboard.start_date.strftime('%d-%m-%Y')
        if onboard.end_date is not None:
            df.loc[customer, 'End Date'] = onboard.end_date.strftime('%d-%m-%Y')
            
        df.loc[customer, 'CR Agent'] = ""
        df.loc[customer, '2nd CR Agent'] = ""
        if onboard.cr_agent is not None:
            df.loc[customer, 'CR Agent'] = onboard.cr_agent.firstname + " " + onboard.cr_agent.lastname[0] + "."
        if onboard.cr_agent2 is not None:
            df.loc[customer, '2nd CR Agent'] = onboard.cr_agent2.firstname + " " + onboard.cr_agent2.lastname[0] + "."

    return df

def export_to_excel(df, df2, file_name='crt-planner'):
    #Create excel file
    excel_file = f'{file_name}.xlsx'
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    #Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Overview')
    df2.to_excel(writer, sheet_name='Month Planner')

    #Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Overview'].set_column(col_idx, col_idx, column_width)

    #Close the Pandas Excel writer and output the Excel file.
    writer.close()

    return excel_file