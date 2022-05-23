import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
import gui.run_page as gr
import sys
from tkinter import Button, Text, messagebox

correlation_result_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\correlation_result.xlsx'
correlation_threshold = 0.7
feat_af_corr_anal_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\manual_features_before_backward_forward.xlsx'

def saveThirdStepPaths(entries):
    global correlation_result_path
    global correlation_threshold
    global feat_af_corr_anal_path
    try:
        correlation_threshold = float(entries['Correlation Threshold:'].get())
        correlation_result_path = entries['Correlation Result Path:'].get()
        feat_af_corr_anal_path = entries['Selected Features Path:'].get()
        print('-'*15)
        print('Correlation Threshold: ', correlation_threshold)
        print('Correlation Result Path: ', correlation_result_path)
        print('Selected Features Path: ', feat_af_corr_anal_path)
        print('-'*15)
    except Exception as error:
        messagebox.showinfo(title='Error', message=error)

def thirdStepInputCheck(correlation_threshold):
    try:
        if float(correlation_threshold) >= 0 and float(correlation_threshold) <= 1:
            print('-'*15)
            print('[Passed]: Correlation Threshold is between 0 and 1.')
            print('Input Check passed!')
            print('-'*15)
        else:
            print('-'*15)
            print('[Failed]: Correlation Threshold is not between 0 and 1.')
            print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)


class ThirdStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict

        # 1. Output area
        fields_dict = {
            '1. Input:': 'Empty',
            'Correlation Threshold:': correlation_threshold
        }
        first_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict, add_choose_file_button=False)

        # 2. Output area
        fields_dict = {
            '2. Output:': 'Empty',
            'Correlation Result Path:': correlation_result_path,
            'Selected Features Path:': feat_af_corr_anal_path
        }
        second_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict, y_axis=y_axis-dict['one_portion']/2)
        entries = {**first_entries, **second_entries}
        self.master.bind('<Return>', (lambda event, e=entries: saveThirdStepPaths(e)))
        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()
        self.save_button = Button(self.frame, text='Save', width=10
                                  , command=(lambda e=entries: saveThirdStepPaths(e)))
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10, command=self.openRunPage)

        self.back_button = Button(self.frame, text="Back", anchor='center', command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center', command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center', command=(lambda: thirdStepInputCheck(correlation_threshold)))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)
