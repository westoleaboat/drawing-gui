"""
  main/views.py: form containing widgets
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import customtkinter

from . import widgets as w
from .constants import FieldTypes as FT
from PIL import Image, ImageDraw

# customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_appearance_mode("dark")
class MyForm(customtkinter.CTkFrame):
    # class MyForm(tk.Frame):
    """Input Form for widgets

    - self._vars = Create a dictionary to hold all out variable objects 
    - _add_frame = instance method that add a new label frame. Pass in 
                   label text and optionally a number of columns.

    """

    var_types = {
        FT.string: tk.StringVar,
        FT.string_list: tk.StringVar,
        FT.short_string_list: tk.StringVar,
        FT.iso_date_string: tk.StringVar,
        FT.long_string: tk.StringVar,
        FT.decimal: tk.DoubleVar,
        FT.integer: tk.IntVar,
        FT.boolean: tk.BooleanVar
    }

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        self._vars = {  # hold all variable objects
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # disable var for Output field
        self._disable_var = tk.BooleanVar()

        # build the form
        self.columnconfigure(0, weight=1)

        # w.LabelInput(
        #     self, 
        #     'Default Label',
        #     input_class=w.BoundText, 
        #     var=self._vars['Notes'],
        #     input_args={
        #         "width": 55, 
        #         "height": 50}
        # ).grid(sticky=tk.W + tk.E, row=0, column=1, rowspan=2)


        w.LabelInput(
          self,
          "Brush Size:",
          # input_class=tk.Scale,
          input_class=customtkinter.CTkSlider,
          field_spec=fields['Brush_size'],
          var=self._vars['Brush_size'],
          # input_args={'orient':'horizontal'}#, 'relief':'raised'}
        ).grid(row=1, pady=(10, 0))

        self._vars['Brush_size'].set(3)
        self._vars['Pen_color'].set('black')

        # CANVAS
        # self.canvas = tk.Canvas(self, bg='white', width=500, height=400)#, relief='groove') #must be flat, groove, raised, ridge, solid, or sunken
        self.canvas = customtkinter.CTkCanvas(self, bg='white', width=500, height=400)#, relief='groove') #must be flat, groove, raised, ridge, solid, or sunken
        self.canvas.grid(row=0,column=0, sticky='nsew')

        # self.slider = customtkinter.CTkSlider(self, from_=1, to=10)

        # Setup image to store canvas for saving
        self.image = Image.new("RGB", (500, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Variables for drawing
        self.previous_x = None
        self.previous_y = None
        # self.pen_color = "black"
        # self.pen_size = 3

        # Add buttons and controls
        # self.add_buttons()

        # self._disable_var.set(True)
        self._disable_var.set(False)

        # text to display data from form
        self.output_var = tk.StringVar()

        ###########
        # buttons #
        ###########
        # improving inter-object communication was added to bug tracker

        # buttons = ttk.Frame(self)  # add on a frame
        buttons = customtkinter.CTkFrame(self)  # add on a frame
        buttons.grid(sticky=tk.W + tk.E, row=2, pady=(0, 20))
        # pass instance methods as callback commands
        # self.transbutton = ttk.Button(
        #     buttons, text="Text to Binary", command=self._on_trans)
        # # self.transbutton.pack(side=tk.RIGHT)

        # self.transbutton = ttk.Button(
        #     buttons, text="Binary to Text", command=self._on_trans, state='disabled')
        # # self.transbutton.pack(side=tk.RIGHT)

        # # self.savebutton = ttk.Button(
        # #     buttons, text="Save", command=self.master._on_save)  # on parent
        # # self.savebutton.pack(side=tk.RIGHT)
        # self.resetbutton = ttk.Button(
        #     buttons, text="Reset", command=self.reset)  # on this class
        # self.resetbutton.pack(side=tk.RIGHT)

        # def add_buttons(self):
            # Color Picker
        # self.color_button = tk.Button(buttons, text="Pick Color", command=self.choose_color)
        self.color_button = customtkinter.CTkButton(buttons, text="Pick Color", command=self.choose_color)
        # self.color_button.pack(side=tk.LEFTpadx=5)
        self.color_button.pack(side=tk.LEFT, padx=5)

        # # Brush Size Adjust
        # self.size_label = tk.Label(self.root, text="Brush Size:")
        # self.size_label.pack(side=tk.LEFT, padx=5)

        # self.size_scale = tk.Scale(self.root, from_=1, to_=10, orient=tk.HORIZONTAL)
        # self.size_scale.set(self.pen_size)
        # self.size_scale.pack(side=tk.LEFT)

        # Clear Button
        self.clear_button = customtkinter.CTkButton(buttons, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Exit Button
        self.exit_button = customtkinter.CTkButton(buttons, text="Exit", command=self.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=5)

        # Save Button
        self.save_button = customtkinter.CTkButton(buttons, text="Save Drawing", command=self.save_drawing)
        self.save_button.pack(side=tk.RIGHT, padx=5)


        # Bind mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def choose_color(self):
        # Open color picker
        color = colorchooser.askcolor()[1]
        if color:
            # self.pen_color = color
            self._vars['Pen_color'].set(color)

    def paint(self, event):
        # Draw on the canvas
        if self.previous_x and self.previous_y:
            # self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, width=self.pen_size,
            self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, width=self._vars['Brush_size'].get(),
                                    fill=self._vars['Pen_color'].get(), capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([(self.previous_x, self.previous_y), (event.x, event.y)], fill=self._vars['Pen_color'].get(),
                           width=self._vars['Brush_size'].get())
        self.previous_x = event.x
        self.previous_y = event.y

    def reset(self, event):
        # Reset coordinates after drawing
        self.previous_x = None
        self.previous_y = None

    def clear_canvas(self):
        # Clear the canvas and reset image
        self.canvas.delete("all")
        self.image = Image.new("RGB", (500, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_drawing(self):
        # Save the drawing as an image file
        try:
            file_path = "drawing.png"
            self.image.save(file_path)
            messagebox.showinfo("Success", f"Drawing saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving drawing: {e}")

    # def reset(self):
    #     """Reset entries. Set all variables to empty string"""
    #     # activate widget
    #     self._disable_var.set(False)
    #     # self.set_output_state(tk.NORMAL)

    #     # reset data
    #     for var in self._vars.values():
    #         if isinstance(var, tk.BooleanVar):
    #             # uncheck checkbox
    #             var.set(False)
    #         else:
    #             # set inputs to empty string
    #             var.set('')
    #             # set data label to empty string
    #             # self.output_var.set('')
    #     # disable widget
    #     self._disable_var.set(True)
        # self.set_output_state(tk.DISABLED)

    def get(self):
        """Retrieve data from the form so it can be saved or used"""
        data = {}
        for key, variable in self._vars.items():
            try:
                # retrieve from ._vars
                data[key] = variable.get()
            except tk.TclError as e:
                # create error message
                message = f'Error in field: {key}. Data not saved!'
                raise ValueError(message) from e
        # return the data
        return data

    #########################################
    # Disable widget if disable_var not used:
    #
    # def set_output_state(self, state):
    #     output_widget = self._get_widget_by_var(self._vars['Output'])
    #     if output_widget:
    #         output_widget.input.configure(state=state)

    # def _get_widget_by_var(self, var):
    #     """Return the widget associated with a given variable."""
    #     for widget in self.winfo_children():
    #         if isinstance(widget, w.LabelInput) and widget.variable == var:
    #             return widget
    #     return None
    #########################################

    # def _on_trans(self):
    #     self.event_generate('<<TranslateText>>')
        # self._disable_var.set(False)

