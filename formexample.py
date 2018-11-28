from flask import Flask, render_template, request, flash,redirect,url_for
from forms import ContactForm,ContactUpdateForm
from flask_sqlalchemy import SQLAlchemy
from tables import Results

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///contact.sqlite3'
app.config['SECRET_KEY'] = "random string"


db = SQLAlchemy(app)

class contact(db.Model):
    id = db.Column('contact_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    Gender = db.Column(db.String(10))
    Address = db.Column(db.String(200)) 
    email=db.Column(db.String(50))
    Age = db.Column(db.String(10))
    language=db.Column(db.String(10))


    
    def __init__(self, name, Gender, Address,email,Age,language):
        self.name = name
        self.Gender = Gender
        self.Address = Address
        self.email= email
        self.Age = Age
        self.language= language

@app.route('/database')
def show_all():
    return render_template('test.html', contact = contact.query.all() )

@app.route('/contact', methods = ['GET', 'POST'])
def new():
  
    form = ContactForm(request.form,csrf_enabled=True)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form = form)
        else:      
            form_contact=contact(request.form['name'], request.form['Gender'],request.form['Address'], request.form['email'],request.form['Age'],request.form['language'])
            form.populate_obj(form_contact)
            db.session.add(form_contact)
            db.session.commit()
  
            flash('Record was successfully added')
            return render_template('success.html')
                     
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('contact.html', form = form)



@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit(contact_id):
    # contact_id=4
 
    data=contact.query.filter(contact.id==contact_id).first()
    if data:
        form = ContactForm(request.form, csrf_enabled=True, obj=data)   
        if form.validate_on_submit():
            form.populate_obj(data)        
            db.session.commit()
            flash('contact updated successfully!')
            return render_template('success.html')
        return render_template('edit.html', form=form)
    else:
        return 'Error loading #{contact_id}'.format(contact_id=contact_id)

    

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
