import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
import gui.run_page as gr
import sys
from tkinter import Button, Text, messagebox

backward_pvalue_threshold = 0.05
vif_threshold = 5
beta_threshold = 0
feat_af_feat_elim_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\manual_features_before_combinations.xlsx'

def saveFourthStepPaths(entries):
    global backward_pvalue_threshold
    global vif_threshold
    global beta_threshold
    global feat_af_feat_elim_path
    try:
        backward_pvalue_threshold = float(entries['P-value Threshold:'].get())
        vif_threshold = float(entries['VIF Threshold:'].get())
        beta_threshold = float(entries['Beta Threshold:'].get())
        print('-'*15)
        print('P-value Threshold: ', backward_pvalue_threshold)
        print('VIF Threshold: ', vif_threshold)
        print('Beta Threshold: ', beta_threshold)
        print('Selected Features Path: ', feat_af_feat_elim_path)
        print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)

def FourthStepInputCheck(backward_pvalue_threshold):
    try:
        if float(backward_pvalue_threshold) >= 0 and float(backward_pvalue_threshold) <= 1:
            print('-'*15)
            print('[Passed]: P-value Threshold is between 0 and 1.')
            print('Input Check passed!')
            print('-'*15)
        else:
            print('-'*15)
            print('[Failed]: P-value Threshold is not between 0 and 1.')
            print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)


class FourthStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict

        # 1. Input area
        fields_dict = {
            '1. Input:': 'Empty',
            'P-value Threshold:': backward_pvalue_threshold,
            'VIF Threshold:': vif_threshold,
            'Beta Threshold:': beta_threshold
        }
        first_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                             , add_choose_file_button=False)

        # 2. Output area
        fields_dict = {
            '2. Output:': 'Empty',
            'Selected Features Path:': feat_af_feat_elim_path
        }
        second_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                              , y_axis=y_axis-dict['one_portion'])
        entries = {**first_entries, **second_entries}
        self.master.bind('<Return>', (lambda event, e=entries: saveFourthStepPaths(e)))
        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()
        self.save_button = Button(self.frame, text='Save', width=10
                                  , command=(lambda e=entries: saveFourthStepPaths(e)))
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10
                                          , command=self.openRunPage)

        self.back_button = Button(self.frame, text="Back", anchor='center'
                                  , command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center'
                                  , command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center'
                                   , command=(lambda: FourthStepInputCheck(backward_pvalue_threshold)))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)
