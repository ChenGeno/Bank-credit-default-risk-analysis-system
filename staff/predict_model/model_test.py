from staff.models import Approval
from staff.models import Profile
from staff.models import User
from staff.models import StaffLoan

# approval = Approval.objects.get(id=1)
#
# a= approval.get_relevant_loan()
# print(a)
# for i in a:
#     print(a[i])

approval_query = Approval.objects.order_by('update_time')[:2]  # limit 2
dash_form = []
for approval in approval_query:
    dash_form.append(approval.get_relevant_loan())
context = {'dash_form': dash_form}