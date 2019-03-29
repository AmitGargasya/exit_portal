import os
import json
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_json_file(key, file):
    file_path = os.getcwd()
    with open(file_path + '/{file}.json'.format(file=file), 'r') as f:
        config = json.load(f)
        for i in key.split(","):
            if i in config:
                config = config[i]
            else:
                return None
        return config


def send_mail(from_sender, emp_mail_id, mgr_hr_mail_ids, emp_name, last_date, emp_id, exit_submitted_date):
    try:
        msg = MIMEMultipart()
        msg["From"] = from_sender
        msg['To'] = emp_mail_id
        msg['Cc'] = ", ".join(mgr_hr_mail_ids)
        msg["Subject"] = "Acknowledgment of resignation of {emp_name} with employee id {emp_id}"\
            .format(emp_name=emp_name, emp_id=emp_id)
        body = """Dear {emp_name},

The Company is in receipt of your resignation dated {exit_submitted_date}.

We would like to inform you that we are in receipt of your resignation and you would be released from the services of the company effective close of business hours on {last_date}, subject to your completing the notice period as stipulated above.

Regards,
Seperation Cell

""".format(emp_name=emp_name, exit_submitted_date=exit_submitted_date, last_date=last_date)
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP_SSL('mx5.alerts.valuelabs.com', 465)
        s.login(from_sender, "******")
        text = msg.as_string()
        toaddr = []
        toaddr.append(emp_mail_id)
        toaddr = toaddr + mgr_hr_mail_ids
        s.sendmail(from_sender, toaddr, text)
        s.quit()
    except Exception as error:
        print("Error while sending mail " + str(error))


def employee_leaving_data(empId, jobTitleName, emp_name, emailId, personal_emailId, employeeCode,
                          region, DOJ, DOL, phoneNumber, hr_emp_id, manager_emp_id, exit_submitted_date):

    data = {
        "empId": empId,
        "jobTitleName": jobTitleName,
        "emp_name": emp_name,
        "emailId": emailId,
        "personal_emailId": personal_emailId,
        "employeeCode": employeeCode,
        "region": region,
        "DOJ": DOJ,
        "DOL": DOL,
        "phoneNumber": phoneNumber,
        "hr_emp_id": hr_emp_id,
        "manager_emp_id": manager_emp_id,
        "exit_submitted_date": exit_submitted_date,
        "status": "Pending"
    }
    return data
