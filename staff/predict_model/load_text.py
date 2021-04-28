# 尝试保存模型，不要每次都训练了：

import joblib
import pandas as pd
import numpy as np

#load model
test_data = joblib.load('saved_model/test_data.sav')
lr2 = joblib.load('saved_model/rfc.pkl')
# print(test_data.iloc[1])
print(type(test_data))
print(type(test_data.values))
print(test_data.values.shape)
print(len(test_data.values[1, :]))
a = []
a.append(test_data.values[1, :])
print(lr2.predict(a))

# print(test_data.iloc[0].values)
# print(lr2.predict(test_data.iloc[0].values.ravel()))
# pd.set_option('display.max_columns', None)  # 显示所有列
# fal_rst = lr2.predict(test_data.values)
# print(type(fal_rst))
# print(fal_rst.shape)

