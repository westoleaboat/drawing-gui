""" main.py: blueprint logic

The code is organized in the following classes:

    -BoundText: Text widget with a bound variable
    -LabelInput: Widget containing a label and input together
    -MyForm: Input form for widgets
    -Application: Application root window


Source: https://dailypythonprojects.substack.com/
This is a ~fast~ MVC implementation of "Drawing App with Tkinter" from the Source.
"""


from blueprint.application import Application

app = Application()
app.mainloop()
