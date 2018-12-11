from flask_wtf import FlaskForm as Form
from wtforms import TextAreaField, PasswordField, StringField, TextField,\
 SelectField,BooleanField, IntegerField, DateField, DateTimeField, FloatField,\
 RadioField, FieldList, FormField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from simflow.models import SourceSystem, PropertyDescription, Person, Role, ProductMaster, SubProductMaster, PropertyCardStatus, ProposalStatus, Proposal
from simflow.models import Person, Role, HouseholdCategoryModel,CarpetAreaClassificationMaster, PropertyTypeModel,PropertyCategoryModel, StatutoryTownAndPlanningModel,\
OwnershipModeModel,LoanSourceModel, LoanPurposeModel, GenderModel, UniqueIdentificationProofModel,ResidenceProofTypeModel,YesNoModel
from flask_wtf.file import FileField, FileRequired
from datetime import datetime

strip_filter = lambda x: x.strip() if x else None

# def sourceSystems():
#     return SourceSystem.query.order_by(SourceSystem.source_system)

# def propertyDescriptions():
#     return PropertyDescription.query.all()

def roleDropDown():
    return Role.query

def householdCategoryModelDropDown():
    return HouseholdCategoryModel.query

def propertyTypeModelDropDown():
    return PropertyTypeModel.query

def propertyCategoryModelDropDown():
    return PropertyCategoryModel.query

def carpetAreaClassificationMasterDropDown():
    return CarpetAreaClassificationMaster.query

def statutoryTownAndPlanningModelDropDown():
    return StatutoryTownAndPlanningModel.query

def ownershipModeModelDropDown():
    return OwnershipModeModel.query

def loanSourceModelDropDown():
    return LoanSourceModel.query

def loanPurposeModelDropDown():
    return LoanPurposeModel.query

# def productDropDown():
#     return ProductMaster.query.order_by(ProductMaster.product).all()

# def subProductDropDown():
#     return SubProductMaster.query.order_by(SubProductMaster.product).all()
# def propertyCardStatusDropDown():
#     return PropertyCardStatus.query.all()
# def proposalStatusDropDown():
#     return ProposalStatus.query

# def defaultstatus():
#     return ProposalStatus.query.filter(ProposalStatus.status=='WIP').first()
#TODO add strip_filter to all txt-fields

class LoginForm(Form):
    username = TextField('Username', validators=[validators.required(message="Username is required")],filters=[strip_filter])
    password = PasswordField('Password',validators=[validators.required(message="Password is required")])

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = Person.query.filter_by(username = self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid username or password')
            return False
        return True

class RegisterForm(Form):
    username = TextField('Username', validators=[validators.data_required(message="Username is a required field")])
    firstName = TextField('First Name', validators=[validators.data_required(message="First Name is a required field")])
    middleName = TextField('Middle Name')
    lastName = TextField('Last Name', validators=[validators.data_required(message="Last Name is a required field")])
    email = TextField('Email', [validators.email(message="Provide a valid email"),validators.InputRequired(message="Email is a required field")])
    mobile = TextField('Mobile',[validators.InputRequired("Mobile is required"), validators.regexp(r'[789]\d{9}',0,"Mobile should be 10 digit number starting 7 or 8 or 9!")])
    password = PasswordField('Password',[validators.InputRequired('Password is required'), validators.EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    role = QuerySelectField('Role', query_factory=roleDropDown, get_label='name')

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        user = Person.query.filter_by(username = self.username.data).first()
        if user:
            self.username.errors.append('User exists with similar name')
            return False
        return True


class PmayExcelFileUpload(Form):
    month = IntegerField('Month',[validators.required("Month is required"), validators.NumberRange(min=1, max=12, message="Months should be between 1 and 12")])
    year = IntegerField('Year', [validators.required("Year is required!"), validators.NumberRange(min=datetime.now().year-1, max=datetime.now().year,message="Year must be between "+str(datetime.now().year-1)+" and "+ str(datetime.now().year))])
    file = FileField(validators=[FileRequired()])


def ResidenceProofTypeModelDropDown():
    return ResidenceProofTypeModel.query

def YesNoModelDropDown():
    return YesNoModel.query

def GenderModelDropDown():
    return GenderModel.query
    
def UniqueIdentificationProofModelDropDown():
    return UniqueIdentificationProofModel.query

class AddressForm(Form):
    # Non-Editable fields
    address1= StringField('Address 1', validators=[validators.data_required(message="Address 1 is required field")],render_kw={'readonly': True})
    address2= StringField('Address 2', validators=[validators.data_required(message="Address 2 is required field")],render_kw={'readonly': True})
    city= StringField('City', validators=[validators.data_required(message="City is required field")],render_kw={'readonly': True})
    state= StringField('State', validators=[validators.data_required(message=" State is required field")],render_kw={'readonly': True})
    pincode= StringField('Pincode',render_kw={'readonly': True})
    residence_proof= QuerySelectField('Residence Proof Type', query_factory=ResidenceProofTypeModelDropDown, get_label='description',render_kw={'readonly': True})
    
    # Editable fields
    active= QuerySelectField('Is Address Active', query_factory=YesNoModelDropDown, get_label='code')

class ContactPhoneForm(Form):
    # Not-Editable fields
    mobile_number = TextField('Mobile Number', render_kw={'readonly': True})
 
    # Editable fields
    active = QuerySelectField('Is Mobile Number Active', query_factory=YesNoModelDropDown, get_label='code')

class BorrowerAndFamilyForm(Form):
    # Non-Editable fields
    loan_no=StringField('Loan Account No',render_kw={'readonly': True})
    borrower_type_code=StringField('Borrower Type',render_kw={'readonly': True})
    employment_category_code=StringField('Employment Category',render_kw={'readonly': True})
    relationship=StringField('RelationshipWithPrimaryBorrower',render_kw={'readonly': True})
    
    # Editable fields
    name=StringField('Name')
    father_husband_name=StringField('Father/Husband Name')
    gender_code = QuerySelectField('Gender', query_factory=GenderModelDropDown, get_label='description')
    dob=StringField('DOB')
    pan=StringField('PAN')
    passport_no=StringField('Passport Number')
    driving_licence_no=StringField('Driving Licence No')
    voter_id=StringField('Voter Id')
    uid_proof=QuerySelectField('UID proof Type', query_factory=UniqueIdentificationProofModelDropDown, get_label='description')
    uid=StringField('UID proof others')
    uid_other_description=StringField('UID Others')

    addresses=FieldList(FormField(AddressForm))
    mobile_numbers=FieldList(FormField(ContactPhoneForm))

class InstallmentForm(Form):
    # Not-Editable fields
    loan_no = StringField('Loan Account Number', render_kw={'readonly': True})
    communication_change_required_code =  StringField('Communication Change Required', render_kw={'readonly': True})

    # Editable fields
    disbursement_installment_no= StringField('Disbursement Installment No', [validators.required('disbursement_installment_no is required!')])
    stage_of_construction_code = StringField('Stage Of Construction Code', [validators.required('stage_of_construction_code is required!')])
    npv_interest_subsidy = StringField('NPV Interest Subsidy', [validators.required('npv_interest_subsidy is required!')])

class LoanRecordForm(Form):
    # Non-Editable fields
    loan_account_number = StringField('Loan account number',render_kw={'readonly': True})
    address1=StringField('Property Address Line 1',render_kw={'readonly': True})
    address2=StringField('Property Address Line 2',render_kw={'readonly': True})
    city=StringField('City',render_kw={'readonly': True})
    pincode=StringField('Pincode',render_kw={'readonly': True})
    category_caste=StringField('Caste Category',render_kw={'readonly': True})
    category_religion=StringField('Religion Category',render_kw={'readonly': True})
    preference_given=StringField('Preference Given',render_kw={'readonly': True})
    loan_purpose_code=StringField('Loan purpose code',render_kw={'readonly': True})
    loan_interest=FloatField('Rate of Interest',render_kw={'readonly': True})
    loan_interest_type_code=StringField('Interest type',render_kw={'readonly': True})

    # Editable fields
    household_category = QuerySelectField('Household category', query_factory=householdCategoryModelDropDown, get_label='description')
    property_type = QuerySelectField('Property type', query_factory=propertyTypeModelDropDown, get_label='description')
    property_category=QuerySelectField('Property category', query_factory=propertyCategoryModelDropDown, get_label='description')
    carpet_area_classification=QuerySelectField('Property category', query_factory=carpetAreaClassificationMasterDropDown, get_label='description')
    location=QuerySelectField('Location',query_factory=statutoryTownAndPlanningModelDropDown)
    ownership=QuerySelectField('Ownership',query_factory=ownershipModeModelDropDown,get_label='description')
    loan_source = QuerySelectField('Loan source',query_factory=loanSourceModelDropDown,get_label='description')
    loan_purpose = QuerySelectField('Loan source',query_factory=loanPurposeModelDropDown,get_label='description')

    borrowers=FieldList(FormField(BorrowerAndFamilyForm))

class GetLoanNoForm(Form):
    loan_account_number = StringField('Loan account number', [validators.required('Loan account number is required!')])













    # loan_purpose_code= '0' + str(int(r['LOAN_PURPOSE'])),
    # # balance_transfer_from_other_pli= ,
    # loan_sanctioned = r['LOAN_AMOUNT_SANCTIONED'],
    # # loan_sanctioned_date

    # loan_interest_type_code= '0' + str(int(r['LOAN_INTEREST_RATE_TYPE'])),
    # loan_tenure=r['LOAN_TENURE'],
    # loan_moratorium_period=r['LOAN_MORATORIUM_PERIOD'],
    # # repayment_start_date=
    # emi_amount_in_sanction_letter=r['EMI_AMOUNT'],
    # date_of_first_disbursement=r['FIRST_DISBURSEMENT_DATE'],
    # cumulative_disbursement=r['CUMULATIVE_LOAN_DISBURSEMENT'],
    # # interest_subsidy_claimed=
    # # co_borrower_flag=
    # number_of_other_family_members=r['NUMBER_OF_FAMILY_MEMBERS'],
    # # electric_supply=
    # # drainage_sanitation=
    # stage_of_construction_code='0' + str(int(r['STAGE_OF_CONSTRUCTION']))
    #{{render_boolean_field(form.balance_transfer_from_other_pli)}}

class MasterForm(Form):
    master_tables = [('GenderModel', 'Gender'),
                   ('EmploymentCategoryModel', 'Employment Category'),
                   ('CommunicationChangeModel', 'Communication Change')
                   ]
    master_type = SelectField('Master Tables', choices=master_tables)