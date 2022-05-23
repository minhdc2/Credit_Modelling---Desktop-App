import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
import gui.run_page as gr
import sys
from tkinter import Button, Text

bootstrapping_performance_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output_MESX\\bootsrapping_performance.xlsx'
test_sampling_percent = 0.8
iteration = 100

def saveSixthStepPaths(entries):
    global test_sampling_percent
    global iteration
    global bootstrapping_performance_path
    try:
        test_sampling_percent = float(entries['Test Sampling %:'].get())
        iteration = int(entries['Number of Iterations:'].get())
        bootstrapping_performance_path = entries['Bootstrapping Performance Path:'].get()
        print('-'*15)
        print('Test Sampling %: ', test_sampling_percent)
        print('Number of Iterations: ', iteration)
        print('Bootstrapping Performance Path: ', bootstrapping_performance_path)
        print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)

def SixthStepInputCheck(test_sampling_percent):
    try:
        if float(test_sampling_percent) >= 0 and float(test_sampling_percent) <= 1:
            print('-'*15)
            print('[Passed]: Test Sampling % is between 0 and 1.')
            print('-'*15)
            print('Input Checks passed!')
        else:
            print('-'*15)
            print('[Failed]: Test Sampling % is not between 0 and 1.')
            print('-'*15)
    except Exception as error:
        print('[Failed]: ', error)


class SixthStepPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict

        # 1. Input area
        fields_dict = {
            '1. Input:': 'Empty',
            'Test Sampling %:': test_sampling_percent,
            'Number of Iterations:': iteration
        }
        first_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                             , add_choose_file_button=False)

        # 2. Output area
        fields_dict = {
            '2. Output:': 'Empty',
            'Bootstrapping Performance Path:': bootstrapping_performance_path
        }
        second_entries, y_axis = gsf.makeform(self.frame, fields_dict, self.dict
                                              , y_axis=y_axis-dict['one_portion'])
        entries = {**first_entries, **second_entries}
        self.master.bind('<Return>', (lambda event, e=entries: saveSixthStepPaths(e)))
        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()
        self.save_button = Button(self.frame, text='Save', width=10
                                  , command=(lambda e=entries: saveSixthStepPaths(e)))
        self.save_and_run_button = Button(self.frame, text='Save & Run', width=10
                                          , command=self.openRunPage)

        self.back_button = Button(self.frame, text="Back", anchor='center'
                                  , command=self.backToMultivariateStepsPage)
        self.quit_button = Button(self.frame, text="Quit", anchor='center'
                                  , command=self.master.quit)
        self.check_button = Button(self.frame, text="Check Input", anchor='center'
                                   , command=(lambda: SixthStepInputCheck(test_sampling_percent)))
        gsf.widgetsPosition1(self.check_button, self.save_button, self.save_and_run_button, self.textbox, self.back_button, self.quit_button
                         , self.dict, y_axis)

    def backToMultivariateStepsPage(self):
        gsf.deleteWidgets(self.frame)
        gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

    def openRunPage(self):
        gsf.deleteWidgets(self.frame)
        gr.RunPage(self.master, self.frame, self.dict)
