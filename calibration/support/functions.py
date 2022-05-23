from features_elimination.support.functions import *

def ODR_calculation(df_population, calibration_factors, dependent_col, cut_off_time, reference_date,
                    time_frequency=None):
    cut_off_time = pd.to_datetime(cut_off_time)
    df_population['QUARTER'] = pd.DatetimeIndex(df_population[reference_date[0]]).quarter
    df_population['YEAR'] = pd.DatetimeIndex(df_population[reference_date[0]]).year

    if time_frequency == 'year':
        calibration_group = calibration_factors + ['YEAR']
    elif time_frequency == 'quarter':
        calibration_group = calibration_factors + ['QUARTER', 'YEAR']
    elif time_frequency == 'month':
        calibration_group = calibration_factors + [reference_date]
    else:
        calibration_group = calibration_factors

    if time_frequency:
        odr_smr_over_time = df_population.groupby(calibration_group).agg(
            {dependent_col[0]: ['mean', 'sum', 'count']}).reset_index()

    odr_over_time = df_population.groupby(calibration_group).agg({dependent_col[0]: 'mean'}).reset_index()
    odr_by_group = odr_over_time.groupby(calibration_factors).agg({dependent_col[0]: 'mean'}).reset_index()
    odr_by_group = odr_by_group.rename(columns={dependent_col[0]: 'ODR'})
    print(odr_by_group)
    if time_frequency:
        return odr_by_group, odr_smr_over_time
        print(odr_smr_over_time)
    else:
        return odr_by_group


def PDCalibration(df_path, df_train_path, model_id, calibration_odr, dependent_col, coefficient_table_name):
    df = pd.read_excel(df_path)
    df_train = pd.read_excel(df_train_path)

    calibration_factors = list(calibration_odr.columns[:-1])
    sdr = df_train[dependent_col + calibration_factors].groupby(calibration_factors).agg({dependent_col[0]: 'mean'}).reset_index()
    sdr = sdr.rename(columns={dependent_col[0]: 'SDR'})
    offset = calibration_odr.merge(sdr, on=calibration_factors, how='inner')
    offset['OFFSET'] = np.log((offset['SDR'] * (1 - offset['ODR'])) / (offset['ODR'] * (1 - offset['SDR'])))
    features_list = list(coefficient_table_name[(coefficient_table_name['model_id'] == model_id) & (
            coefficient_table_name['variable'] != 'Intercept')]['variable'])

    predicted_probs_dict = LogisticModel(dependent_col, features_list, df_train).getPDPredicted(df)

    df['ESTIMATE_PD'] = predicted_probs_dict[1]
    df = df.merge(offset, on=calibration_factors, how='inner')
    df['ODDS'] = (df['ESTIMATE_PD']) / (1 - df['ESTIMATE_PD'])
    df['SCORE'] = np.log(df['ODDS'])

    df['ADJUSTED_PD'] = 1 / (1 + np.exp(-df['SCORE'] + df['OFFSET']))

    return offset, df[calibration_factors + ['APP_ID', 'ESTIMATE_PD', 'ODDS', 'SCORE', 'ADJUSTED_PD']]