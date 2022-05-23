from tkinter import messagebox
import pandas as pd
import adjust_woe_for_bins.input_values as fss
import adjust_woe_for_bins.support.functions as asf
import update_woe_adjusted_to_raw.input_values as ui
import update_woe_adjusted_to_raw.support.functions as usf
import correlation_analysis.support.functions as csf
import features_elimination.support.functions as fsf
import scenarios_combinations.support.functions as ssf
import gui.multivariate_analysis.first_step_page as gmf
import gui.multivariate_analysis.second_step_page as gms
import gui.multivariate_analysis.third_step_page as gmt
import gui.multivariate_analysis.fourth_step_page as gmft
import gui.multivariate_analysis.fifth_step_page as gmff
import gui.multivariate_analysis.sixth_step_page as gmsx
import bootstrapping_validation.support.functions as bsf

# 1. First Step
single_factor_analysis = None

class FirstStep():
    def __init__(self, variables_list_path, binning_result_path, special_values, destination_path_1):
        self.variables_list_path = variables_list_path
        self.binning_result_path = binning_result_path
        self.special_values = special_values
        self.destination_path_1 = destination_path_1

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self):
        if not self.skipped:
            global single_factor_analysis
            single_factor_analysis = asf.runTechnicalProcess(self.variables_list_path, self.binning_result_path
                                                         , self.special_values, self.destination_path_1)

# 2. Second Step
df_train = None
df_test = None
all_cols = None
predictor_cols = None

class SecondStep():
    def __init__(self, df_train_path, df_test_path, dependent_col, excluded_cols, single_factor_analysis
                 , train_destination_path, test_destination_path):
        self.df_train_path = df_train_path
        self.df_test_path = df_test_path
        self.dependent_col = dependent_col
        self.excluded_cols = excluded_cols
        self.single_factor_analysis = single_factor_analysis
        self.train_destination_path = train_destination_path
        self.test_destination_path = test_destination_path

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self, separately=True):
        if not self.skipped:
            if separately:
                global single_factor_analysis
                single_factor_analysis = pd.read_excel(gmf.destination_path_1)
                self.single_factor_analysis = single_factor_analysis
            global df_train
            global all_cols
            global predictor_cols
            global df_test
            result_set = usf.runUpdateWoEAdjusted(self.df_train_path, self.dependent_col, self.excluded_cols, self.single_factor_analysis, self.train_destination_path)
            df_train, all_cols, predictor_cols = result_set[0], result_set[1], result_set[2]
            df_test_raw = pd.read_csv(self.df_test_path)
            df_test_raw = usf.upperColumnName(df_test_raw)
            df_test = usf.UpdateWoEAdjustedToRaw(predictor_cols, df_test_raw, self.single_factor_analysis).saveToExcel(self.test_destination_path)

# 3. Third Step
features_after_corr_analysis = None

class ThirdStep():
    def __init__(self, df_train, predictor_cols, single_factor_analysis
                 , correlation_threshold, correlation_result_path, feat_af_corr_anal_path):
        self.df_train = df_train
        self.predictor_cols = predictor_cols
        self.single_factor_analysis = single_factor_analysis
        self.correlation_threshold = correlation_threshold
        self.correlation_result_path = correlation_result_path
        self.feat_af_corr_anal_path = feat_af_corr_anal_path

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self, separately=True):
        global features_after_corr_analysis
        if not self.skipped:
            if separately:
                global df_train
                global predictor_cols
                global single_factor_analysis
                df_train = pd.read_excel(gms.train_destination_path)
                all_cols = list(df_train.columns)
                predictor_cols = usf.Collection(all_cols).exclude(ui.dependent_col + ui.excluded_cols).show()
                single_factor_analysis = pd.read_excel(gmf.destination_path_1)
                self.df_train = df_train
                self.predictor_cols = predictor_cols
                self.single_factor_analysis = single_factor_analysis
            features_after_corr_analysis = csf.runCorrelationAnalysis(self.df_train, self.predictor_cols, self.single_factor_analysis
                                                         , self.correlation_threshold, self.correlation_result_path)
            pd.DataFrame({'Variable': features_after_corr_analysis}).to_excel(self.feat_af_corr_anal_path, index=False)

# 4. Fourth Step
features_after_backward_elimination = None

class FourthStep():
    def __init__(self, dependent_col, features_after_corr_analysis, df_train
                 , backward_pvalue_threshold, vif_threshold, beta_threshold, feat_af_feat_elim_path):
        self.dependent_col = dependent_col
        self.final_kept_features = features_after_corr_analysis
        self.df_train = df_train
        self.backward_pvalue_threshold = backward_pvalue_threshold
        self.vif_threshold = vif_threshold
        self.beta_threshold = beta_threshold
        self.feat_af_feat_elim_path = feat_af_feat_elim_path

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self, separately=True):
        global features_after_backward_elimination
        if not self.skipped:
            if separately:
                global df_train
                global features_after_corr_analysis
                df_train = pd.read_excel(gms.train_destination_path)
                features_after_corr_analysis = list(pd.read_excel(gmt.feat_af_corr_anal_path)['Variable'])
                self.df_train = df_train
                self.final_kept_features = features_after_corr_analysis
            features_after_backward_elimination = fsf.FeaturesElimination(self.dependent_col, self.final_kept_features
                                                                          , self.df_train).StepsBaseElimination(self.backward_pvalue_threshold
                                                                                                                , self.vif_threshold, self.beta_threshold
                                                                                                                , 'backward').final_kept_features
            pd.DataFrame({'Variable': features_after_backward_elimination}).to_excel(self.feat_af_feat_elim_path, index=False)

# 5. Fifth Step
class FifthStep():
    def __init__(self, dependent_col, kept_features, df_train, df_test, min_number, max_number, pvalue_threshold
                 , vif_threshold, beta_threshold, model_performance_path, model_coefficient_path):
        self.dependent_col = dependent_col
        self.kept_features = kept_features
        self.df_train = df_train
        self.df_test = df_test
        self.min_number = min_number
        self.max_number = max_number
        self.pvalue_threshold = pvalue_threshold
        self.vif_threshold = vif_threshold
        self.beta_threshold = beta_threshold
        self.model_performance_path = model_performance_path
        self.model_coefficient_path = model_coefficient_path

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self, separately=True):
        if not self.skipped:
            if separately:
                global df_train
                global df_test
                global features_after_backward_elimination
                df_train = pd.read_excel(gms.train_destination_path)
                df_test = pd.read_excel(gms.test_destination_path)
                features_after_backward_elimination = list(pd.read_excel(gmft.feat_af_feat_elim_path)['Variable'])
                self.df_train = df_train
                self.df_test = df_test
                self.kept_features = features_after_backward_elimination
            ssf.exportScenarios(self.dependent_col, self.kept_features, self.min_number, self.max_number, self.df_train, self.df_test, self.pvalue_threshold,
                            self.vif_threshold, self.beta_threshold, self.model_performance_path, self.model_coefficient_path)

# 5. Fifth Step
class SixthStep():
    def __init__(self, df_train, df_test, dependent_col, model_performance_path, model_coefficient_path
                  , test_sampling_percent, iteration, bootstrapping_performance_path):
        self.df_train = df_train
        self.df_test = df_test
        self.dependent_col = dependent_col
        self.model_performance_path = model_performance_path
        self.model_coefficient_path = model_coefficient_path
        self.test_sampling_percent = test_sampling_percent
        self.iteration = iteration
        self.bootstrapping_performance_path = bootstrapping_performance_path

    def skip(self, res=True):
        self.skipped = res
        return self

    def run(self, separately=True):
        if not self.skipped:
            if separately:
                global df_train
                global df_test
                df_train = pd.read_excel(gms.train_destination_path)
                df_test = pd.read_excel(gms.test_destination_path)
                self.df_train = df_train
                self.df_test = df_test
            model_performance = pd.read_csv(self.model_performance_path, delimiter='|')
            model_coefficient = pd.read_csv(self.model_coefficient_path, delimiter='|')
            bootstrap_model_ids = list(model_performance['model_id'])
            bsf.BootStrapping(self.df_train, self.df_test, self.dependent_col, model_performance, model_coefficient
                          , bs_sample_prop=self.test_sampling_percent, iteration=self.iteration, model_ids=bootstrap_model_ids).to_excel(self.bootstrapping_performance_path, index=False)

# All steps
class Steps():
    def __init__(self, selected_steps, all_steps):
        self.selected_steps = selected_steps
        self.all_steps = all_steps

    def findSkippedSteps(self, skipped_steps={}):
        for head in self.all_steps:
            if head in self.selected_steps:
                skipped_steps[head] = False
            else:
                skipped_steps[head] = True
        return skipped_steps

    def findDependentPairs(self, dependent_pairs={}):
        print('Initial Steps List: ', self.all_steps)
        for pos in range(len(self.all_steps)):
            if pos == 0:
                dependent_pairs[self.all_steps[pos]] = None
            else:
                dependent_pairs[self.all_steps[pos]] = self.all_steps[pos-1]
        return dependent_pairs

    def findSeparateRunSteps(self):
        dependent_pairs = self.findDependentPairs()
        separate_steps = {}
        for step in self.all_steps:
            if step not in self.selected_steps:
                separate_steps[step] = None
            elif dependent_pairs[step] in self.selected_steps:
                separate_steps[step] = False
            else:
                separate_steps[step] = True
        return separate_steps

    def scenarios(self):
        self.is_skipped = self.findSkippedSteps()
        self.is_separate = self.findSeparateRunSteps()
        print('Skipped Steps: ', self.is_skipped)
        print('Separate Steps: ', self.is_separate)
        return self

    def run(self):
        try:
            # Step 1:
            print('[Multivariate Regression] has been started!')
            print('-'*20)
            print('[Step 1] has been started!')
            FirstStep(gmf.variables_list_path,
                      gmf.binning_result_path,
                      fss.special_values,
                      gmf.destination_path_1)\
                .skip(self.is_skipped[self.all_steps[0]])\
                .run()
            print('[Step 1] has completed succesfully!')

            # Step 2:
            print('[Step 2] has been started!')
            SecondStep(gms.df_train_path,
                       gms.df_test_path,
                       ui.dependent_col,
                       ui.excluded_cols,
                       single_factor_analysis,
                       gms.train_destination_path,
                       gms.test_destination_path)\
                .skip(self.is_skipped[self.all_steps[1]])\
                .run(self.is_separate[self.all_steps[1]])
            print('[Step 2] has completed succesfully!')

            # Step 3:
            print('[Step 3] has been started!')
            ThirdStep(df_train,
                       predictor_cols,
                       single_factor_analysis,
                       gmt.correlation_threshold,
                       gmt.correlation_result_path,
                       gmt.feat_af_corr_anal_path) \
                .skip(self.is_skipped[self.all_steps[2]]) \
                .run(self.is_separate[self.all_steps[2]])
            print('[Step 3] has completed succesfully!')

            # Step 4:
            print('[Step 4] has been started!')
            FourthStep(ui.dependent_col,
                       features_after_corr_analysis,
                       df_train,
                       gmft.backward_pvalue_threshold,
                       gmft.vif_threshold,
                       gmft.beta_threshold,
                       gmft.feat_af_feat_elim_path) \
                .skip(self.is_skipped[self.all_steps[3]]) \
                .run(self.is_separate[self.all_steps[3]])
            print('[Step 4] has completed succesfully!')

            # Step 5:
            print('[Step 5] has been started!')
            FifthStep(ui.dependent_col,
                       features_after_backward_elimination,
                       df_train,
                       df_test,
                       gmff.min_number,
                       gmff.max_number,
                       gmff.pvalue_threshold,
                       gmff.vif_threshold,
                       gmff.beta_threshold,
                       gmff.model_performance_path,
                       gmff.model_coefficient_path) \
                .skip(self.is_skipped[self.all_steps[4]]) \
                .run(self.is_separate[self.all_steps[4]])
            print('[Step 5] has completed succesfully!')

            # Step 6:
            print('[Step 6] has been started!')
            SixthStep(df_train,
                      df_test,
                      ui.dependent_col,
                      gmff.model_performance_path,
                      gmff.model_coefficient_path,
                      gmsx.test_sampling_percent,
                      gmsx.iteration,
                      gmsx.bootstrapping_performance_path) \
                .skip(self.is_skipped[self.all_steps[5]]) \
                .run(self.is_separate[self.all_steps[5]])
            print('[Step 6] has completed succesfully!')
            print('-' * 20)
            print('[Multivariate Regression] has been completed successfully!')
        except Exception as error:
            messagebox.showinfo(title='Error', message=error)