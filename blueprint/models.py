""" main/models.py: example data"""

from .constants import FieldTypes as FT
import tkinter as tk


from . import views as v


class myModel:
    # pass
    fields = {
        # "Notes": {'req': True, 'type': FT.long_string}
        "Brush_size": {'req': True, 'type': FT.integer, 'min':1, "max":10},
        "Pen_color": {'req': True, "type": FT.string}
    }

    