from tkinter import Menu
import gui.main_page as gm

def MenuTab(root):
    menubar = Menu()

    steps_menu = Menu(menubar, tearoff=0)
    steps_menu.add_command(label='Home Page', command=lambda r=root: MainPage(root))
    multivariate_analysis_menu = Menu(steps_menu, tearoff=0)
    multivariate_analysis_menu.add_separator()
    multivariate_analysis_menu.add_command(label='Step 1: Technically adjust WoE',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openFirstStepPage())
    multivariate_analysis_menu.add_command(label='Step 2: Update adjusted WoE to raw data',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openSecondStepPage())
    multivariate_analysis_menu.add_command(label='Step 3: Remove highly correlated features',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openThirdStepPage())
    multivariate_analysis_menu.add_command(label='Step 4: Backward features elimination',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openFourthStepPage())
    multivariate_analysis_menu.add_command(label='Step 5: Multivariate-scenarios combinations',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openFifthStepPage())
    multivariate_analysis_menu.add_command(label='Step 6: Bootstrapping validation',
                                           command=lambda r=root: gm.MainPage(r).openMultivariateAnalysisPage().openSixthStepPage())
    menubar.add_cascade(menu=steps_menu, label='Steps')
    steps_menu.add_cascade(menu=multivariate_analysis_menu, label='B. Multivariate Analysis')
    root.config(menu=menubar)