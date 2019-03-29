import PySimpleGUI as sg
from exit_portal.exit_portal import employee, hr

form = sg.FlexForm('Exit Portal Login Page')  # begin with a blank form

layout = [
    [sg.Text('Please enter below details')],
    [sg.Text('Email_Id', size=(15, 1)), sg.InputText()],
    [sg.Text('Password', size=(15, 1)), sg.InputText(password_char='*')],
    [sg.Checkbox('HR', enable_events=False, key='HR'),
     sg.Checkbox('Employee', default=False, enable_events=False, key='Employee')],
    [sg.Submit(), sg.Cancel()]
]
button, values = form.Layout(layout).Read()

email_id = values[0]
password = values[1]

if button == "Submit":
    if values['HR'] is True:
        hr(email_id, password)
    elif values['Employee'] is True:
        employee(email_id, password)
    else:
        print("Choose Any one Option(HR/Employee)")
        exit(0)
else:
    exit(0)
