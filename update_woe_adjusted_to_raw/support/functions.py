import pandas as pd
import numpy as np
from datetime import datetime

class Collection:
    def __init__(self, a_list):
        self.a_list = a_list
    def show(self):
        return self.a_list
    def exclude(self, another_list):
        self.a_list = [kept_col for kept_col in self.a_list if kept_col not in another_list]
        return self

def upperColumnName(df):
    cols = list(df.columns)
    uppered_cols = {old_name: old_name.upper() for old_name in cols}
    df_train = df.rename(columns = uppered_cols)
    return df_train

def getLeftRightValues(bin):
    if ',' in bin:
        if bin[0] == '(':
            bin = bin[1:]
        if bin[-1:] == ']':
            bin = bin[:-1]
        com_pos = bin.find(',')
        left_value = bin[:com_pos]
        right_value = bin[(com_pos + 2):]
    else:
        left_value, right_value = bin, bin
    return left_value, right_value

class HandleDataType:
    def __init__(self, org_values, bin_woe_adj_pairs):
        self.org_values = org_values
        self.bin_woe_adj_pairs = bin_woe_adj_pairs

    def replaceNumericValues(self):
        woe_adj_values = []
        for org_value in self.org_values:
            for bin_woe_adj_pair in self.bin_woe_adj_pairs:
                bin = bin_woe_adj_pair[0]
                left_value, right_value = getLeftRightValues(bin)
                if left_value != right_value:
                    if org_value > float(left_value) and org_value <= float(right_value): # -inf, inf can be solved
                        woe_adj = bin_woe_adj_pair[1]
                        break
                    else:
                        woe_adj = np.nan
                elif right_value == 'Missing':
                    if np.isnan(org_value) == True:
                        woe_adj = bin_woe_adj_pair[1]
                        break
                    else:
                        woe_adj = np.nan
                else:
                    if org_value == float(right_value) or str(org_value) == str(right_value):
                        woe_adj = bin_woe_adj_pair[1]
                    else:
                        woe_adj = np.nan
            woe_adj_values.append(woe_adj)
        return woe_adj_values

    def replaceStringValues(self):
        woe_adj_values = []
        for org_value in self.org_values:
            if isinstance(org_value, str) == True:
                for bin_woe_adj_pair in self.bin_woe_adj_pairs:
                    if org_value in bin_woe_adj_pair[0].replace(u'\xa0', u' '):
                        woe_adj = bin_woe_adj_pair[1]
                        break
                    else:
                        woe_adj = np.nan
            elif isinstance(org_value, float) == True:
                if np.isnan(org_value) == True:
                    for bin_woe_adj_pair in self.bin_woe_adj_pairs:
                        if bin_woe_adj_pair[0] == 'Missing':
                            woe_adj = bin_woe_adj_pair[1]
                            break
                        else:
                            woe_adj = np.nan
                else:
                    woe_adj = np.nan
            else:
                woe_adj = np.nan
            woe_adj_values.append(woe_adj)
        return woe_adj_values

class UpdateWoEAdjustedToRaw:
    def __init__(self, predictor_cols, df_train_raw, single_factor_analysis):
        self.predictor_cols = predictor_cols
        self.df_train_raw = df_train_raw
        self.single_factor_analysis = single_factor_analysis

    def updateFeatureColumns(self):
        begin_time = datetime.now()
        df_train = self.df_train_raw.copy()
        for feature in self.predictor_cols:
            print(f'Step 2: {feature}')
            org_values = list(df_train[feature])
            bin_woe_adj_pairs = self.single_factor_analysis[self.single_factor_analysis['Variable'] == feature][['Bin', 'WOE_Adjusted']].values
            col_type = df_train[feature].dtypes
            if col_type == np.dtype('float') or col_type == np.dtype('int') or col_type == np.dtype('int64'):
                if len(bin_woe_adj_pairs) > 0:
                    woe_adj_values = HandleDataType(org_values, bin_woe_adj_pairs).replaceNumericValues()
                    df_train[feature] = woe_adj_values
            if col_type == np.dtype('O'):
                if 'Ngưỡng' in list(self.single_factor_analysis.columns):
                    bin_woe_adj_pairs = self.single_factor_analysis[self.single_factor_analysis['Variable'] == feature][['Ngưỡng', 'WOE_Adjusted']].values
                if len(bin_woe_adj_pairs) > 0:
                    woe_adj_values = HandleDataType(org_values, bin_woe_adj_pairs).replaceStringValues()
                    df_train[feature] = woe_adj_values
        end_time = datetime.now()
        complete_time = (end_time - begin_time).total_seconds()
        print('WoE Adjusted was updated to raw dataset!')
        print('Duration: ' + str(complete_time) + 's.')
        return df_train

    def saveToExcel(self, destination_path):
        df_train = self.updateFeatureColumns()
        df_train.to_excel(destination_path, index = False)
        return df_train

def runUpdateWoEAdjusted(df_train_path, dependent_col, excluded_cols, single_factor_analysis
                         , destination_path):
    df_train_raw = pd.read_csv(df_train_path)
    df_train_raw = upperColumnName(df_train_raw)
    all_cols = list(df_train_raw.columns)
    predictor_cols = Collection(all_cols).exclude(dependent_col + excluded_cols).show()
    df_train = UpdateWoEAdjustedToRaw(predictor_cols, df_train_raw, single_factor_analysis)\
        .saveToExcel(destination_path)
    return df_train, all_cols, predictor_cols
