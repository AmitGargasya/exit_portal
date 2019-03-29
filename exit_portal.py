from exit_portal.utils import read_json_file, send_mail, employee_leaving_data
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from exit_portal.exit_portal import declaration_form
from exit_portal.hr_approval_page import hr_approval


def user_validation(emailId, password):

    try:
        pwd = read_json_file("{emailId}".format(emailId=emailId), "password")
        if pwd == password:
            valid_code = 1
        else:
            valid_code = 0
        return valid_code

    except Exception as e:
        raise e


def hr(emailId, password):
    try:
        valid_code = user_validation(emailId, password)
        hr_emp_id = ''
        hr_name = ''
        if valid_code == 1:
            employeeCode = ''
            with open('Employee.txt') as json_file:
                json_data = json.load(json_file)
            for json_obj in json_data:
                employeeCode = json_obj['employeeCode']
                hr_emp_id = json_obj['empId']
                hr_first_nm = json_obj['firstName']
                hr_last_nm = json_obj['lastName']
                hr_name = hr_first_nm + ' ' + hr_last_nm
            if employeeCode == "HR":
                    from_sender = read_json_file("from_sender", "config")
                    with open('Exit_employee.txt', 'r') as infile:
                        try:
                            data = infile.read().replace('][', ',')
                            exit_emp = json.loads(data)
                            infile.close()

                        except ValueError:
                            exit_emp = []

                        print(exit_emp)
                        if len(exit_emp) != 0:
                            for emp in exit_emp:
                                manager_emp_id = emp['manager_emp_id']
                                hr_emp_id = emp['hr_emp_id']
                                emp_first_nm = emp['firstName']
                                emp_last_nm = emp['lastName']
                                emp_id = emp['empId']
                                personal_email_id = emp['personal_emailId']
                                jobTitleName = emp['jobTitleName']
                                employeeCode = emp['employeeCode']
                                region = emp['region']
                                DOJ = emp['DOJ']
                                DOL = emp['DOL']
                                phoneNumber = emp['phoneNumber']

                                emp_name = emp_first_nm + ' ' + emp_last_nm
                                if emp['hr_emp_id'] == hr_emp_id and emp['status'] == "Pending":
                                    print("Work from here")
                                    hr_approval(hr_emp_id, hr_name, emp_name, emp_id, phoneNumber, manager_emp_id, DOJ, DOL, jobTitleName)

                        else:
                            print("No Record")
            else:
                print("Not a HR")
                exit(0)

        else:
            print("Please Enter correct credential")

    except Exception as e:
        raise e


def employee(emailId, password):
    try:
        valid_code = user_validation(emailId, password)
        if valid_code == 1:
            from_sender = read_json_file("from_sender", "config")
            manager_emp_id = ''
            hr_emp_id = ''
            manager_mail_id = ''
            hr_mail_id = ''
            emp_name = ''
            emp_id = ''
            jobTitleName = ''
            personal_email_id = ''
            employeeCode = ''
            region = ''
            DOJ = ''
            phoneNumber = ''
            exit_employee = []
            with open('Employee.txt', 'r') as json_file:
                json_data = json.load(json_file)
                json_file.close()
            for json_obj in json_data:
                if json_obj['emailId'] == emailId:
                    manager_emp_id = json_obj['manager_emp_id']
                    hr_emp_id = json_obj['hr_emp_id']
                    emp_first_nm = json_obj['firstName']
                    emp_last_nm = json_obj['lastName']
                    emp_id = json_obj['empId']
                    personal_email_id = json_obj['personal_emailId']
                    jobTitleName = json_obj['jobTitleName']
                    employeeCode = json_obj['employeeCode']
                    region = json_obj['region']
                    DOJ = json_obj['DOJ']
                    phoneNumber = json_obj['phoneNumber']

                    emp_name = emp_first_nm + ' ' + emp_last_nm

            for json_obj1 in json_data:
                if json_obj1['empId'] == manager_emp_id:
                    manager_mail_id = json_obj1['emailId']

                if json_obj1['empId'] == hr_emp_id:
                    hr_mail_id = json_obj1['emailId']

            mgr_hr_mail_ids = [manager_mail_id, hr_mail_id]

            declaration_code = declaration_form(emp_name, emp_id)
            if declaration_code == 1:
                last_date = str(date.today() + relativedelta(months=+3))
                exit_submitted_date = str(date.today())

                output = employee_leaving_data(emp_id, jobTitleName, emp_name, emailId, personal_email_id, employeeCode,
                                               region, DOJ, last_date, phoneNumber, hr_emp_id, manager_emp_id,
                                               exit_submitted_date)
                exit_employee.append(output)
                with open('Exit_employee.txt', 'r') as infile:

                    try:
                        data = infile.read().replace('][', ',')
                        exit_emp = json.loads(data)
                        infile.close()

                    except ValueError:
                        exit_emp = []

                if len(exit_emp) != 0:
                    for emp in exit_emp:
                        if emp['empId'] != emp_id:
                            with open('Exit_employee.txt', 'a') as outfile:
                                json.dump(exit_employee, outfile)
                                outfile.close()
                        else:
                            print("Employee is already serving notice")

                else:

                    with open('Exit_employee.txt', 'w') as outfile:
                        json.dump(exit_employee, outfile)
                        outfile.close()

                send_mail(from_sender, emailId, mgr_hr_mail_ids, emp_name, last_date, emp_id, exit_submitted_date)
            else:
                print("No declaration")
                exit(0)
        else:
            print("Invalid User. Please enter the correct username and password")

    except Exception as e:
        raise e


