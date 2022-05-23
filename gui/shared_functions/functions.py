from tkinter import Label, Entry, Button, filedialog, END

def makeform(root, fields_dict, dict, y_axis=0, add_choose_file_button=True):
    entries = {}
    for field in list(fields_dict.keys()):
        label = Label(root, bg='white', text=field, anchor='w')
        y_axis += dict['one_portion']/2
        label.place(relx=dict['start_point'], rely=y_axis, relwidth=dict['two_portions'], relheight=dict['button_height'])
        if fields_dict[field] != 'Empty':
            entry = Entry(root)
            entry.insert(END, fields_dict[field])
            entry_width = dict['two_portions']
            if add_choose_file_button:
                button = Button(root, text='Choose File', command=lambda e=entry: navigateFileLocation(e))
                button.place(relx=dict['nine_portions'], rely=y_axis, relwidth=dict['one_portion'], relheight=dict['button_height'] * 0.8)
                entry_width = dict['seven_portions']

            entry.place(relx=dict['two_portions'], rely=y_axis, relwidth=entry_width, relheight=dict['button_height'])
            entries[field] = entry
    for key in list(dict.keys()):
        if dict[key] > y_axis + dict['button_height']:
            y_axis = dict[key]
            break
    return entries, y_axis

def navigateFileLocation(entry):
    file_path = filedialog.askopenfilename()
    entry.insert(END, file_path)

class PrintConsole(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(END, text) # write text to textbox
        self.textbox.see('end')
        self.textbox.update_idletasks()
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

def deleteWidgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def widgetsPosition1(check_button, save_button, save_and_run_button, textbox, back_button, quit_button, dict, y_axis):
    check_button.place(relx=dict['start_point'], rely=y_axis, relwidth=dict['two_portions'], relheight=dict['button_height'])
    textbox_y_axis = y_axis + dict['one_portion']
    textbox_height = dict['nine_portions'] - dict['one_portion'] / 2 - textbox_y_axis
    textbox.place(relx=dict['start_point'], rely=textbox_y_axis, relwidth=dict['ten_portions'], relheight=textbox_height)
    back_button.place(relx=dict['start_point'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
    save_button.place(relx=dict['three_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
    save_and_run_button.place(relx=dict['five_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
    quit_button.place(relx=dict['eight_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
