import gui.shared_functions.functions as gsf
import gui.multivariate_analysis.main_page as gmm
from tkinter import Frame, Button

class MainPage:
    def __init__(self, master):
        self.dict = {
            'button_height': 0.05,
            'start_point': 0,
            'one_portion': 0.1,
            'two_portions': 0.2,
            'three_portions': 0.3,
            'four_portions': 0.4,
            'five_portions': 0.5,
            'six_portions': 0.6,
            'seven_portions': 0.7,
            'eight_portions': 0.8,
            'nine_portions': 0.9,
            'ten_portions': 1,
        }
        # keep `root` in `self.master`
        self.master = master
        self.frame = Frame(self.master, bg='white')
        self.frame.place(relx=self.dict['one_portion'], rely=self.dict['start_point'], relwidth=self.dict['eight_portions'], relheight=self.dict['ten_portions'])
        self.button1 = Button(self.frame, text="A. Single Factor Analysis"  # (*)
                            # , command = helloCallBack
                            )
        self.button2 = Button(self.frame, text="B. Multivariate Analysis", command=self.openMultivariateAnalysisPage)
        self.button1.place(relx=self.dict['start_point'], rely=self.dict['two_portions'], relwidth=self.dict['ten_portions'], relheight=self.dict['two_portions'])
        self.button2.place(relx=self.dict['start_point'], rely=self.dict['six_portions'], relwidth=self.dict['ten_portions'], relheight=self.dict['two_portions'])

    def openMultivariateAnalysisPage(self):
        gsf.deleteWidgets(self.frame)
        # use `root` with another class
        return gmm.MultivariateAnalysisPage(self.master, self.frame, self.dict)

