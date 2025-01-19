"""
main/application.py: root window class
"""
import tkinter as tk
from tkinter import ttk
from . import views as v
from . import models as m
import customtkinter

# customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_appearance_mode("dark")
# class Application(tk.Tk):  # subclase from Tk instead of Frame
class Application(customtkinter.CTk):  # subclase from Tk instead of Frame
    """Application root window.
    It needs to contain:
        - A title label
        - An instance of MyForm class (call and place form in GUI)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = m.myModel()
        self.myform = v.MyForm(self, self.model)

        # window title
        self.title('Drawing Application')
        self.columnconfigure(0, weight=0)

        # header
        # ttk.Label(  # parent is self. self is our Tk instance inside this class
        customtkinter.CTkLabel(  # parent is self. self is our Tk instance inside this class
            self, text=' ',
            font=("TkDefaultFont", 18)
        ).grid(row=0)

        # Add form with widgets
        self.myform = v.MyForm(self, self.model)

        self.myform.grid(row=1, padx=10, sticky=tk.W + tk.E)




if __name__ == "__main__":
    # create instance of our application and start its mainloop
    app = Application()
    app.mainloop()
