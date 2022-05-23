# 0. Import packages
import pandas as pd
import numpy as np

def runCorrelationAnalysis(df_train, predictor_cols, single_factor_analysis, threshold, correlation_result_path):
    df_train, predictor_cols, single_factor_analysis
    result_set = CorrelationAnalysis(df_train, predictor_cols, single_factor_analysis).saveToExcel(threshold, correlation_result_path)
    final_kept_features = result_set[0]
    print('There are ' + str(len(final_kept_features)) + ' left after correlation analysis.')
    return final_kept_features

def correlation(df_train, option):
    corr_matrix = df_train.corr(method = option).unstack().reset_index().values
    corr_matrix_df = pd.DataFrame(corr_matrix, columns = ['Variable1', 'Variable2', 'corr_value'])
    return corr_matrix_df

def getIV(feature, single_factor_analysis):
    print(f'Step 3: {feature}')
    filtered_df = single_factor_analysis[single_factor_analysis['Variable'] == feature]
    IV_list = np.unique(list(filtered_df['IV Report']))
    if len(IV_list) == 1:
        IV_value = IV_list[0]
    if len(IV_list) == 0:
        IV_value = 0
    return IV_value

def findExludedAndKeptFeatures(vl_cols, thres_vl_pairs, single_factor_analysis, kept_features = [], exluded_features = []):
    if len(vl_cols) > 0:
        vl_col_head, vl_cols = vl_cols[0], vl_cols[1:]
        paired_cols = [pair[1] for pair in thres_vl_pairs if pair[0] == vl_col_head]
        if len(paired_cols) > 0:
            paired_cols_IV = [getIV(feature, single_factor_analysis) for feature in paired_cols]
            vl_col_IV = getIV(vl_col_head, single_factor_analysis)
            if vl_col_IV <= max(paired_cols_IV):
                exluded_features.append(vl_col_head)
                # thres_vl_pairs = [pair for pair in thres_vl_pairs if pair[0] != vl_col_head and pair[1] != vl_col_head]
                kept_features, excluded_features = findExludedAndKeptFeatures(vl_cols, thres_vl_pairs, single_factor_analysis, kept_features, exluded_features)
            else:
                kept_features.append(vl_col_head)
                kept_features, excluded_features = findExludedAndKeptFeatures(vl_cols, thres_vl_pairs, single_factor_analysis, kept_features, exluded_features)
        else:
            kept_features.append(vl_col_head)
            kept_features, excluded_features = findExludedAndKeptFeatures(vl_cols, thres_vl_pairs,single_factor_analysis, kept_features, exluded_features)
    return kept_features, exluded_features

class CorrelationAnalysis:
    def __init__(self, df_train, predictor_cols, single_factor_analysis):
        self.df_train = df_train
        self.predictor_cols = predictor_cols
        self.single_factor_analysis = single_factor_analysis

    def singleCorrelationResult(self, option, threshold):
        selected_cols = np.unique(list(self.single_factor_analysis['Variable']))
        predictor_cols = [col for col in self.predictor_cols if col in selected_cols]
        selected_df = self.df_train[predictor_cols]
        corr_matrix_df = correlation(selected_df, option)
        thres_vl_df = corr_matrix_df[corr_matrix_df['corr_value'].abs() > threshold][['Variable1', 'Variable2']].drop_duplicates()
        thres_vl_pairs = [list(a_pair) for a_pair in thres_vl_df.values if a_pair[0] != a_pair[1]]
        vl_cols = np.unique([pair[0] for pair in thres_vl_pairs])
        kept_features, excluded_features = findExludedAndKeptFeatures(vl_cols, thres_vl_pairs, self.single_factor_analysis, [], [])
        return corr_matrix_df, kept_features, excluded_features

    def combinedCorrelationResult(self, threshold):
        option_1 = 'pearson'
        pearson_before, _, excluded_features_1 = self.singleCorrelationResult(option_1, threshold)
        option_2 = 'spearman'
        spearman_before, _, excluded_features_2 = self.singleCorrelationResult(option_2, threshold)
        features_IV_list = [list(pair) for pair in self.single_factor_analysis[['Variable', 'IV Report']].drop_duplicates().values]
        features_IV_list = [pair for pair in features_IV_list if pair[0] in list(self.df_train.columns)]
        col_list = []
        variable_col = [pair[0] for pair in features_IV_list]
        IV_col = [pair[1] for pair in features_IV_list]
        pearson_col = [0 if pair[0] in excluded_features_1 else 1 for pair in features_IV_list]
        spearman_col = [0 if pair[0] in excluded_features_2 else 1 for pair in features_IV_list]
        corr_keep = [1 if i == 1 and j == 1 else 0 for i, j in zip(pearson_col, spearman_col)]
        col_list.append(variable_col)
        col_list.append(IV_col)
        col_list.append(pearson_col)
        col_list.append(spearman_col)
        col_list.append(corr_keep)
        corr_result_df = pd.DataFrame(np.array(col_list).T, columns = ['Variable', 'IV Report', 'pearson_keep', 'spearman_keep', 'corr_keep'])
        final_kept_features = list(corr_result_df[corr_result_df['corr_keep'] == '1']['Variable'])
        pearson_after = correlation(self.df_train[final_kept_features], option_1)
        spearman_after = correlation(self.df_train[final_kept_features], option_2)
        return final_kept_features, corr_result_df, pearson_before, pearson_after, spearman_before, spearman_after

    def saveToExcel(self, threshold, correlation_result_path):
        result_set = self.combinedCorrelationResult(threshold)
        sheet_names = ['correlation_result', 'pearson_(before)', 'pearson_(after)', 'spearman_(before)', 'spearman_(after)']
        # Save to Excel file
        opened_Excel = pd.ExcelWriter(correlation_result_path)
        for i, j in zip(result_set[1:], sheet_names):
            i.to_excel(opened_Excel, engine = 'xlsxwriter', sheet_name = j, index = False)
        opened_Excel.save()
        return result_set
