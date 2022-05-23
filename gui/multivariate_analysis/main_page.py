import gui.multivariate_analysis.first_step_page as gmf
import gui.multivariate_analysis.second_step_page as gms
import gui.multivariate_analysis.third_step_page as gmt
import gui.multivariate_analysis.fourth_step_page as gmft
import gui.multivariate_analysis.fifth_step_page as gmff
import gui.multivariate_analysis.sixth_step_page as gmsx
import gui.main_page as gm
import gui.shared_functions.functions as gsf
from tkinter import Button

class MultivariateAnalysisPage:
    def __init__(self, master, frame, dict):
        # keep `root` in `self.master`
        self.master = master
        self.frame = frame
        self.dict = dict
        self.save_quit_button_width = self.dict['two_portions']
        buttons = []
        self.button1 = Button(self.frame, text="Step 1: Technically adjust WoE", anchor='w', command=self.openFirstStepPage)
        buttons.append(self.button1)
        self.button2 = Button(self.frame, text="Step 2: Update adjusted WoE to raw data", anchor='w', command=self.openSecondStepPage)
        buttons.append(self.button2)
        self.button3 = Button(self.frame, text="Step 3: Remove highly correlated features", anchor='w', command = self.openThirdStepPage)
        buttons.append(self.button3)
        self.button4 = Button(self.frame, text="Step 4: Backward features elimination", anchor='w', command = self.openFourthStepPage)
        buttons.append(self.button4)
        self.button5 = Button(self.frame, text="Step 5: Multivariate-scenarios combinations", anchor='w', command = self.openFifthStepPage)
        buttons.append(self.button5)
        self.button6 = Button(self.frame, text="Step 6: Bootstrapping validation", anchor='w', command = self.openSixthStepPage)
        buttons.append(self.button6)
        self.y_axis = self.dict['start_point']
        for button in buttons:
            self.y_axis += 0.1
            button.place(relx=self.dict['start_point'], rely=self.y_axis, relwidth=self.dict['ten_portions'], relheight=self.dict['button_height'])
        self.button7 = Button(self.frame, text="Back", anchor='center', command=self.backToMainPage)
        self.button7.place(rely=self.dict['nine_portions'], relwidth=self.dict['two_portions'], relheight=self.dict['button_height'])
        self.button8 = Button(self.frame, text="Quit", anchor='center', command=self.master.quit)
        self.button8.place(relx=dict['eight_portions'], rely=self.dict['nine_portions'], relwidth=self.dict['two_portions'], relheight=self.dict['button_height'])

    def openFirstStepPage(self):
        gsf.deleteWidgets(self.frame)
        gmf.FirstStepPage(self.master, self.frame, self.dict)

    def openSecondStepPage(self):
        gsf.deleteWidgets(self.frame)
        gms.SecondStepPage(self.master, self.frame, self.dict)

    def openThirdStepPage(self):
        gsf.deleteWidgets(self.frame)
        gmt.ThirdStepPage(self.master, self.frame, self.dict)

    def openFourthStepPage(self):
        gsf.deleteWidgets(self.frame)
        gmft.FourthStepPage(self.master, self.frame, self.dict)

    def openFifthStepPage(self):
        gsf.deleteWidgets(self.frame)
        gmff.FifthStepPage(self.master, self.frame, self.dict)

    def openSixthStepPage(self):
        gsf.deleteWidgets(self.frame)
        gmsx.SixthStepPage(self.master, self.frame, self.dict)

    def backToMainPage(self):
        gsf.deleteWidgets(self.frame)
        # use `root` with another class
        gm.MainPage(self.master)