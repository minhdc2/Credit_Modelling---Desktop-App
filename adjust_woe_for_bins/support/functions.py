# 0. Import packages
import pandas as pd
import numpy as np
from datetime import datetime

# A. Technical WoE Address
def runTechnicalProcess(variables_list_path, binning_result_path, special_values, destination_path):
    begin_time = datetime.now()
    features_list = pd.read_excel(variables_list_path)
    binning_result = pd.read_excel(binning_result_path)
    single_factor_analysis = AdjustWoE(binning_result, features_list, special_values).saveToExcel(destination_path)
    end_time = datetime.now()
    complete_time = (end_time - begin_time).total_seconds()
    print('Technical WoE process was completed!')
    print('Duration: ' + str(complete_time) + 's.')
    return single_factor_analysis

def filter_df(features_list, filter_dict):
    filter_cols = list(filter_dict.keys())
    filtered_df = features_list.copy()
    for i in filter_cols:
        filter_condition = filter_dict[i]
        filtered_df = filtered_df[filtered_df[i] == filter_condition]
    filtered_df = filtered_df.drop_duplicates()
    return filtered_df


def get_solution(filtered_df, solution_col):
    solution_list = list(filtered_df[solution_col].values)
    if len(solution_list) == 1:
        solution_scenario = solution_list[0]
    return solution_scenario


def isSpecialValue(bin, special_values):
    right_value = bin[bin.find(','):]
    left_value = bin[:bin.find(',')]
    answer = False
    for special_value in list(special_values.keys()):
        if str(special_value) in right_value or special_value == bin or ('inf' in right_value and str(special_value) in left_value):
            answer = True
            break
    return answer


def doesBinHaveOver30Bad(feature, bin, binning_result):
    bin_row = binning_result[(binning_result['Variable'] == feature) & (binning_result['Bin'] == bin)]
    bad_cnt_list = list(bin_row['No Bad'])
    if len(bad_cnt_list) == 1:
        bad_cnt = bad_cnt_list[0]
        if bad_cnt > 30:
            answer = True
        else:
            answer = False
    return answer


class TechnicalSingleBinProcess:
    def __init__(self, feature, bin, binning_result, special_values):
        self.feature = feature
        self.bin = bin
        self.binning_result = binning_result
        self.special_values = special_values

    def getOriginalRow(self):
        woe_row = self.binning_result[
            (self.binning_result['Variable'].str.upper() == self.feature.upper()) & (
                        self.binning_result['Bin'] == self.bin)]
        woe_list = list(woe_row['WOE'])
        woe_org = woe_list[0]
        return (self.feature, self.bin, woe_org)

    def neutralCase(self):
        woe_row = self.binning_result[
            (self.binning_result['Variable'] == self.feature.upper()) & (self.binning_result['Bin'] == self.bin)]
        if not doesBinHaveOver30Bad(self.feature, self.bin, self.binning_result) and isSpecialValue(self.bin,
                                                                                                    self.special_values):
            woe_adj = 0
        else:
            woe_list = list(woe_row['WOE'])
            woe_adj = woe_list[0]
        return (self.feature, self.bin, woe_adj)

    def bestCase(self):
        woe_row = self.binning_result[
            (self.binning_result['Variable'].str.upper() == self.feature.upper()) & (
                        self.binning_result['Bin'] == self.bin)]
        woe_list = list(woe_row['WOE'])
        woe_org = woe_list[0]
        if not doesBinHaveOver30Bad(self.feature, self.bin, self.binning_result) and isSpecialValue(self.bin,
                                                                                                    self.special_values):
            woe_adj = TechnicalSingleFactorProcess(self.feature, self.binning_result, self.special_values).findBestWoE()
        else:
            woe_adj = woe_org
        return (self.feature, self.bin, woe_adj)

    def worstCase(self):
        woe_row = self.binning_result[
            (self.binning_result['Variable'].str.upper() == self.feature.upper()) & (
                        self.binning_result['Bin'] == self.bin)]
        woe_list = list(woe_row['WOE'])
        woe_org = woe_list[0]
        if not doesBinHaveOver30Bad(self.feature, self.bin, self.binning_result) and isSpecialValue(self.bin,
                                                                                                    self.special_values):
            woe_adj = TechnicalSingleFactorProcess(self.feature, self.binning_result,
                                                   self.special_values).findWorstWoE()
        else:
            woe_adj = woe_org
        return (self.feature, self.bin, woe_adj)

    def missingBest_negative92Neutral(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if self.bin == 'Missing':
            row = self.bestCase()
        if '-999992' in right_value:
            row = self.neutralCase()
        return row

    def worst_97Best(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if ', 999997' in right_value:
            row = self.bestCase()
        else:
            row = self.worstCase()
        return row

    def neutral_97Best(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if ', 999997' in right_value:
            row = self.bestCase()
        else:
            row = self.neutralCase()
        return row

    def neutral_97Worst(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if ', 999997' in right_value:
            row = self.worstCase()
        else:
            row = self.neutralCase()
        return row

    def neutral_9798Worst(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if '999997' in right_value or '999998' in right_value:
            row = self.worstCase()
        else:
            row = self.neutralCase()
        return row

    def worst_97Neutral(self):
        row = self.getOriginalRow()
        right_value = self.bin[self.bin.find(','):]
        if ', 999997' in right_value:
            row = self.neutralCase()
        else:
            row = self.worstCase()
        return row


class TechnicalSingleFactorProcess:
    def __init__(self, feature, binning_result, special_values):
        self.feature = feature
        self.binning_result = binning_result
        self.special_values = special_values

    def findBestWoE(self):
        bin_woe_pairs = list(
            self.binning_result[self.binning_result['Variable'].str.upper() == self.feature.upper()][
                ['Bin', 'WOE']].values)
        unspecial_WoEs = []
        for bin_woe in bin_woe_pairs:
            if not isSpecialValue(bin_woe[0], self.special_values):
                unspecial_WoEs.append(bin_woe[1])
        max_WoE = max(unspecial_WoEs)
        best_woe = list(self.binning_result[(self.binning_result['Variable'].str.upper() == self.feature.upper()) & (
                self.binning_result['WOE'] == max_WoE)]['WOE'].values)[0]
        return best_woe

    def findWorstWoE(self):
        bin_badRate_pairs = list(
            self.binning_result[self.binning_result['Variable'].str.upper() == self.feature.upper()][
                ['Bin', 'WOE']].values)
        unspecial_WoEs = []
        for bin_badRate in bin_badRate_pairs:
            if not isSpecialValue(bin_badRate[0], self.special_values):
                unspecial_WoEs.append(bin_badRate[1])
        min_WoE = min(unspecial_WoEs)
        best_woe = list(self.binning_result[(self.binning_result['Variable'].str.upper() == self.feature.upper()) & (
                self.binning_result['WOE'] == min_WoE)]['WOE'].values)[0]
        return best_woe

    def WoEAdjusted(self, solution_scenario):
        bins = list(self.binning_result[self.binning_result['Variable'] == self.feature]['Bin'])
        single_feature_rows = []
        if isinstance(solution_scenario, float) and np.isnan(solution_scenario):
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.getOriginalRow()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Worst, 97: neutral':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.worst_97Neutral()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Neutral, 97 98 worst':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.neutral_9798Worst()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Neutral, 97 worst':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.neutral_97Worst()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Neutral, 97 best':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.neutral_97Best()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Missing Best, -92 neutral':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.missingBest_negative92Neutral()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Worst, 97 best':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.worst_97Best()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Best':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.bestCase()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Neutral':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.neutralCase()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        if solution_scenario == 'Worst':
            for bin in bins:
                class_ = TechnicalSingleBinProcess(self.feature, bin, self.binning_result, self.special_values)
                row = class_.worstCase()
                print(f"Step 1: ({row[0]}, {row[1]}, {row[2]})")
                single_feature_rows.append(row)
        return single_feature_rows


class AdjustWoE:
    def __init__(self, binning_result, features_list, special_values):
        self.binning_result = binning_result
        self.features_list = features_list
        self.special_values = special_values

    def allFeatures(self):
        self.binning_result['Variable'] = self.binning_result['Variable'].str.upper()
        self.features_list['Tên biến'] = self.features_list['Tên biến'].str.upper()
        features = np.unique(list(self.binning_result['Variable']))
        all_feature_rows = []
        for single_feature in features:
            filter_dict = {
                'Kết luận cuối cùng': 'Keep',
                'Tên biến': single_feature
            }
            filtered_df = filter_df(self.features_list, filter_dict)
            if not filtered_df.empty:
                solution_scenario = get_solution(filtered_df, 'Xử lý kỹ thuật')
                single_feature_rows = TechnicalSingleFactorProcess(single_feature, self.binning_result
                                                                   , self.special_values).WoEAdjusted(solution_scenario)
                all_feature_rows += single_feature_rows
        return all_feature_rows

    def addColumn(self):
        woe_adjusted_rows = self.allFeatures()
        woe_adjusted_df = pd.DataFrame(woe_adjusted_rows, columns=['Variable', 'Bin', 'WOE_Adjusted'])
        woe_adjusted_df = pd.merge(self.binning_result, woe_adjusted_df, how='inner', on=['Variable', 'Bin'],
                                   suffixes=['', '_y'])
        return woe_adjusted_df

    def saveToExcel(self, destination_path):
        woe_adjusted_df = self.addColumn()
        woe_adjusted_df.to_excel(destination_path, index=False)
        return woe_adjusted_df
