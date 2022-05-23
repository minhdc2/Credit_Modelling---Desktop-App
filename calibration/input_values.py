import pandas as pd

calibration_model_id = '1.2.3.4.5.6.7.8.9.10.11.16.19.20.22.23'

# change segment value
odr_results = pd.read_excel('D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\input\\odr_results.xlsx')
odr_results = odr_results.loc[odr_results['SEGMENT_V5A']=='1. Small SME',['NGANH FINAL','ODR']]

ajusted_pd_train_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output\\train_dataset_after_adjusted_pd.xlsx'
ajusted_pd_test_path = 'D:\\2. F\\PwC\\0. Risk Consulting\\ACB\\output\\test_dataset_after_adjusted_pd.xlsx'