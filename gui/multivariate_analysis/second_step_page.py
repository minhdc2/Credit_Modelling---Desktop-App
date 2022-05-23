import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
import gui.run_page as gr
import pandas as pd
import sys
from tkinter import Button, Text, messagebox

df_train_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\input_MESX\\Raw data for multivariate train set.csv'
df_test_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\input_MESX\\Raw data for multivariate train set.csv'

train_destination_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\train_dataset_after_technical_process_SB.xlsx'
test_destination_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\test_dataset_after_technical_process_SB.xlsx'

def saveSecondStepPaths(entries):
    global df_train_path
    global df_test_path
    global train_destination_path
    global test_destination_path
    try:
        df_train_path = entries['Train dataset:'].get()
        df_test_path = entries['Test dataset:'].get()
        train_destination_path = entries['Transformed Train dataset:'].get()
        test_destination_path = entries['Transformed Test dataset:'].get()
        print(df_train_path, df_test_path, train_destination_path, test_destination_path)
    except Exception as error:
        messagebox.showinfo(title='Error', message=error)

def secondStepInputCheck(df_train_path, df_test_path):
    error = []
    try:
        pd.read_csv(df_train_path)
    except Exception as er:
        error.append(er)
        print('(!) Train dataset format is not *.csv')
    try:
        pd.read_csv(df_test_path)
    except Exception as er:
        error.append(er)
        print('(!) Test dataset format is not *.csv')
    if not error:
        print('Input Check passed!')


class SecondStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict
        fields_dict = {
            '1. Input:': 'Empty',
            'Train dataset:': df_train_path,
            'Test dataset:': df_test_path,
            '2. Output:': 'Empty',
            'Transformed Train dataset:': train_destination_path,
            'Transformed Test dataset:': test_destination_path
        }
        entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict)
        self.master.bind('<Return>', (lambda event, e=entries: saveSecondStepPaths(e)))
        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()
        self.save_button = Button(self.frame, text='Save', width=10
                                  , command=(lambda e=entries: saveSecondStepPaths(e)))
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10, command=self.openRunPage)

        self.back_button = Button(self.frame, text="Back", anchor='center', command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center', command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center', command=(lambda: secondStepInputCheck(df_train_path, df_test_path)))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)
