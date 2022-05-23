import pandas as pd
import numpy as np
from features_elimination.support.functions import *

def BootStrapping(df_train, df_test, dependent_col, performance_table_name, coefficient_table_name
                  , bs_sample_prop=0.8, iteration=100, top_models=None, model_ids=None):
    bad_list_test = list(df_test[dependent_col[0]])
    pd_portfolio_test = sum(bad_list_test) / len(bad_list_test)
    n_sample = int(bs_sample_prop * len(df_test))
    if top_models:
        top_model_info = performance_table_name.sort_values(by = 'auc_score_test', ascending = False).head(top_models)
        model_ids = list(np.unique(top_model_info['model_id']))
    elif model_ids==None:
        print('Define top models or list of model ids')
        return

    bs_results = []
    for model_id in model_ids:
        features_list = list(coefficient_table_name[(coefficient_table_name['model_id']==model_id)&(coefficient_table_name['variable']!='Intercept')]['variable'])
        auc_bs_value = []
        gini_bs_value = []
        lift_bs_value = []

        for i in range(0, iteration):
            print(f'Step 6: {model_id}, iteration: {str(i)}')
            df_test_bs = df_test.sample(n=n_sample, random_state=i)

            auc_score_test = LogisticModel(dependent_col, features_list, df_train).getAUCScore(df_test_bs)  # AUC score test
            auc_bs_value.append(auc_score_test)
            gini_test = 2 * auc_score_test - 1  # Gini test
            gini_bs_value.append(gini_test)
            lift_test = LogisticModel(dependent_col, features_list, df_train).getPDWorstGroup(df_test, 10)/pd_portfolio_test  # Lift test
            lift_bs_value.append(lift_test)

        auc_score_avg = sum(auc_bs_value) / iteration
        auc_score_min = min(auc_bs_value)
        auc_score_max = max(auc_bs_value)

        gini_avg = sum(gini_bs_value) / iteration
        gini_min = min(gini_bs_value)
        gini_max = max(gini_bs_value)

        lift_avg = sum(lift_bs_value) / iteration
        lift_min = min(lift_bs_value)
        lift_max = max(lift_bs_value)

        bs_result = {'model_id': model_id
                     , 'auc_score_min': auc_score_min, 'auc_score_avg': auc_score_avg, 'auc_score_max': auc_score_max
                     , 'gini_min': gini_min, 'gini_avg': gini_avg, 'gini_max': gini_max
                     , 'lift_min': lift_min, 'lift_avg': lift_avg, 'lift_max': lift_max}
        bs_results.append(bs_result)
    bs_results = pd.DataFrame(bs_results)
    return bs_results