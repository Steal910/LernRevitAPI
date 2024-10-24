# -*- coding: utf-8 -*-
__title__   = "Rename Views"
__doc__     = """Version = 1.0
Date    = 23.10.2024
________________________________________________________________
Description:

Rename Views in Revit by using Find/Replace Logic

________________________________________________________________
How-To:

-> Click on the button
-> Select Views
-> Define Renaming Rules
-> Rename Views

________________________________________________________________
Last Updates:
- [23.10.2024] v1.0 Release
________________________________________________________________
Author: Mateusz Dworzycki"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

#.NET Imports
import clr
from pyrevit.forms import select_views

clr.AddReference('System')
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# 1️⃣ Select Views

# Get Views - Selected in ProjectBrowser
sel_el_ids = uidoc.Selection.GetElementIds()
sel_elem = [doc.GetElement(e_id) for e_id in sel_el_ids]
sel_views = [el for el in sel_elem if issubclass(type(el),View)]

# If None Selected - Promp SelectViews from pyrevit.forms.select_views()
if not sel_views:
    sel_views = forms.select_views()

# Ensure Views Selected
if not sel_views:
    forms.alert('No Views Selected. Please Try Again', exitscript=True)

# 2️⃣🅰️ Define Renaming Rules
#prefix  = 'pre-'
#find    = 'FloorPlan'
#replace = 'MD-Level'
#suffix  = '-suf'

# 2️⃣🅱️ Define Renaming Rules (UI FORM)

from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
components = [Label('Prefix:'),  TextBox('prefix'),
              Label('Find:'),    TextBox('find'),
              Label('Replace:'), TextBox('replace'),
              Label('Suffix:'),  TextBox('suffix'),
              Separator(),       Button('Rename Views')]

form = FlexForm('Title', components)
form.show()

user_inputs = form.values #type: dict
prefix      = user_inputs['prefix']
find        = user_inputs['find']
replace     = user_inputs['replace']
suffix      = user_inputs['suffix']

# Start Transaction to make changes in project
t = Transaction(doc, 'py-Rename Views')
t.Start()   #🔓

for view in sel_views:
    #3️⃣ Create new View Name
    old_name = view.Name
    new_name = prefix + old_name.replace(find, replace) + suffix

    #4️⃣ Rename Views (Ensure uniqe view name)
    for i in range(20):
        try:
            view.Name = new_name
            print('{} -> {}'.format(old_name, new_name))
            break
        except:
            new_name += '*'

t.Commit()  #🔒

print('-'*50)
print('Done!')