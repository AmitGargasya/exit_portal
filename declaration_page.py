import PySimpleGUI as sg


def declaration_form(emp_name, emp_id):
    form = sg.FlexForm('Declaration Page')  # begin with a blank form

    layout = [

        [sg.Checkbox('I {emp_name} with employee id {emp_id} here by declare that I am pressing exit with the reason'
                     .format(emp_name=emp_name, emp_id=emp_id), default=False)],
        [sg.InputCombo(values=['Higher Studies', 'Personal Issues', 'Joining new company'],
                       default_value='Higher Studies', key='_COMBO_', enable_events=False, readonly=False,
                       tooltip='Reason for exit', disabled=False, size=(40, 1))],

        [sg.Submit(), sg.Cancel()]
    ]
    button, values = form.Layout(layout).Read()

    if button == "Submit":
        return 1
    else:
        return 0

