from tkinter import *
import sys
import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.first_step_page as gmf
import gui.multivariate_analysis.second_step_page as gms
import gui.multivariate_analysis.third_step_page as gmt
import gui.multivariate_analysis.fourth_step_page as gmft
import gui.multivariate_analysis.fifth_step_page as gmff
import gui.multivariate_analysis.sixth_step_page as gmsx
import gui.shared_functions.steps_command as gss

class RunPage:
    def __init__(self, master, frame, dict):
        self.master = master
        self.frame = frame
        self.dict = dict
        self.steps_run_label = Label(self.frame, text='Steps Run', bg='white', anchor='w')
        self.all_steps = [1, 2, 3, 4, 5, 6]
        self.selected_steps = []
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()
        self.first_step_radiobutton = Radiobutton(self.frame, text='Step 1: Technically adjust WoE', bg='white', anchor='w', variable=self.var1
                                                  , value=1, command=lambda:self.checkFirstStepInput(self.var1))
        self.second_step_radiobutton = Radiobutton(self.frame, text='Step 2: Update adjusted WoE to raw data', bg='white', anchor='w', variable=self.var2
                                                  , value=2, command=lambda:self.checkSecondStepInput(self.var2))
        self.third_step_radiobutton = Radiobutton(self.frame, text='Step 3: Remove highly correlated features', bg='white', anchor='w', variable=self.var3
                                                  , value=3, command=lambda:self.checkThirdStepInput(self.var3))
        self.fourth_step_radiobutton = Radiobutton(self.frame, text='Step 4: Backward features elimination', bg='white', anchor='w', variable=self.var4
                                                  , value=4, command=lambda:self.checkFourthStepInput(self.var4))
        self.fifth_step_radiobutton = Radiobutton(self.frame, text='Step 5: Multivariate-scenarios combinations', bg='white', anchor='w', variable=self.var5
                                                  , value=5, command=lambda:self.checkFifthStepInput(self.var5))
        self.sixth_step_radiobutton = Radiobutton(self.frame, text='Step 6: Bootstrapping validation', bg='white', anchor='w', variable=self.var6
                                                  , value=6, command=lambda:self.checkSixthStepInput(self.var6))

        self.textbox = Text(self.frame)
        sys.stdout = gsf.PrintConsole(self.textbox)
        sys.stdout.flush()

        # Buttons Declaration
        self.save_button = Button(self.frame, text="Save", anchor='center', command=lambda: gss.Steps(self.selected_steps, self.all_steps).scenarios())
        self.deselect_button = Button(self.frame, text="Deselect", anchor='center', command=self.deselectButtons)
        self.run_button = Button(self.frame, text="Run", anchor='center', command=(lambda: gss.Steps(self.selected_steps, self.all_steps).scenarios().run()))
        self.quit_button = Button(self.frame, text="Quit", anchor='center', command=self.master.quit)

        # Widgets Location
        self.steps_run_label.place(relx=self.dict['start_point'], rely=self.dict['start_point'], relwidth=self.dict['two_portions'], relheight=self.dict['button_height'])

        self.first_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['one_portion'], relwidth=self.dict['two_portions'], relheight=self.dict['button_height'])
        self.second_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['two_portions'], relwidth=self.dict['three_portions'], relheight=self.dict['button_height'])
        self.third_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['three_portions'], relwidth=self.dict['three_portions'], relheight=self.dict['button_height'])
        self.fourth_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['four_portions'], relwidth=self.dict['three_portions'], relheight=self.dict['button_height'])
        self.fifth_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['five_portions'], relwidth=self.dict['three_portions'], relheight=self.dict['button_height'])
        self.sixth_step_radiobutton.place(relx=self.dict['start_point'], rely=self.dict['six_portions'], relwidth=self.dict['three_portions'], relheight=self.dict['button_height'])

        self.textbox.place(relx=self.dict['three_portions'], rely=self.dict['one_portion'], relwidth=self.dict['ten_portions'], relheight=self.dict['five_portions'])

        self.save_button.place(relx=dict['start_point'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
        self.deselect_button.place(relx=dict['three_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
        self.run_button.place(relx=dict['five_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])
        self.quit_button.place(relx=dict['eight_portions'], rely=dict['nine_portions'], relwidth=dict['two_portions'], relheight=dict['button_height'])

    def checkFirstStepInput(self, var1):
        if var1.get() not in self.selected_steps:
            self.selected_steps.append(var1.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gmf.binning_result_path:
            err_no += 1
            print('(!)[Result binning path] is empty! Return to STEP 1.')
        if not gmf.variables_list_path:
            err_no += 1
            print('(!)[Variables List path] is empty! Return to STEP 1.')
        if not gmf.destination_path_1:
            err_no += 1
            print("(!)[Step 1's Output path] is empty! Return to STEP 1.")
        if err_no == 0:
            print('All paths were filled to run STEP 1.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 1.')
            print('---------------------------------')

    def checkSecondStepInput(self, var2):
        if var2.get() not in self.selected_steps:
            self.selected_steps.append(var2.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gmf.destination_path_1:
            err_no += 1
            print("(!)[Step 1's Output path] is empty! Return to STEP 1.")
        if not gms.df_train_path:
            err_no += 1
            print("(!)[Raw Train Dataset path] is empty! Return to STEP 2.")
        if not gms.df_test_path:
            err_no += 1
            print("(!)[Raw Test Dataset path] is empty! Return to STEP 2.")
        if not gms.train_destination_path:
            err_no += 1
            print("(!)[Transformed Train dataset] is empty! Return to STEP 2.")
        if not gms.test_destination_path:
            err_no += 1
            print("(!)[Transformed Test dataset] is empty! Return to STEP 2.")
        if err_no == 0:
            print('All paths were filled to run STEP 2.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 2.')
            print('---------------------------------')

    def checkThirdStepInput(self, var3):
        if var3.get() not in self.selected_steps:
            self.selected_steps.append(var3.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gmf.destination_path_1:
            err_no += 1
            print("(!)[Step 1's Output path] is empty! Return to STEP 1.")
        if not gms.train_destination_path:
            err_no += 1
            print("(!)[Step 2's Train Destination Path] is empty! Return to STEP 2.")
        if not gmt.correlation_threshold:
            err_no += 1
            print("(!)[Correlation Threshold] is empty! Return to STEP 3.")
        if not gmt.correlation_result_path:
            err_no += 1
            print("(!)[Correlation Result Path] is empty! Return to STEP 3.")
        if err_no == 0:
            print('All paths were filled to run STEP 3.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 3.')
            print('---------------------------------')

    def checkFourthStepInput(self, var4):
        if var4.get() not in self.selected_steps:
            self.selected_steps.append(var4.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gms.train_destination_path:
            err_no += 1
            print("(!)[Step 2's Train Destination Path] is empty! Return to STEP 2.")
        if not gmt.feat_af_corr_anal_path:
            err_no += 1
            print("(!)[Step 3's Selected Features Path] is empty! Return to STEP 3.")
        if not gmft.backward_pvalue_threshold:
            err_no += 1
            print("(!)[P-value Threshold] is empty! Return to STEP 4.")
        if not gmft.vif_threshold:
            err_no += 1
            print("(!)[VIF Threshold] is empty! Return to STEP 4.")
        if not str(gmft.beta_threshold):
            err_no += 1
            print("(!)[Beta Threshold] is empty! Return to STEP 4.")
        if not gmft.feat_af_feat_elim_path:
            err_no += 1
            print("(!)[Selected Features Path] is empty! Return to STEP 4.")
        if err_no == 0:
            print('All paths were filled to run STEP 4.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 3.')
            print('---------------------------------')

    def checkFifthStepInput(self, var5):
        if var5.get() not in self.selected_steps:
            self.selected_steps.append(var5.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gms.train_destination_path:
            err_no += 1
            print("(!)[Step 2's Train Destination Path] is empty! Return to STEP 2.")
        if not gms.test_destination_path:
            err_no += 1
            print("(!)[Step 2's Test Destination Path] is empty! Return to STEP 2.")
        if not gmft.feat_af_feat_elim_path:
            err_no += 1
            print("(!)[Step 4's Selected Features Path] is empty! Return to STEP 4.")
        if not gmff.min_number:
            err_no += 1
            print("(!)[Min Features Number] is empty! Return to STEP 5.")
        if not gmff.max_number:
            err_no += 1
            print("(!)[Max Features Number] is empty! Return to STEP 5.")
        if not gmff.pvalue_threshold:
            err_no += 1
            print("(!)[P-value Threshold] is empty! Return to STEP 5.")
        if not gmff.vif_threshold:
            err_no += 1
            print("(!)[VIF Threshold] is empty! Return to STEP 5.")
        if not str(gmff.beta_threshold):
            err_no += 1
            print("(!)[Beta Threshold] is empty! Return to STEP 5.")
        if not gmff.model_performance_path:
            err_no += 1
            print("(!)[Model Performance Path] is empty! Return to STEP 5.")
        if not gmff.model_coefficient_path:
            err_no += 1
            print("(!)[Model Coefficient Path] is empty! Return to STEP 5.")
        if err_no == 0:
            print('All paths were filled to run STEP 5.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 5.')
            print('---------------------------------')

    def checkSixthStepInput(self, var6):
        if var6.get() not in self.selected_steps:
            self.selected_steps.append(var6.get())
        print('Selected Steps: ', self.selected_steps)
        err_no = 0
        if not gms.train_destination_path:
            err_no += 1
            print("(!)[Step 2's Train Destination Path] is empty! Return to STEP 2.")
        if not gms.test_destination_path:
            err_no += 1
            print("(!)[Step 2's Test Destination Path] is empty! Return to STEP 2.")
        if not gmff.model_performance_path:
            err_no += 1
            print("(!)[Model Performance Path] is empty! Return to STEP 5.")
        if not gmff.model_coefficient_path:
            err_no += 1
            print("(!)[Model Coefficient Path] is empty! Return to STEP 5.")
        if not gmsx.test_sampling_percent:
            err_no += 1
            print("(!)[Test Sampling %] is empty! Return to STEP 6.")
        if not gmsx.iteration:
            err_no += 1
            print("(!)[Iteration] is empty! Return to STEP 6.")
        if not gmsx.bootstrapping_performance_path:
            err_no += 1
            print("(!)[Bootstrapping Performance Path] is empty! Return to STEP 6.")
        if err_no == 0:
            print('All paths were filled to run STEP 6.')
        else:
            print('---------------------------------')
            print(str(err_no) + ' missing input paths were found to run STEP 6.')
            print('---------------------------------')

    def deselectButtons(self):
        self.var1.set(0)
        self.var2.set(0)
        self.var3.set(0)
        self.var4.set(0)
        self.var5.set(0)
        self.var6.set(0)
        self.selected_steps = []
        return self
