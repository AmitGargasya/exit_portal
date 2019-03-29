import PySimpleGUI as sg


def hr_approval(hr_emp_id, hr_name, emp_name, emp_id, phoneNumber, manager_emp_id, DOJ, DOL, jobTitleName):
    form = sg.FlexForm('HR approval on employee exit')  # begin with a blank form

    layout = [



        [sg.Submit(), sg.Cancel()]
    ]
    button, values = form.Layout(layout).Read()

    if button == "Submit":
        return 1
    else:
        return 0

