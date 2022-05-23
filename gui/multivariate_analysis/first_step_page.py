import pandas as pd
import gui.shared_functions.functions as gsf
import gui.run_page as gr
import gui.multivariate_analysis.main_page as gmm
from tkinter import Button, Text
import sys

# A. STATIC VALUES
binning_result_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\input_MESX\\Results binning.xlsx'
variables_list_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\input_MESX\\ME&SX_keep_variables.xlsx'
destination_path_1 = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\single_factor_analysis.xlsx'
############################################

def saveFirstStepPaths(entries):
    global binning_result_path
    global variables_list_path
    global destination_path_1
    binning_result_path = entries['Result binning:'].get()
    variables_list_path = entries['Variables list:'].get()
    destination_path_1 = entries['Output path:'].get()
    print(binning_result_path, variables_list_path, destination_path_1)

def firstStepInputCheck(binning_result_path, variables_list_path):
    error = []
    try:
        pd.read_excel(binning_result_path)
    except Exception as er:
        error.append(er)
        print('(!) Train dataset format is not Excel')
    try:
        pd.read_excel(variables_list_path)
    except Exception as er:
        error.append(er)
        print('(!) Test dataset format is not Excel')
    if not error:
        print('Input Check passed!')

class FirstStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict
        fields_dict = {
            '1. Input:': 'Empty',
            'Result binning:': binning_result_path,
            'Variables list:': variables_list_path,
            '2. Output:': 'Empty',
            'Output path:': destination_path_1
        }
        entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict)
        self.master.bind('<Return>', (lambda event, e=entries: saveFirstStepPaths(e)))
        self.textbox = Text(self.frame)
        self.save_button = Button(self.frame, text='Save', width=10, command=(lambda e=entries: saveFirstStepPaths(e)))
        sys.stdout = gsf.PrintConsole(self.textbox)
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10, command=self.openRunPage)
        sys.stdout.flush()
        self.back_button = Button(self.frame, text="Back", anchor='center', command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center', command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center', command=lambda: firstStepInputCheck(binning_result_path, variables_list_path))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)