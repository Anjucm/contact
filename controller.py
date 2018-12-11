import os
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, current_app
from jinja2 import TemplateNotFound
from sqlalchemy.exc import IntegrityError
from simflow.forms import LoanRecordForm
from simflow.models import Person, db, Role, PmayLoanModel, HouseholdCategoryModel, PropertyTypeModel,GenderModel
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
from simflow.extensions import login_manager
from simflow.forms import validators, PmayExcelFileUpload,MasterForm
from simflow.extensions import Identity, AnonymousIdentity, identity_changed, admin_permission
from sqlalchemy import desc
from simflow.utils import printError
from flask_restful import Api
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS=['xlsx','xls']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

pmay = Blueprint(
    'pmay',
    __name__,
    template_folder='templates'
)

@pmay.route("/")
def pmay_home():
    return render_template ("pmay/index.html")

@pmay.route("/master", methods=["GET","POST"])
def newAddress():
    form=MasterForm()
    
    if form.validate_on_submit():
        # print(form.master_type.data)
        tablename=request.form['master_type']
        print(tablename)
        # address = AddressModel()
        # address.active=form.active.data
        # db.session.add(address)
        db.session.commit()
        return redirect(url_for('pmay.show_all',tablename=tablename))
        # return redirect(url_for('pmay.gender',tablename=tablename))
    else:
        printError(form)


    return render_template('pmay/master.html', form=form)

@pmay.route('/<tablename>',methods=['GET', 'POST'])
def show_all(tablename):
    print(tablename)
    var = 'tablename'
    table = getattr(simflow.models, var)
    return render_template('pmay/gender.html', contact = table.query.all())