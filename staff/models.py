from django.db import models
from dataclasses import dataclass
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver


# Create your models here.
class Application(models.Model):
    # loan表主键，在这里做外键，该表与信贷表为一对一关系
    loan_id = models.CharField(max_length=20)
    # 申请人id, user表外键
    applicant_id = models.CharField(max_length=20)
    # 特征字段：
    loan_amnt = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    int_rate = models.CharField(max_length=20)
    sub_grade = models.CharField(max_length=20)
    emp_length = models.CharField(max_length=20)
    home_ownership = models.CharField(max_length=20)
    annual_inc = models.CharField(max_length=20)
    verification_status = models.CharField(max_length=20)
    purpose = models.CharField(max_length=20)
    dti = models.CharField(max_length=20)
    delinq_2yrs = models.CharField(max_length=20)
    inq_last_6mths = models.CharField(max_length=20)
    open_acc = models.CharField(max_length=20)
    pub_rec = models.CharField(max_length=20)
    revol_bal = models.CharField(max_length=20)
    revol_util = models.CharField(max_length=20)
    total_acc = models.CharField(max_length=20)
    initial_list_status = models.CharField(max_length=20)
    collections_12_mths_ex_med = models.CharField(max_length=20)
    acc_now_delinq = models.CharField(max_length=20)
    tot_coll_amt = models.CharField(max_length=20)
    tot_cur_bal = models.CharField(max_length=20)
    total_rev_hi_lim = models.CharField(max_length=20)



class Approval(models.Model):
    class IsPass(models.IntegerChoices):
        Under_review = 0
        Pass_review = 1
        Failed_review = 2
    # loan表主键，在这里做外键，该表与信贷表为一对一关系
    loan_id = models.CharField(max_length=20)
    # 会员号为profile表uk键，profile表与该表为1对n关系
    member_id = models.CharField(max_length=20)
    # user表主键，user表与该表为1对n关系（审批人）
    approver_id = models.CharField(max_length=20)
    # 审批进度
    approval_progress = models.IntegerField(default=0)
    # 审批状态
    is_pass_review = models.IntegerField(choices=IsPass.choices, default=0)
    create_time = models.DateField(auto_now=False, auto_now_add=True)  # 创建时间
    update_time = models.DateField(auto_now=True, auto_now_add=False)  # 最近一次修改时间

    def get_relevant_loan(self):
        # 获得member_id对应的profile
        profile = Profile.objects.get(member_id=self.member_id)
        # 根据profile获取到的user_id,得到user（从而获得用户名）
        user = User.objects.get(id=profile.user_id)
        username = user.username
        # 根据loan_id获取loan数据，从而得到loan_amnt和purpose字段
        loan_data = StaffLoan.objects.get(id=self.loan_id)
        loan_amnt = loan_data.loan_amnt
        purpose = loan_data.purpose
        rst_dit = {'username': username, 'loan_amnt': loan_amnt, 'purpose': purpose, 'progress': self.approval_progress,
                   'create_time': str(self.create_time), 'update_time': str(self.update_time), 'approver_id': self.approver_id,
                   'is_pass': self.is_pass_review}
        return rst_dit


# 用户拓展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 会员号字段
    member_id = models.CharField(max_length=20, blank=False, null=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    # 是否是第一次登录
    is_first_login = models.BooleanField(null=True)
    def __str__(self):
        return f'user: "{self.user.username}", member_id: "{self.member_id}", is_first_login: "{self.is_first_login}"'

# 信号接收函数, 每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, is_first_login=1)
# 信号接收函数，每当更新User实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Staff(models.Model):
    def __str__(self):
        return "Staff:[id={}, sno={}, sname={}]".format(
            self.id, self.sno, self.sname
        )

    class Sex(models.IntegerChoices):  # 采用 Django 提供了的 IntegerChoices 类，完成性别字段的枚举
        WOMAN = 0
        MAN = 1

    id = models.AutoField(primary_key=True)  # 用户id。 (AutoField：自增)
    sno = models.CharField(max_length=32, unique=True)  # 员工号(系统账号)  (unique=True : 字段唯一)
    password = models.CharField(max_length=32)  # 密码
    sname = models.CharField(max_length=32)  # 员工姓名
    email = models.EmailField(null=True, max_length=32)  # 邮箱 (blank=True 允许空值)
    sex = models.IntegerField(choices=Sex.choices, default=1)  # 性别  (default=1 : 默认为男性)
    """
      目前，将 auto_now 或 auto_now_add 设置为 True，将导致该字段设置为 editable=False 和 blank=True。
      auto_now: 每次保存对象时，自动将该字段设置为现在。  auto_now_add: 当第一次创建对象时，自动将该字段设置为现在。
    """
    create_time = models.DateField(auto_now=False, auto_now_add=True)  # 创建时间
    update_time = models.DateField(auto_now=True, auto_now_add=False)  # 最近一次修改时间


class StaffClean(models.Model):
    loan_status = models.IntegerField(blank=True, null=True)
    member_id = models.CharField(max_length=20, blank=True, null=True)
    term_36_months = models.IntegerField(db_column='term_ 36 months', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    term_60_months = models.IntegerField(db_column='term_ 60 months', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    home_ownership_any = models.IntegerField(db_column='home_ownership_ANY', blank=True, null=True)  # Field name made lowercase.
    home_ownership_mortgage = models.IntegerField(db_column='home_ownership_MORTGAGE', blank=True, null=True)  # Field name made lowercase.
    home_ownership_none = models.IntegerField(db_column='home_ownership_NONE', blank=True, null=True)  # Field name made lowercase.
    home_ownership_other = models.IntegerField(db_column='home_ownership_OTHER', blank=True, null=True)  # Field name made lowercase.
    home_ownership_own = models.IntegerField(db_column='home_ownership_OWN', blank=True, null=True)  # Field name made lowercase.
    home_ownership_rent = models.IntegerField(db_column='home_ownership_RENT', blank=True, null=True)  # Field name made lowercase.
    verification_status_not_verified = models.IntegerField(db_column='verification_status_Not Verified', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    verification_status_source_verified = models.IntegerField(db_column='verification_status_Source Verified', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    verification_status_verified = models.IntegerField(db_column='verification_status_Verified', blank=True, null=True)  # Field name made lowercase.
    purpose_car = models.IntegerField(blank=True, null=True)
    purpose_credit_card = models.IntegerField(blank=True, null=True)
    purpose_debt_consolidation = models.IntegerField(blank=True, null=True)
    purpose_educational = models.IntegerField(blank=True, null=True)
    purpose_home_improvement = models.IntegerField(blank=True, null=True)
    purpose_house = models.IntegerField(blank=True, null=True)
    purpose_major_purchase = models.IntegerField(blank=True, null=True)
    purpose_medical = models.IntegerField(blank=True, null=True)
    purpose_moving = models.IntegerField(blank=True, null=True)
    purpose_other = models.IntegerField(blank=True, null=True)
    purpose_renewable_energy = models.IntegerField(blank=True, null=True)
    purpose_small_business = models.IntegerField(blank=True, null=True)
    purpose_vacation = models.IntegerField(blank=True, null=True)
    purpose_wedding = models.IntegerField(blank=True, null=True)
    addr_state_ak = models.IntegerField(db_column='addr_state_AK', blank=True, null=True)  # Field name made lowercase.
    addr_state_al = models.IntegerField(db_column='addr_state_AL', blank=True, null=True)  # Field name made lowercase.
    addr_state_ar = models.IntegerField(db_column='addr_state_AR', blank=True, null=True)  # Field name made lowercase.
    addr_state_az = models.IntegerField(db_column='addr_state_AZ', blank=True, null=True)  # Field name made lowercase.
    addr_state_ca = models.IntegerField(db_column='addr_state_CA', blank=True, null=True)  # Field name made lowercase.
    addr_state_co = models.IntegerField(db_column='addr_state_CO', blank=True, null=True)  # Field name made lowercase.
    addr_state_ct = models.IntegerField(db_column='addr_state_CT', blank=True, null=True)  # Field name made lowercase.
    addr_state_dc = models.IntegerField(db_column='addr_state_DC', blank=True, null=True)  # Field name made lowercase.
    addr_state_de = models.IntegerField(db_column='addr_state_DE', blank=True, null=True)  # Field name made lowercase.
    addr_state_fl = models.IntegerField(db_column='addr_state_FL', blank=True, null=True)  # Field name made lowercase.
    addr_state_ga = models.IntegerField(db_column='addr_state_GA', blank=True, null=True)  # Field name made lowercase.
    addr_state_hi = models.IntegerField(db_column='addr_state_HI', blank=True, null=True)  # Field name made lowercase.
    addr_state_ia = models.IntegerField(db_column='addr_state_IA', blank=True, null=True)  # Field name made lowercase.
    addr_state_id = models.IntegerField(db_column='addr_state_ID', blank=True, null=True)  # Field name made lowercase.
    addr_state_il = models.IntegerField(db_column='addr_state_IL', blank=True, null=True)  # Field name made lowercase.
    addr_state_in = models.IntegerField(db_column='addr_state_IN', blank=True, null=True)  # Field name made lowercase.
    addr_state_ks = models.IntegerField(db_column='addr_state_KS', blank=True, null=True)  # Field name made lowercase.
    addr_state_ky = models.IntegerField(db_column='addr_state_KY', blank=True, null=True)  # Field name made lowercase.
    addr_state_la = models.IntegerField(db_column='addr_state_LA', blank=True, null=True)  # Field name made lowercase.
    addr_state_ma = models.IntegerField(db_column='addr_state_MA', blank=True, null=True)  # Field name made lowercase.
    addr_state_md = models.IntegerField(db_column='addr_state_MD', blank=True, null=True)  # Field name made lowercase.
    addr_state_me = models.IntegerField(db_column='addr_state_ME', blank=True, null=True)  # Field name made lowercase.
    addr_state_mi = models.IntegerField(db_column='addr_state_MI', blank=True, null=True)  # Field name made lowercase.
    addr_state_mn = models.IntegerField(db_column='addr_state_MN', blank=True, null=True)  # Field name made lowercase.
    addr_state_mo = models.IntegerField(db_column='addr_state_MO', blank=True, null=True)  # Field name made lowercase.
    addr_state_ms = models.IntegerField(db_column='addr_state_MS', blank=True, null=True)  # Field name made lowercase.
    addr_state_mt = models.IntegerField(db_column='addr_state_MT', blank=True, null=True)  # Field name made lowercase.
    addr_state_nc = models.IntegerField(db_column='addr_state_NC', blank=True, null=True)  # Field name made lowercase.
    addr_state_nd = models.IntegerField(db_column='addr_state_ND', blank=True, null=True)  # Field name made lowercase.
    addr_state_ne = models.IntegerField(db_column='addr_state_NE', blank=True, null=True)  # Field name made lowercase.
    addr_state_nh = models.IntegerField(db_column='addr_state_NH', blank=True, null=True)  # Field name made lowercase.
    addr_state_nj = models.IntegerField(db_column='addr_state_NJ', blank=True, null=True)  # Field name made lowercase.
    addr_state_nm = models.IntegerField(db_column='addr_state_NM', blank=True, null=True)  # Field name made lowercase.
    addr_state_nv = models.IntegerField(db_column='addr_state_NV', blank=True, null=True)  # Field name made lowercase.
    addr_state_ny = models.IntegerField(db_column='addr_state_NY', blank=True, null=True)  # Field name made lowercase.
    addr_state_oh = models.IntegerField(db_column='addr_state_OH', blank=True, null=True)  # Field name made lowercase.
    addr_state_ok = models.IntegerField(db_column='addr_state_OK', blank=True, null=True)  # Field name made lowercase.
    addr_state_or = models.IntegerField(db_column='addr_state_OR', blank=True, null=True)  # Field name made lowercase.
    addr_state_pa = models.IntegerField(db_column='addr_state_PA', blank=True, null=True)  # Field name made lowercase.
    addr_state_ri = models.IntegerField(db_column='addr_state_RI', blank=True, null=True)  # Field name made lowercase.
    addr_state_sc = models.IntegerField(db_column='addr_state_SC', blank=True, null=True)  # Field name made lowercase.
    addr_state_sd = models.IntegerField(db_column='addr_state_SD', blank=True, null=True)  # Field name made lowercase.
    addr_state_tn = models.IntegerField(db_column='addr_state_TN', blank=True, null=True)  # Field name made lowercase.
    addr_state_tx = models.IntegerField(db_column='addr_state_TX', blank=True, null=True)  # Field name made lowercase.
    addr_state_ut = models.IntegerField(db_column='addr_state_UT', blank=True, null=True)  # Field name made lowercase.
    addr_state_va = models.IntegerField(db_column='addr_state_VA', blank=True, null=True)  # Field name made lowercase.
    addr_state_vt = models.IntegerField(db_column='addr_state_VT', blank=True, null=True)  # Field name made lowercase.
    addr_state_wa = models.IntegerField(db_column='addr_state_WA', blank=True, null=True)  # Field name made lowercase.
    addr_state_wi = models.IntegerField(db_column='addr_state_WI', blank=True, null=True)  # Field name made lowercase.
    addr_state_wv = models.IntegerField(db_column='addr_state_WV', blank=True, null=True)  # Field name made lowercase.
    addr_state_wy = models.IntegerField(db_column='addr_state_WY', blank=True, null=True)  # Field name made lowercase.
    initial_list_status_f = models.IntegerField(blank=True, null=True)
    initial_list_status_w = models.IntegerField(blank=True, null=True)
    norm_loan_amnt = models.FloatField(blank=True, null=True)
    norm_int_rate = models.FloatField(blank=True, null=True)
    norm_sub_grade = models.FloatField(blank=True, null=True)
    norm_emp_length = models.FloatField(blank=True, null=True)
    norm_annual_inc = models.FloatField(blank=True, null=True)
    norm_dti = models.FloatField(blank=True, null=True)
    norm_delinq_2yrs = models.FloatField(blank=True, null=True)
    norm_inq_last_6mths = models.FloatField(blank=True, null=True)
    norm_mths_since_last_delinq = models.FloatField(blank=True, null=True)
    norm_open_acc = models.FloatField(blank=True, null=True)
    norm_pub_rec = models.FloatField(blank=True, null=True)
    norm_revol_bal = models.FloatField(blank=True, null=True)
    norm_revol_util = models.FloatField(blank=True, null=True)
    norm_total_acc = models.FloatField(blank=True, null=True)
    norm_total_rec_int = models.FloatField(blank=True, null=True)
    norm_total_rec_late_fee = models.FloatField(blank=True, null=True)
    norm_recoveries = models.FloatField(blank=True, null=True)
    norm_collection_recovery_fee = models.FloatField(blank=True, null=True)
    norm_collections_12_mths_ex_med = models.FloatField(blank=True, null=True)
    norm_acc_now_delinq = models.FloatField(blank=True, null=True)
    norm_tot_coll_amt = models.FloatField(blank=True, null=True)
    norm_tot_cur_bal = models.FloatField(blank=True, null=True)
    norm_total_rev_hi_lim = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"member_id: {self.member_id}, loan_status: {self.loan_status}, norm_loan_amnt: {self.norm_loan_amnt}"

    class Meta:
        managed = False
        db_table = 'staff_clean'


class StaffLoan(models.Model):
    id = models.IntegerField(primary_key=True)
    member_id = models.CharField(max_length=20, blank=True, null=True)
    loan_amnt = models.CharField(max_length=20, blank=True, null=True)
    funded_amnt = models.CharField(max_length=20, blank=True, null=True)
    funded_amnt_inv = models.CharField(max_length=20, blank=True, null=True)
    term = models.CharField(max_length=10, blank=True, null=True)
    int_rate = models.CharField(max_length=20, blank=True, null=True)
    installment = models.CharField(max_length=20, blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    sub_grade = models.CharField(max_length=5, blank=True, null=True)
    emp_title = models.CharField(max_length=20, blank=True, null=True)
    emp_length = models.CharField(max_length=20, blank=True, null=True)
    home_ownership = models.CharField(max_length=20, blank=True, null=True)
    annual_inc = models.CharField(max_length=20, blank=True, null=True)
    verification_status = models.CharField(max_length=20, blank=True, null=True)
    issue_d = models.CharField(max_length=20, blank=True, null=True)
    loan_status = models.CharField(max_length=20, blank=True, null=True)
    pymnt_plan = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    desc_0 = models.CharField(max_length=20, blank=True, null=True)
    purpose = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    addr_state = models.CharField(max_length=20, blank=True, null=True)
    dti = models.CharField(max_length=20, blank=True, null=True)
    delinq_2yrs = models.CharField(max_length=20, blank=True, null=True)
    earliest_cr_line = models.CharField(max_length=20, blank=True, null=True)
    inq_last_6mths = models.CharField(max_length=20, blank=True, null=True)
    mths_since_last_delinq = models.CharField(max_length=20, blank=True, null=True)
    mths_since_last_record = models.CharField(max_length=20, blank=True, null=True)
    open_acc = models.CharField(max_length=20, blank=True, null=True)
    pub_rec = models.CharField(max_length=20, blank=True, null=True)
    revol_bal = models.CharField(max_length=20, blank=True, null=True)
    revol_util = models.CharField(max_length=20, blank=True, null=True)
    total_acc = models.CharField(max_length=20, blank=True, null=True)
    initial_list_status = models.CharField(max_length=20, blank=True, null=True)
    out_prncp = models.CharField(max_length=20, blank=True, null=True)
    out_prncp_inv = models.CharField(max_length=20, blank=True, null=True)
    total_pymnt = models.CharField(max_length=20, blank=True, null=True)
    total_pymnt_inv = models.CharField(max_length=20, blank=True, null=True)
    total_rec_prncp = models.CharField(max_length=20, blank=True, null=True)
    total_rec_int = models.CharField(max_length=20, blank=True, null=True)
    total_rec_late_fee = models.CharField(max_length=20, blank=True, null=True)
    recoveries = models.CharField(max_length=20, blank=True, null=True)
    collection_recovery_fee = models.CharField(max_length=20, blank=True, null=True)
    last_pymnt_d = models.CharField(max_length=20, blank=True, null=True)
    last_pymnt_amnt = models.CharField(max_length=20, blank=True, null=True)
    next_pymnt_d = models.CharField(max_length=20, blank=True, null=True)
    last_credit_pull_d = models.CharField(max_length=20, blank=True, null=True)
    collections_12_mths_ex_med = models.CharField(max_length=20, blank=True, null=True)
    mths_since_last_major_derog = models.CharField(max_length=20, blank=True, null=True)
    policy_code = models.CharField(max_length=20, blank=True, null=True)
    application_type = models.CharField(max_length=20, blank=True, null=True)
    annual_inc_joint = models.CharField(max_length=20, blank=True, null=True)
    dti_joint = models.CharField(max_length=20, blank=True, null=True)
    verification_status_joint = models.CharField(max_length=20, blank=True, null=True)
    acc_now_delinq = models.CharField(max_length=20, blank=True, null=True)
    tot_coll_amt = models.CharField(max_length=20, blank=True, null=True)
    tot_cur_bal = models.CharField(max_length=20, blank=True, null=True)
    open_acc_6m = models.CharField(max_length=20, blank=True, null=True)
    open_il_6m = models.CharField(max_length=20, blank=True, null=True)
    open_il_12m = models.CharField(max_length=20, blank=True, null=True)
    open_il_24m = models.CharField(max_length=20, blank=True, null=True)
    mths_since_rcnt_il = models.CharField(max_length=20, blank=True, null=True)
    total_bal_il = models.CharField(max_length=20, blank=True, null=True)
    il_util = models.CharField(max_length=20, blank=True, null=True)
    open_rv_12m = models.CharField(max_length=20, blank=True, null=True)
    open_rv_24m = models.CharField(max_length=20, blank=True, null=True)
    max_bal_bc = models.CharField(max_length=20, blank=True, null=True)
    all_util = models.CharField(max_length=20, blank=True, null=True)
    total_rev_hi_lim = models.CharField(max_length=20, blank=True, null=True)
    inq_fi = models.CharField(max_length=20, blank=True, null=True)
    total_cu_tl = models.CharField(max_length=20, blank=True, null=True)
    inq_last_12m = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_loan'


"""
class LoanData(models.Model):
    def __str__(self):
        return "LoanData:[id={}, member_id={}, loan_amnt={}, loan_status={}]".format(
            self.id, self.member_id, self.loan_amnt, self.loan_status
        )

    member_id = models.CharField(max_length=255, blank=True, null=True)
    loan_amnt = models.CharField(max_length=255, blank=True, null=True)
    funded_amnt = models.CharField(max_length=255, blank=True, null=True)
    funded_amnt_inv = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    int_rate = models.CharField(max_length=255, blank=True, null=True)
    installment = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    sub_grade = models.CharField(max_length=255, blank=True, null=True)
    emp_title = models.CharField(max_length=255, blank=True, null=True)
    emp_length = models.CharField(max_length=255, blank=True, null=True)
    home_ownership = models.CharField(max_length=255, blank=True, null=True)
    annual_inc = models.CharField(max_length=255, blank=True, null=True)
    verification_status = models.CharField(max_length=255, blank=True, null=True)
    issue_d = models.CharField(max_length=255, blank=True, null=True)
    loan_status = models.CharField(max_length=255, blank=True, null=True)
    pymnt_plan = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    desc_0 = models.CharField(max_length=255, blank=True, null=True)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    addr_state = models.CharField(max_length=255, blank=True, null=True)
    dti = models.CharField(max_length=255, blank=True, null=True)
    delinq_2yrs = models.CharField(max_length=255, blank=True, null=True)
    earliest_cr_line = models.CharField(max_length=255, blank=True, null=True)
    inq_last_6mths = models.CharField(max_length=255, blank=True, null=True)
    mths_since_last_delinq = models.CharField(max_length=255, blank=True, null=True)
    mths_since_last_record = models.CharField(max_length=255, blank=True, null=True)
    open_acc = models.CharField(max_length=255, blank=True, null=True)
    pub_rec = models.CharField(max_length=255, blank=True, null=True)
    revol_bal = models.CharField(max_length=255, blank=True, null=True)
    revol_util = models.CharField(max_length=255, blank=True, null=True)
    total_acc = models.CharField(max_length=255, blank=True, null=True)
    initial_list_status = models.CharField(max_length=255, blank=True, null=True)
    out_prncp = models.CharField(max_length=255, blank=True, null=True)
    out_prncp_inv = models.CharField(max_length=255, blank=True, null=True)
    total_pymnt = models.CharField(max_length=255, blank=True, null=True)
    total_pymnt_inv = models.CharField(max_length=255, blank=True, null=True)
    total_rec_prncp = models.CharField(max_length=255, blank=True, null=True)
    total_rec_int = models.CharField(max_length=255, blank=True, null=True)
    total_rec_late_fee = models.CharField(max_length=255, blank=True, null=True)
    recoveries = models.CharField(max_length=255, blank=True, null=True)
    collection_recovery_fee = models.CharField(max_length=255, blank=True, null=True)
    last_pymnt_d = models.CharField(max_length=255, blank=True, null=True)
    last_pymnt_amnt = models.CharField(max_length=255, blank=True, null=True)
    next_pymnt_d = models.CharField(max_length=255, blank=True, null=True)
    last_credit_pull_d = models.CharField(max_length=255, blank=True, null=True)
    collections_12_mths_ex_med = models.CharField(max_length=255, blank=True, null=True)
    mths_since_last_major_derog = models.CharField(max_length=255, blank=True, null=True)
    policy_code = models.CharField(max_length=255, blank=True, null=True)
    application_type = models.CharField(max_length=255, blank=True, null=True)
    annual_inc_joint = models.CharField(max_length=255, blank=True, null=True)
    dti_joint = models.CharField(max_length=255, blank=True, null=True)
    verification_status_joint = models.CharField(max_length=255, blank=True, null=True)
    acc_now_delinq = models.CharField(max_length=255, blank=True, null=True)
    tot_coll_amt = models.CharField(max_length=255, blank=True, null=True)
    tot_cur_bal = models.CharField(max_length=255, blank=True, null=True)
    open_acc_6m = models.CharField(max_length=255, blank=True, null=True)
    open_il_6m = models.CharField(max_length=255, blank=True, null=True)
    open_il_12m = models.CharField(max_length=255, blank=True, null=True)
    open_il_24m = models.CharField(max_length=255, blank=True, null=True)
    mths_since_rcnt_il = models.CharField(max_length=255, blank=True, null=True)
    total_bal_il = models.CharField(max_length=255, blank=True, null=True)
    il_util = models.CharField(max_length=255, blank=True, null=True)
    open_rv_12m = models.CharField(max_length=255, blank=True, null=True)
    open_rv_24m = models.CharField(max_length=255, blank=True, null=True)
    max_bal_bc = models.CharField(max_length=255, blank=True, null=True)
    all_util = models.CharField(max_length=255, blank=True, null=True)
    total_rev_hi_lim = models.CharField(max_length=255, blank=True, null=True)
    inq_fi = models.CharField(max_length=255, blank=True, null=True)
    total_cu_tl = models.CharField(max_length=255, blank=True, null=True)
    inq_last_12m = models.CharField(max_length=255, blank=True, null=True)
"""