import numpy as np
import pandas as pd
from staff.models import StaffClean
# # 特征标准化
# from sklearn.preprocessing import StandardScaler
#
# class DataClean:
#     def __init__(self, member_id):
#         self.loan_data = LoanData.objects.filter(member_id=member_id)
#
#     # def logistic_clean(self):
#
#
# "1288686"
querySet = StaffClean.objects.filter(member_id='1311441').values()
#
# # querySet = LoanData.objects.all().values()
data = pd.DataFrame(list(querySet))
u_d = ['id','loan_status','member_id']
for i in u_d:
    del data[i]
print(data.shape)
print(data)
import joblib
lr2 = joblib.load('saved_model/rfc.pkl')
print(lr2.predict(data))


from staff.models import Profile
from staff.models import User
from django.contrib.auth import authenticate
#
# u = authenticate(username='chen', password='chen')
# p = Profile.objects.get(user_id=u.id)
# print(p.is_first_login)

