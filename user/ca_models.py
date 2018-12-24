from peewee import *
from playhouse.postgres_ext import *

database = PostgresqlDatabase('calculation', **{'host': '120.79.69.141', 'user': 'postgres'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class AuthGroup(BaseModel):
    name = CharField(index=True)

    class Meta:
        table_name = 'auth_group'


class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        table_name = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )


class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType)
    name = CharField()

    class Meta:
        table_name = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )


class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)

    class Meta:
        table_name = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )


class CalculationProvince(BaseModel):
    desc_content = CharField()
    name = CharField()
    parent_province = ForeignKeyField(column_name='parent_province_id', field='id', model='self', null=True)
    province = CharField(column_name='province_id')

    class Meta:
        table_name = 'calculation_province'


class CalculationCity(BaseModel):
    cid = CharField()
    name = CharField()
    province = ForeignKeyField(column_name='province_id', field='id', model=CalculationProvince)

    class Meta:
        table_name = 'calculation_city'


class CalculationArea(BaseModel):
    aid = CharField()
    city = ForeignKeyField(column_name='city_id', field='id', model=CalculationCity)
    name = CharField()
    tax_province = IntegerField()

    class Meta:
        table_name = 'calculation_area'


class CalculationAtmosphericwaterpollution(BaseModel):
    check_type = CharField()
    create_time = DateTimeField()
    desc_content = CharField()
    equivalent = FloatField()
    equivalent_unit = CharField()
    index_num = IntegerField(index=True)
    is_delete = BooleanField()
    name = CharField()
    parent_pollution = ForeignKeyField(column_name='parent_pollution_id', field='id', model='self', null=True)
    pollutants_type = CharField(index=True)
    update_time = DateTimeField()
    water_type = IntegerField()

    class Meta:
        table_name = 'calculation_atmosphericwaterpollution'


class CalculationIndustry(BaseModel):
    atarray = ArrayField(column_name='atArray', field_class=IntegerField, null=True)
    create_time = DateTimeField()
    desc_content = TextField()
    gasgroup = TextField(column_name='gasGroup', null=True)
    is_delete = BooleanField()
    name = CharField(index=True)
    noisearray = ArrayField(column_name='noiseArray', field_class=IntegerField, null=True)
    solidarray = ArrayField(column_name='solidArray', field_class=IntegerField, null=True)
    solidgroup = TextField(column_name='solidGroup', null=True)
    update_time = DateTimeField()
    waterarray = ArrayField(column_name='waterArray', field_class=IntegerField, null=True)
    watergroup = TextField(column_name='waterGroup', null=True)

    class Meta:
        table_name = 'calculation_industry'


class CalculationIndustryanalysis(BaseModel):
    area = IntegerField(column_name='area_id')
    atm = ArrayField(field_class=CharField)
    atm_map_dict = BinaryJSONField()
    city = IntegerField(column_name='city_id')
    create_time = DateTimeField()
    desc_content = CharField()
    industry = IntegerField(column_name='industry_id')
    is_delete = BooleanField()
    noise = ArrayField(field_class=CharField)
    noise_map_dict = BinaryJSONField()
    province = IntegerField(column_name='province_id')
    solid = ArrayField(field_class=CharField)
    solid_map_dict = BinaryJSONField()
    total = DecimalField()
    update_time = DateTimeField()
    user = IntegerField(column_name='user_id', index=True)
    water = ArrayField(field_class=CharField)
    water_map_dict = BinaryJSONField()

    class Meta:
        table_name = 'calculation_industryanalysis'


class CalculationIndustryrationality(BaseModel):
    at_wa_range = CharField()
    content = CharField()
    create_time = DateTimeField()
    desc_content = CharField()
    industry = ForeignKeyField(column_name='industry_id', field='id', model=CalculationIndustry)
    is_delete = BooleanField()
    update_time = DateTimeField()
    year = IntegerField()

    class Meta:
        table_name = 'calculation_industryrationality'


class CalculationIndustryfile(BaseModel):
    content = CharField()
    create_time = DateTimeField()
    desc_content = CharField()
    file_url = CharField()
    industry_rationality = ForeignKeyField(
        column_name='industry_rationality_id', field='id', model=CalculationIndustryrationality)
    is_delete = BooleanField()
    name = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'calculation_industryfile'


class CalculationPollutiondata(BaseModel):
    address = CharField()
    address_type = CharField()
    bear_mater = CharField()
    company_name = CharField()
    create_time = DateTimeField()
    danger_item = CharField()
    danger_item_type = CharField()
    danger_pollution_name = CharField()
    danger_pollution_name_type = CharField()
    desc_content = CharField()
    document_url = CharField()
    icon_class = CharField()
    index_num = IntegerField()
    is_delete = BooleanField()
    is_number_data_again = CharField()
    is_observation_equipment = CharField()
    is_observation_return = CharField()
    observation_name = CharField()
    observation_number = CharField()
    observation_type = CharField()
    order_num = IntegerField()
    pollution_name = CharField()
    storage_size = CharField()
    storage_size_type = CharField()
    storage_unit = CharField()
    tax_mater = CharField()
    telephone = CharField()
    update_time = DateTimeField()
    user_address = CharField()
    user = IntegerField(column_name='user_id')
    user_info = TextField()
    username = CharField()

    class Meta:
        table_name = 'calculation_pollutiondata'


class CalculationPollutionhots(BaseModel):
    pollution = IntegerField(column_name='pollution_id', null=True)
    pollution_type = CharField()

    class Meta:
        table_name = 'calculation_pollutionhots'


class CalculationPollutionname(BaseModel):
    address = CharField()
    address_type = CharField()
    bear_mater = CharField()
    create_time = DateTimeField()
    danger_item = CharField()
    danger_item_type = CharField()
    danger_pollution_name = CharField()
    danger_pollution_name_type = CharField()
    desc_content = CharField()
    icon_class = CharField()
    index_num = IntegerField()
    is_delete = BooleanField()
    is_number_data_again = ArrayField(field_class=CharField, null=True)
    is_observation_equipment = ArrayField(field_class=CharField, null=True)
    is_observation_return = ArrayField(field_class=CharField, null=True)
    observation_name = ArrayField(field_class=CharField, null=True)
    observation_number = IntegerField()
    observation_type = ArrayField(field_class=CharField, null=True)
    order_num = IntegerField()
    pollution_name = CharField()
    storage_size = CharField()
    storage_size_type = CharField()
    storage_unit = CharField()
    tax_mater = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'calculation_pollutionname'


class CalculationPollutionnameBak(BaseModel):
    address = CharField(null=True)
    address_type = CharField(null=True)
    create_time = DateTimeField(null=True)
    danger_item = CharField(null=True)
    danger_item_type = CharField(null=True)
    danger_pollution_name = CharField(null=True)
    danger_pollution_name_type = CharField(null=True)
    desc_content = CharField(null=True)
    icon_class = CharField(null=True)
    id = IntegerField(null=True)
    index_num = IntegerField(null=True)
    is_delete = BooleanField(null=True)
    is_number_data_again = ArrayField(field_class=CharField, null=True)
    is_observation_equipment = ArrayField(field_class=CharField, null=True)
    is_observation_return = ArrayField(field_class=CharField, null=True)
    observation_name = ArrayField(field_class=CharField, null=True)
    observation_number = IntegerField(null=True)
    observation_type = ArrayField(field_class=CharField, null=True)
    order_num = IntegerField(null=True)
    pollution_name = CharField(null=True)
    storage_size = CharField(null=True)
    storage_size_type = CharField(null=True)
    storage_unit = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'calculation_pollutionname_bak'
        primary_key = False


class CalculationProvincetax(BaseModel):
    create_time = DateTimeField()
    desc_content = CharField()
    is_delete = BooleanField()
    pollution = ForeignKeyField(column_name='pollution_id', field='id', model=CalculationAtmosphericwaterpollution)
    province = ForeignKeyField(column_name='province_id', field='id', model=CalculationProvince)
    tax = FloatField()
    update_time = DateTimeField()
    year = IntegerField()

    class Meta:
        table_name = 'calculation_provincetax'
        indexes = (
            (('pollution', 'province'), False),
        )


class CalculationSolidnoisepollution(BaseModel):
    create_time = DateTimeField()
    desc_content = CharField()
    is_delete = BooleanField()
    name = CharField()
    pollutants_type = CharField(index=True)
    tax = IntegerField()
    update_time = DateTimeField()
    year = IntegerField()

    class Meta:
        table_name = 'calculation_solidnoisepollution'


class CalculationUserprofile(BaseModel):
    birthday = DateField(null=True)
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    gender = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    mobile = CharField(index=True, null=True)
    name = CharField(null=True)
    password = CharField()
    username = CharField(index=True)

    class Meta:
        table_name = 'calculation_userprofile'


class CalculationUserprofileGroups(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    userprofile = ForeignKeyField(column_name='userprofile_id', field='id', model=CalculationUserprofile)

    class Meta:
        table_name = 'calculation_userprofile_groups'
        indexes = (
            (('userprofile', 'group'), True),
        )


class CalculationUserprofileUserPermissions(BaseModel):
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)
    userprofile = ForeignKeyField(column_name='userprofile_id', field='id', model=CalculationUserprofile)

    class Meta:
        table_name = 'calculation_userprofile_user_permissions'
        indexes = (
            (('userprofile', 'permission'), True),
        )


class CalculationVerifycode(BaseModel):
    add_time = DateTimeField()
    code = CharField()
    mobile = CharField()

    class Meta:
        table_name = 'calculation_verifycode'


class DashboardUserdashboardmodule(BaseModel):
    app_label = CharField(null=True)
    children = TextField()
    collapsed = BooleanField()
    column = IntegerField()
    module = CharField()
    order = IntegerField()
    settings = TextField()
    title = CharField()
    user = IntegerField()

    class Meta:
        table_name = 'dashboard_userdashboardmodule'


class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType, null=True)
    object = TextField(column_name='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(column_name='user_id', field='id', model=CalculationUserprofile)

    class Meta:
        table_name = 'django_admin_log'


class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        table_name = 'django_migrations'


class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        table_name = 'django_session'


class JetBookmark(BaseModel):
    date_add = DateTimeField()
    title = CharField()
    url = CharField()
    user = IntegerField()

    class Meta:
        table_name = 'jet_bookmark'


class JetPinnedapplication(BaseModel):
    app_label = CharField()
    date_add = DateTimeField()
    user = IntegerField()

    class Meta:
        table_name = 'jet_pinnedapplication'


class SilkRequest(BaseModel):
    body = TextField()
    encoded_headers = TextField()
    end_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    meta_num_queries = IntegerField(null=True)
    meta_time = FloatField(null=True)
    meta_time_spent_queries = FloatField(null=True)
    method = CharField()
    num_sql_queries = IntegerField()
    path = CharField(index=True)
    prof_file = CharField()
    pyprofile = TextField()
    query_params = TextField()
    raw_body = TextField()
    start_time = DateTimeField(index=True)
    time_taken = FloatField(null=True)
    view_name = CharField(index=True, null=True)

    class Meta:
        table_name = 'silk_request'


class SilkProfile(BaseModel):
    dynamic = BooleanField()
    end_line_num = IntegerField(null=True)
    end_time = DateTimeField(null=True)
    exception_raised = BooleanField()
    file_path = CharField()
    func_name = CharField()
    line_num = IntegerField(null=True)
    name = CharField()
    request = ForeignKeyField(column_name='request_id', field='id', model=SilkRequest, null=True)
    start_time = DateTimeField()
    time_taken = FloatField(null=True)

    class Meta:
        table_name = 'silk_profile'


class SilkSqlquery(BaseModel):
    end_time = DateTimeField(null=True)
    query = TextField()
    request = ForeignKeyField(column_name='request_id', field='id', model=SilkRequest, null=True)
    start_time = DateTimeField(null=True)
    time_taken = FloatField(null=True)
    traceback = TextField()

    class Meta:
        table_name = 'silk_sqlquery'


class SilkProfileQueries(BaseModel):
    profile = ForeignKeyField(column_name='profile_id', field='id', model=SilkProfile)
    sqlquery = ForeignKeyField(column_name='sqlquery_id', field='id', model=SilkSqlquery)

    class Meta:
        table_name = 'silk_profile_queries'
        indexes = (
            (('profile', 'sqlquery'), True),
        )


class SilkResponse(BaseModel):
    body = TextField()
    encoded_headers = TextField()
    id = CharField(primary_key=True)
    raw_body = TextField()
    request = ForeignKeyField(column_name='request_id', field='id', model=SilkRequest)
    status_code = IntegerField()

    class Meta:
        table_name = 'silk_response'

