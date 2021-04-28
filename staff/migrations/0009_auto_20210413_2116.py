# Generated by Django 3.1.4 on 2021-04-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_profile_is_first_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffClean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_status', models.IntegerField(blank=True, null=True)),
                ('member_id', models.CharField(blank=True, max_length=20, null=True)),
                ('term_36_months', models.IntegerField(blank=True, db_column='term_ 36 months', null=True)),
                ('term_60_months', models.IntegerField(blank=True, db_column='term_ 60 months', null=True)),
                ('home_ownership_any', models.IntegerField(blank=True, db_column='home_ownership_ANY', null=True)),
                ('home_ownership_mortgage', models.IntegerField(blank=True, db_column='home_ownership_MORTGAGE', null=True)),
                ('home_ownership_none', models.IntegerField(blank=True, db_column='home_ownership_NONE', null=True)),
                ('home_ownership_other', models.IntegerField(blank=True, db_column='home_ownership_OTHER', null=True)),
                ('home_ownership_own', models.IntegerField(blank=True, db_column='home_ownership_OWN', null=True)),
                ('home_ownership_rent', models.IntegerField(blank=True, db_column='home_ownership_RENT', null=True)),
                ('verification_status_not_verified', models.IntegerField(blank=True, db_column='verification_status_Not Verified', null=True)),
                ('verification_status_source_verified', models.IntegerField(blank=True, db_column='verification_status_Source Verified', null=True)),
                ('verification_status_verified', models.IntegerField(blank=True, db_column='verification_status_Verified', null=True)),
                ('purpose_car', models.IntegerField(blank=True, null=True)),
                ('purpose_credit_card', models.IntegerField(blank=True, null=True)),
                ('purpose_debt_consolidation', models.IntegerField(blank=True, null=True)),
                ('purpose_educational', models.IntegerField(blank=True, null=True)),
                ('purpose_home_improvement', models.IntegerField(blank=True, null=True)),
                ('purpose_house', models.IntegerField(blank=True, null=True)),
                ('purpose_major_purchase', models.IntegerField(blank=True, null=True)),
                ('purpose_medical', models.IntegerField(blank=True, null=True)),
                ('purpose_moving', models.IntegerField(blank=True, null=True)),
                ('purpose_other', models.IntegerField(blank=True, null=True)),
                ('purpose_renewable_energy', models.IntegerField(blank=True, null=True)),
                ('purpose_small_business', models.IntegerField(blank=True, null=True)),
                ('purpose_vacation', models.IntegerField(blank=True, null=True)),
                ('purpose_wedding', models.IntegerField(blank=True, null=True)),
                ('addr_state_ak', models.IntegerField(blank=True, db_column='addr_state_AK', null=True)),
                ('addr_state_al', models.IntegerField(blank=True, db_column='addr_state_AL', null=True)),
                ('addr_state_ar', models.IntegerField(blank=True, db_column='addr_state_AR', null=True)),
                ('addr_state_az', models.IntegerField(blank=True, db_column='addr_state_AZ', null=True)),
                ('addr_state_ca', models.IntegerField(blank=True, db_column='addr_state_CA', null=True)),
                ('addr_state_co', models.IntegerField(blank=True, db_column='addr_state_CO', null=True)),
                ('addr_state_ct', models.IntegerField(blank=True, db_column='addr_state_CT', null=True)),
                ('addr_state_dc', models.IntegerField(blank=True, db_column='addr_state_DC', null=True)),
                ('addr_state_de', models.IntegerField(blank=True, db_column='addr_state_DE', null=True)),
                ('addr_state_fl', models.IntegerField(blank=True, db_column='addr_state_FL', null=True)),
                ('addr_state_ga', models.IntegerField(blank=True, db_column='addr_state_GA', null=True)),
                ('addr_state_hi', models.IntegerField(blank=True, db_column='addr_state_HI', null=True)),
                ('addr_state_ia', models.IntegerField(blank=True, db_column='addr_state_IA', null=True)),
                ('addr_state_id', models.IntegerField(blank=True, db_column='addr_state_ID', null=True)),
                ('addr_state_il', models.IntegerField(blank=True, db_column='addr_state_IL', null=True)),
                ('addr_state_in', models.IntegerField(blank=True, db_column='addr_state_IN', null=True)),
                ('addr_state_ks', models.IntegerField(blank=True, db_column='addr_state_KS', null=True)),
                ('addr_state_ky', models.IntegerField(blank=True, db_column='addr_state_KY', null=True)),
                ('addr_state_la', models.IntegerField(blank=True, db_column='addr_state_LA', null=True)),
                ('addr_state_ma', models.IntegerField(blank=True, db_column='addr_state_MA', null=True)),
                ('addr_state_md', models.IntegerField(blank=True, db_column='addr_state_MD', null=True)),
                ('addr_state_me', models.IntegerField(blank=True, db_column='addr_state_ME', null=True)),
                ('addr_state_mi', models.IntegerField(blank=True, db_column='addr_state_MI', null=True)),
                ('addr_state_mn', models.IntegerField(blank=True, db_column='addr_state_MN', null=True)),
                ('addr_state_mo', models.IntegerField(blank=True, db_column='addr_state_MO', null=True)),
                ('addr_state_ms', models.IntegerField(blank=True, db_column='addr_state_MS', null=True)),
                ('addr_state_mt', models.IntegerField(blank=True, db_column='addr_state_MT', null=True)),
                ('addr_state_nc', models.IntegerField(blank=True, db_column='addr_state_NC', null=True)),
                ('addr_state_nd', models.IntegerField(blank=True, db_column='addr_state_ND', null=True)),
                ('addr_state_ne', models.IntegerField(blank=True, db_column='addr_state_NE', null=True)),
                ('addr_state_nh', models.IntegerField(blank=True, db_column='addr_state_NH', null=True)),
                ('addr_state_nj', models.IntegerField(blank=True, db_column='addr_state_NJ', null=True)),
                ('addr_state_nm', models.IntegerField(blank=True, db_column='addr_state_NM', null=True)),
                ('addr_state_nv', models.IntegerField(blank=True, db_column='addr_state_NV', null=True)),
                ('addr_state_ny', models.IntegerField(blank=True, db_column='addr_state_NY', null=True)),
                ('addr_state_oh', models.IntegerField(blank=True, db_column='addr_state_OH', null=True)),
                ('addr_state_ok', models.IntegerField(blank=True, db_column='addr_state_OK', null=True)),
                ('addr_state_or', models.IntegerField(blank=True, db_column='addr_state_OR', null=True)),
                ('addr_state_pa', models.IntegerField(blank=True, db_column='addr_state_PA', null=True)),
                ('addr_state_ri', models.IntegerField(blank=True, db_column='addr_state_RI', null=True)),
                ('addr_state_sc', models.IntegerField(blank=True, db_column='addr_state_SC', null=True)),
                ('addr_state_sd', models.IntegerField(blank=True, db_column='addr_state_SD', null=True)),
                ('addr_state_tn', models.IntegerField(blank=True, db_column='addr_state_TN', null=True)),
                ('addr_state_tx', models.IntegerField(blank=True, db_column='addr_state_TX', null=True)),
                ('addr_state_ut', models.IntegerField(blank=True, db_column='addr_state_UT', null=True)),
                ('addr_state_va', models.IntegerField(blank=True, db_column='addr_state_VA', null=True)),
                ('addr_state_vt', models.IntegerField(blank=True, db_column='addr_state_VT', null=True)),
                ('addr_state_wa', models.IntegerField(blank=True, db_column='addr_state_WA', null=True)),
                ('addr_state_wi', models.IntegerField(blank=True, db_column='addr_state_WI', null=True)),
                ('addr_state_wv', models.IntegerField(blank=True, db_column='addr_state_WV', null=True)),
                ('addr_state_wy', models.IntegerField(blank=True, db_column='addr_state_WY', null=True)),
                ('initial_list_status_f', models.IntegerField(blank=True, null=True)),
                ('initial_list_status_w', models.IntegerField(blank=True, null=True)),
                ('norm_loan_amnt', models.FloatField(blank=True, null=True)),
                ('norm_int_rate', models.FloatField(blank=True, null=True)),
                ('norm_sub_grade', models.FloatField(blank=True, null=True)),
                ('norm_emp_length', models.FloatField(blank=True, null=True)),
                ('norm_annual_inc', models.FloatField(blank=True, null=True)),
                ('norm_dti', models.FloatField(blank=True, null=True)),
                ('norm_delinq_2yrs', models.FloatField(blank=True, null=True)),
                ('norm_inq_last_6mths', models.FloatField(blank=True, null=True)),
                ('norm_mths_since_last_delinq', models.FloatField(blank=True, null=True)),
                ('norm_open_acc', models.FloatField(blank=True, null=True)),
                ('norm_pub_rec', models.FloatField(blank=True, null=True)),
                ('norm_revol_bal', models.FloatField(blank=True, null=True)),
                ('norm_revol_util', models.FloatField(blank=True, null=True)),
                ('norm_total_acc', models.FloatField(blank=True, null=True)),
                ('norm_total_rec_int', models.FloatField(blank=True, null=True)),
                ('norm_total_rec_late_fee', models.FloatField(blank=True, null=True)),
                ('norm_recoveries', models.FloatField(blank=True, null=True)),
                ('norm_collection_recovery_fee', models.FloatField(blank=True, null=True)),
                ('norm_collections_12_mths_ex_med', models.FloatField(blank=True, null=True)),
                ('norm_acc_now_delinq', models.FloatField(blank=True, null=True)),
                ('norm_tot_coll_amt', models.FloatField(blank=True, null=True)),
                ('norm_tot_cur_bal', models.FloatField(blank=True, null=True)),
                ('norm_total_rev_hi_lim', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'staff_clean',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(max_length=20)),
                ('member_id', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=20)),
                ('approver', models.CharField(max_length=20)),
                ('approval_progress', models.IntegerField(default=0)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='member_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
