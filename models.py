#ref http://flask-sqlalchemy.pocoo.org/2.3/
#q=db.session.query(Person).filter(Person.roles.any(Role.name==r.name)).all()
#TODO onupdate=datetime.datetime.now include this in all tables

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from .db import db



roles = db.Table(
    'role_users',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
class YesNoModel(db.Model):
    __tablename__='yes_no_master'
    id = db.Column(db.String(2),primary_key=True)
    code = db.Column(db.String(5), unique=True)
class Employee(db.Model):
    __tablename__ = 'employee'
    emp_no = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date, nullable=True)
    first_name=db.Column(db.String(120))
    middle_name=db.Column(db.String(120),nullable=True)
    last_name=db.Column(db.String(120))
    emloyee_id = db.Column(db.String(30), unique=True)
    users=db.relationship('Person', backref='employee', lazy=True)

    def __repr__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} ({self.emloyeeId})"
#TODO do we need a field for isAuthentiated?

class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    firstName=db.Column(db.String(80))
    middleName=db.Column(db.String(80), nullable=True)
    lastName=db.Column(db.String(80))
    email = db.Column(db.String(),unique=True)
    mobile = db.Column(db.String())
    password = db.Column(db.String())
    active = db.Column(db.Boolean())
    # addresses = db.relationship('Address', backref='person', lazy='dynamic')
    roles = db.relationship('Role',lazy='subquery', secondary='role_users',  backref=db.backref("person",lazy=True))
    vendor_id=db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=True)
    employee_emp_no=db.Column(db.Integer, db.ForeignKey('employee.emp_no'), nullable=True)
    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def check_password(self,value):
        return check_password_hash(self.password, value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def role_list(self):
        return ', '.join(role.name for role in self.roles)

    def has_role(self, role):
        for r in self.roles:
            if r.name == role:
                return True
        return False

    def isVendor(self):
        if self.vendor_id:
            return True
        else:
            return False

    def __repr__(self):
        return 'User - {} with role {}'.format(self.username)

    def getName(self):
        return '{} {} {}'.format(self.firstName, self.middleName, self.lastName)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class CountryMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    country = db.Column(db.String(2))
    isd_code = db.Column(db.String(20))
    latitude = db.Column(db.Float(12,7))
    longitude = db.Column(db.Float(12,7))
    created_at = db.DateTime()
    updated_at = db.DateTime()

    # def __str__(self):
    #     return f"{self.name} ({self.country}) - (ISD - {self.isdCode})"



class state_master(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    alpha_code = db.Column(db.String(2))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    districts = db.relationship('district_master', backref='state_master', lazy=True)
    pincodes = db.relationship('unique_pincode', backref='state_master', lazy=True)

    def __repr__(self):
        return f"{self.name}"

class district_master(db.Model):
    district=db.Column(db.String(80),primary_key=True)
    state = db.Column(db.Integer, db.ForeignKey('state_master.code'), nullable=False)
    pincodes = db.relationship('pincode_master', backref='state_master', lazy=True)

class unique_pincode(db.Model):
    id=db.Column(db.String(10), primary_key=True) #pincode is the key
    state = db.Column(db.Integer, db.ForeignKey('state_master.code'), nullable=False)

class pincode_master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(10), db.ForeignKey('unique_pincode.id'), nullable=False)
    office_name = db.Column(db.String(80))
    office_type = db.Column(db.String(64))
    delivery_status = db.Column(db.String(64))
    division = db.Column(db.String(80))
    region = db.Column(db.String(80))
    circle = db.Column(db.String(80))
    taluk = db.Column(db.String(80))
    district = db.Column(db.String(80), db.ForeignKey('district_master.district'), nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('state_master.code'), nullable=False)


#     def __str__(self):
#         return f"{self.pincode} - {self.officeName}, {self.taluk}, {self.district}, {self.state.name}"

class VendorStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status =  db.Column(db.String(30), unique=True)
    vendors=db.relationship('Vendor',backref='vendor_status',lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())


class Vendor(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    orgId=db.Column(db.String(30), unique=True)
    name = db.Column(db.String(120), nullable=False)
    addrline1 = db.Column(db.String(120), nullable=False)
    addrline2 = db.Column(db.String(120), nullable=True)
    addrline3 = db.Column(db.String(120), nullable=True)
    addrline4 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=False)
    contactPerson = db.Column(db.String(120), nullable=True)
    landmark = db.Column(db.String(120), nullable=True)
    contactEmail = db.Column(db.String(80), nullable=False)
    alternateEmail = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.String(20), nullable=False)
    alternateNumber = db.Column(db.String(20), nullable=True)
    pincode =  db.Column(db.String(10), db.ForeignKey('unique_pincode.id'), nullable=False)
    pan = db.Column(db.String(10), nullable=False)
    dateOfCommencement = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status_id = db.Column(db.Integer, db.ForeignKey('vendor_status.id'),nullable=False)

class BranchMaster(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    branch_code=db.Column(db.String(60),unique=True)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120), nullable=True)
    address3 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120))
    pincode=db.Column(db.String(10), db.ForeignKey(unique_pincode.id))

class UniqueIdentificationProofModel(db.Model):
    __tablename__ = 'id_proof_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('BorrowerAndFamilyModel')

class GenderModel(db.Model):
    __tablename__ = 'gender_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('BorrowerAndFamilyModel')


class EmploymentCategoryModel(db.Model):
    __tablename__ = 'employment_category_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('BorrowerAndFamilyModel')

class CommunicationChangeModel(db.Model):
    __tablename__ = 'communication_change_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    installments=db.relationship('InstallmentModel')


class ResidenceProofTypeModel(db.Model):
    __tablename__ = 'residence_proof_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('AddressModel')

class CategoryCasteModel(db.Model):
    __tablename__ = 'caste_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class CategoryReligionModel(db.Model):
    __tablename__ = 'religion_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')
    # def __str__(self):
    #     return self.description
    

class PreferenceGivenModel(db.Model):
    __tablename__ = 'customer_type_preference_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class HouseholdCategoryModel(db.Model):
    __tablename__ = 'household_category_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class PropertyTypeModel(db.Model):
    __tablename__ = 'property_type_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class PropertyCategoryModel(db.Model):
    __tablename__ = 'property_category_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class CarpetAreaClassificationMaster(db.Model):
    __tablename__ = 'carpet_area_classification_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')


class OwnershipModeModel(db.Model):
    __tablename__ = 'ownership_mode_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class StageOfConstructionModel(db.Model):
    __tablename__ = 'stage_of_construction_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')
    installments=db.relationship('InstallmentModel')

class LoanSourceModel(db.Model):
    __tablename__ = 'loan_source_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class LoanPurposeModel(db.Model):
    __tablename__ = 'loan_purpose_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class LoanInterestTypeModel(db.Model):
    __tablename__ = 'loan_interest_type_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    loans = db.relationship('PmayLoanModel')

class RelationshipWithPrimaryBorrower(db.Model):
    __tablename__ = 'relationship_with_primary_borrower_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    borrowers = db.relationship('BorrowerAndFamilyModel')
    def __str__(self):
        return self.description
    

class BorrowerTypeModel(db.Model):
    __tablename__='borrower_type_master'
    code = db.Column(db.String(2),primary_key=True)
    description=db.Column(db.String(80),unique=True)
    borrowers = db.relationship('BorrowerAndFamilyModel')
    
class StatutoryTownAndPlanningModel(db.Model):
    __tablename__ = 'statutory_town_and_panning_code_master'
    town_planning_area_code = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.Integer)
    state = db.Column(db.String(80))
    distict_code=db.Column(db.Integer)
    town_planning_area_name=db.Column(db.String(80))
    loans = db.relationship('PmayLoanModel')
    def __repr__(self):
        return "{}, {}".format(self.town_planning_area_name,self.town_planning_area_name)


class PmayLoanModel(db.Model):
    __tablename__ = 'pmay_loans'
    loan_account_number=db.Column(db.String(20), primary_key=True)
    installments = db.relationship('InstallmentModel')
    category_caste = db.Column(db.String(2),db.ForeignKey('caste_master.code'))
    caste = db.relationship('CategoryCasteModel')
    category_religion = db.Column(db.String(2), db.ForeignKey('religion_master.code'))
    religion = db.relationship('CategoryReligionModel')
    preference_given =db.Column(db.String(2), db.ForeignKey('customer_type_preference_master.code'))
    preference = db.relationship('PreferenceGivenModel')
    household_category_code = db.Column(db.String(2), db.ForeignKey('household_category_master.code'))
    household_category = db.relationship('HouseholdCategoryModel')
    household_annual_income = db.Column(db.Integer)
    property_type_code = db.Column(db.String(2), db.ForeignKey('property_type_master.code'))
    property_type = db.relationship('PropertyTypeModel')
    property_category_code = db.Column(db.String(2), db.ForeignKey('property_category_master.code'))
    property_category= db.relationship('PropertyCategoryModel')
    carpet_area_classification_code = db.Column(db.String(2), db.ForeignKey('carpet_area_classification_master.code'))
    carpet_area_classification = db.relationship('CarpetAreaClassificationMaster')
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    pincode = db.Column(db.String(10),db.ForeignKey('unique_pincode.id'))
    location_code = db.Column(db.Integer, db.ForeignKey('statutory_town_and_panning_code_master.town_planning_area_code'))
    location = db.relationship('StatutoryTownAndPlanningModel')
    ownership_mode = db.Column(db.String(2), db.ForeignKey('ownership_mode_master.code'))
    ownership = db.relationship('OwnershipModeModel')
    loan_source_code = db.Column(db.String(2), db.ForeignKey('loan_source_master.code'))
    loan_source= db.relationship('LoanSourceModel')
    loan_purpose_code = db.Column(db.String(2), db.ForeignKey('loan_purpose_master.code'))
    loan_purpose = db.relationship('LoanPurposeModel')
    balance_transfer_from_other_pli_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    loan_sanctioned = db.Column(db.Float)
    loan_sanctioned_date = db.Column(db.Date)
    loan_interest = db.Column(db.Float)
    loan_interest_type_code = db.Column(db.String(2), db.ForeignKey('loan_interest_type_master.code'))
    loan_interest_type = db.relationship('LoanInterestTypeModel')
    loan_tenure = db.Column(db.Integer)
    loan_moratorium_period = db.Column(db.Integer)
    repayment_start_date = db.Column(db.Date)
    emi_amount_in_sanction_letter = db.Column(db.Float)
    date_of_first_disbursement = db.Column(db.Date)
    cumulative_disbursement = db.Column(db.Float)
    interest_subsidy_claimed = db.Column(db.Float)
    co_borrower_flag_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    number_of_other_family_members = db.Column(db.Integer)
    water_supply_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    electric_supply_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    drainage_sanitation_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    stage_of_construction_code = db.Column(db.String(2),db.ForeignKey('stage_of_construction_master.code'))
    stage_of_construction=db.relationship('StageOfConstructionModel')
    borrowers = db.relationship('BorrowerAndFamilyModel')

class BorrowerAndFamilyModel(db.Model):
    __tablename__='borrower_and_family'
    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), db.ForeignKey('pmay_loans.loan_account_number'))
    loan = db.relationship('PmayLoanModel')
    name = db.Column(db.String(80))
    father_husband_name=db.Column(db.String(80))
    borrower_type_code = db.Column(db.String(2),db.ForeignKey('borrower_type_master.code'))
    borrower_type = db.relationship('BorrowerTypeModel')
    relationship_with_primary_borrower_code = db.Column(db.String(2),db.ForeignKey('relationship_with_primary_borrower_master.code'))
    relationship = db.relationship('RelationshipWithPrimaryBorrower')
    uid_proof = db.Column(db.String(2), db.ForeignKey('id_proof_master.code'), nullable=False)
    uid_other_description=db.Column(db.String(30))
    uid = db.Column(db.String(30))
    gender_code=db.Column(db.String(2),db.ForeignKey('gender_master.code'))
    gender = db.relationship('GenderModel')
    dob = db.Column(db.Date)
    pan = db.Column(db.String(10))
    passport_no=db.Column(db.String(12))
    driving_licence_no=db.Column(db.String(20))
    voter_id=db.Column(db.String(20))
    employment_category_code=db.Column(db.String(2),db.ForeignKey('employment_category_master.code'))
    employment_category = db.relationship('EmploymentCategoryModel')
    addresses = db.relationship('AddressModel')
    mobile_numbers = db.relationship('ContactPhoneModel')

class AddressModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowers_and_family_id = db.Column(db.Integer, db.ForeignKey('borrower_and_family.id'))
    borrower_and_family = db.relationship('BorrowerAndFamilyModel')
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10),db.ForeignKey('unique_pincode.id'))
    active_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    date_created = db.Column(db.Date)
    date_last_updated = db.Column(db.Date)
    residence_proof_code = db.Column(db.String(2),db.ForeignKey('residence_proof_master.code'))
    residence_proof = db.relationship('ResidenceProofTypeModel')

class ContactPhoneModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowers_and_family_id = db.Column(db.Integer, db.ForeignKey('borrower_and_family.id'))
    borrower_and_family = db.relationship('BorrowerAndFamilyModel')
    mobile_number = db.Column(db.String(10))
    active_id = db.Column(db.String(5),db.ForeignKey('yes_no_master.id'))
    date_created = db.Column(db.Date)
    date_last_updated = db.Column(db.Date)

class InstallmentModel(db.Model):
    __tablename__ = 'installments'
    id=db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), db.ForeignKey('pmay_loans.loan_account_number'))
    loan=db.relationship('PmayLoanModel')
    disbursement_installment_no=db.Column(db.Integer)
    stage_of_construction_code = db.Column(db.String(2),db.ForeignKey('stage_of_construction_master.code'))
    stage_of_construction=db.relationship('StageOfConstructionModel')
    communication_change_required_code=db.Column(db.String(2),db.ForeignKey('communication_change_master.code'))
    communication_change=db.relationship('CommunicationChangeModel')
    npv_interest_subsidy = db.Column(db.Float)
