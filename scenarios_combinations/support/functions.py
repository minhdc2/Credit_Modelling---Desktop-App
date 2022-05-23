import pandas as pd
import numpy as np
from datetime import datetime
import itertools
from math import comb
import math
from features_elimination.support.functions import *

def createModelID(features_list, feature_IDs):
    model_id = ''
    for feature in features_list:
        id = feature_IDs[feature]
        model_id = model_id + id + '.'
    model_id = model_id[:-1]
    return model_id

def countScenarios(min_number, max_number):
    tot_cnt = 0
    for i in list(range(min_number, max_number + 1)):
        tot_cnt += comb(max_number, i)
    return tot_cnt


def exportScenarios(dependent_col, final_kept_features, min_number, max_number, df_train, df_test, pvalue_threshold, vif_threshold, beta_threshold
                    , model_performance_path, model_coefficient_path):
    begin_time = datetime.now()
    feature_IDs = {}
    feature_IDs_reverse = {}
    id = 0
    for feature in final_kept_features:
        id += 1
        feature_IDs[feature] = str(id)
        feature_IDs_reverse[str(id)] = feature
    kept_features = list(feature_IDs.keys())
    bad_list_train = list(df_train['GB_NEXT24M'])
    pd_portfolio_train = sum(bad_list_train) / len(bad_list_train)
    bad_list_test = list(df_test['GB_NEXT24M'])
    pd_portfolio_test = sum(bad_list_test)/len(bad_list_test)
    cnt = 0
    tot_cnt = countScenarios(min_number, max_number)
    percent_20 = math.ceil(tot_cnt*0.2)
    percent_40 = math.ceil(tot_cnt * 0.4)
    percent_60 = math.ceil(tot_cnt * 0.6)
    percent_80 = math.ceil(tot_cnt * 0.8)
    print('Step 5: ' + str(tot_cnt) + ' scenarios has started!')
    with open(model_performance_path, 'w') as f1, open(model_coefficient_path, 'w') as f2:
        f1.write('model_id|pseudo_r2_squared|llr_p_value|log_likelihood_ratio|auc_score_train|auc_score_test|gini_train|gini_test|lift_train|lift_test|timestamp')
        f1.write('\n')
        f2.write('model_id|variable|coefficent|p_value|timestamp')
        f2.write('\n')
        for number_of_features in list(range(min_number, max_number + 1)):
            features_list_combinations = itertools.combinations(kept_features, number_of_features)
            for features_list in features_list_combinations:
                cnt += 1
                if cnt == percent_20:
                    print('20% scenarios was completed.')
                if cnt == percent_40:
                    print('40% scenarios was completed.')
                if cnt == percent_60:
                    print('60% scenarios was completed.')
                if cnt == percent_80:
                    print('80% scenarios was completed.')
                if cnt == tot_cnt:
                    print('100% scenarios was completed.')
                features_list = [feature for feature in features_list]
                model_id = createModelID(features_list, feature_IDs)
                result = LogisticModel(dependent_col, features_list, df_train).Logit()
                result_params = result.params  # coefficients
                result_pvalues = result.pvalues  # Variables p-value
                _, highest_param = findHighestBetaFeature(result_params)
                _, highest_pvalue = findHighestPvalueFeature(result_pvalues)
                _, highest_vif = findHighestVIFFeature(features_list, df_train)
                print('Step 5: ', highest_param, beta_threshold, highest_pvalue, pvalue_threshold, highest_vif, vif_threshold)
                if highest_param <= beta_threshold and highest_pvalue <= pvalue_threshold and highest_vif <= vif_threshold:
                    prsquared = result.prsquared  # Pseudo R-square
                    llr_pvalue = result.llr_pvalue  # LLR p-value
                    llr = result.llr  # Log-likelihood Ratio
                    auc_score_train = LogisticModel(dependent_col, features_list, df_train).getAUCScore(df_train) #AUC score train
                    gini_train = 2 * auc_score_train - 1 #Gini train
                    auc_score_test = LogisticModel(dependent_col, features_list, df_train).getAUCScore(df_test) # AUC score test
                    gini_test = 2 * auc_score_test - 1 #Gini test
                    lift_train = LogisticModel(dependent_col, features_list, df_train).getPDWorstGroup(df_train, 10)/pd_portfolio_train # Lift train
                    lift_test = LogisticModel(dependent_col, features_list, df_train).getPDWorstGroup(df_test, 10)/pd_portfolio_test # Lift test
                    time_stamp = str(datetime.now())
                    model_performance_row = (str(model_id), str(prsquared), str(llr_pvalue), str(llr), str(auc_score_train), str(auc_score_test), str(gini_train), str(gini_test), str(lift_train), str(lift_test), str(time_stamp))
                    f1.write('|'.join(model_performance_row))
                    f1.write('\n')
                    for feature in features_list + ['Intercept']:
                        coef = result_params[result_params.index == feature].values[0]
                        p_value = result_pvalues[result_pvalues.index == feature].values[0]
                        time_stamp = str(datetime.now())
                        model_coefficient_row = (str(model_id), str(feature), str(coef), str(p_value), str(time_stamp))
                        f2.write('|'.join(model_coefficient_row))
                        f2.write('\n')
    f1.close()
    f2.close()
    end_time = datetime.now()
    complete_time = (end_time - begin_time).total_seconds()
    print('Step 5: ' + str(cnt) + ' scenarios combinations was run completely.')
    print('Duration: ' + str(complete_time) + 's.')
    return complete_time

def saveTopModelsToExcel(top_models, train_destination_path, test_destination_path, model_performance_path, model_coefficient_path, top_models_destination_path):
    begin_time = datetime.now()
    dependent_col = ['GB_NEXT24M']
    df_train = pd.read_excel(train_destination_path)
    df_test = pd.read_excel(test_destination_path)
    models_performance_df = pd.read_csv(model_performance_path, sep = '|')
    models_coefficient_df = pd.read_csv(model_coefficient_path, sep = '|')
    top_scenarios_df = models_performance_df.sort_values(by='auc_score_test', ascending=False).iloc[:top_models]
    model_ids = list(top_scenarios_df['model_id'])
    file_id = 0
    for model_id in model_ids:
        model_performance_df = top_scenarios_df[top_scenarios_df['model_id'] == model_id]
        model_coefficient_df = models_coefficient_df[models_coefficient_df['model_id'] == model_id]
        features_list = [feature for feature in list(model_coefficient_df['variable']) if feature != 'Intercept']
        predicted_probs_train_dict = LogisticModel(dependent_col, features_list, df_train).getPDPredicted(df_train)
        predicted_probs_train_dict['APP_ID'] = list(df_train['APP_ID'])
        predicted_probs_train_dict[dependent_col[0]] = list(df_train[dependent_col[0]])
        pd_predicted_train_df = pd.DataFrame(predicted_probs_train_dict)

        predicted_probs_test_dict = LogisticModel(dependent_col, features_list, df_train).getPDPredicted(df_test)
        predicted_probs_test_dict['APP_ID'] = list(df_test['APP_ID'])
        predicted_probs_test_dict[dependent_col[0]] = list(df_test[dependent_col[0]])
        pd_predicted_test_df = pd.DataFrame(predicted_probs_test_dict)

        # Save to Excel file
        file_id += 1
        opened_Excel = pd.ExcelWriter(top_models_destination_path + 'model_' + str(file_id) + '.xlsx')
        model_performance_df.to_excel(opened_Excel, engine = 'xlsxwriter', sheet_name = 'model_performance', index = False)
        model_coefficient_df.to_excel(opened_Excel, engine = 'xlsxwriter', sheet_name = 'model_coefficient', index = False)
        pd_predicted_train_df.to_excel(opened_Excel, engine = 'xlsxwriter', sheet_name = 'pd_predicted_train', index = False)
        pd_predicted_test_df.to_excel(opened_Excel, engine = 'xlsxwriter', sheet_name = 'pd_predicted_test', index = False)
        opened_Excel.save()
    end_time = datetime.now()
    complete_time = (end_time - begin_time).total_seconds()
    print('Best models were exported completely.')
    print('Duration: ' + str(complete_time) + 's.')


