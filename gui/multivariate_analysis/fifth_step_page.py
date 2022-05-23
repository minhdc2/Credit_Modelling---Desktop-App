import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
import gui.run_page as gr
import gui.multivariate_analysis.fourth_step_page as gmft
import sys

import pandas as pd
from tkinter import Button, Text, messagebox

min_number = 17
max_number = 17
pvalue_threshold = 0.1
vif_threshold = 5
beta_threshold = 0
model_performance_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\model_performance.txt'
model_coefficient_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\model_coefficient.txt'

def saveFifthStepPaths(entries):
    global min_number
    global max_number
    global pvalue_threshold
    global vif_threshold
    global beta_threshold
    global model_performance_path
    global model_coefficient_path
    try:
        min_number = int(entries['Min Features Number:'].get())
        max_number = int(entries['Max Features Number:'].get())
        pvalue_threshold = float(entries['P-value Threshold:'].get())
        vif_threshold = float(entries['VIF Threshold:'].get())
        beta_threshold = float(entries['Beta Threshold:'].get())
        model_performance_path = entries['Model Performance Path:'].get()
        model_coefficient_path = entries['Model Coefficient Path:'].get()
        print('-'*15)
        print('Min Features Number: ', min_number)
        print('Max Features Number: ', max_number)
        print('P-value Threshold: ', pvalue_threshold)
        print('VIF Threshold: ', vif_threshold)
        print('Beta Threshold: ', beta_threshold)
        print('Model Performance Path: ', model_performance_path)
        print('Model Coefficient Path: ', model_coefficient_path)
        print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)

def FifthStepInputCheck(min_number, max_number, pvalue_threshold):
    try:
        passed = 0
        if float(min_number) >= 1 and float(min_number) <= max_number:
            passed += 1
            print('-'*15)
            print('[Passed]: Min Number is between 1 and Max Number.')
            print('-'*15)
        else:
            print('-'*15)
            print('[Failed]: Min Number is not between 1 and Max Number.')
            print('-'*15)

        ln = len(pd.read_excel(gmft.feat_af_feat_elim_path))
        if float(max_number) >= min_number and float(max_number) <= ln:
            passed += 1
            print('-'*15)
            print(f'[Passed]: Max Number is between Min Number and {str(ln)}.')
            print('-'*15)
        else:
            print('-'*15)
            print(f'[Failed]: Max Number is not between Min Number and {str(ln)}.')
            print('-'*15)

        if float(pvalue_threshold) >= 0 and float(pvalue_threshold) <= 1:
            passed += 1
            print('-'*15)
            print('[Passed]: P-value Threshold is between 0 and 1.')
            print('-'*15)
        else:
            print('-'*15)
            print('[Failed]: P-value Threshold is not between 0 and 1.')
            print('-'*15)

        if passed == 3:
            print('Input Checks passed!')
        else:
            print('[Failed] Input Checks failed!')
    except Exception as error:
        print('[Failed]: ', error)


class FifthStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict

        # 1. Input area
        fields_dict = {
            '1. Input:': 'Empty',
            'Min Features Number:': min_number,
            'Max Features Number:': max_number,
            'P-value Threshold:': pvalue_threshold,
            'VIF Threshold:': vif_threshold,
            'Beta Threshold:': beta_threshold
        }
        first_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                             , add_choose_file_button=False)

        # 2. Output area
        fields_dict = {
            '2. Output:': 'Empty',
            'Model Performance Path:': model_performance_path,
            'Model Coefficient Path:': model_coefficient_path
        }
        second_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                              , y_axis=y_axis-dict['one_portion'])
        entries = {**first_entries, **second_entries}
        self.master.bind('<Return>', (lambda event, e=entries: saveFifthStepPaths(e)))
        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()
        self.save_button = Button(self.frame, text='Save', width=10
                                  , command=(lambda e=entries: saveFifthStepPaths(e)))
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10
                                          , command=self.openRunPage)

        self.back_button = Button(self.frame, text="Back", anchor='center'
                                  , command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center'
                                  , command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center'
                                   , command=(lambda: FifthStepInputCheck(min_number, max_number, pvalue_threshold)))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)
