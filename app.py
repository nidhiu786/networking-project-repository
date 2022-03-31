from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
 
app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/meetjoshi/Documents/example.db'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db' 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
 
# Settings for migrations
migrate = Migrate(app, db)
 
# Models
class Project(db.Model):
    # Id : Field which stores unique id for every row in
    # database table.
    # project_title: Used to store the project title of the Project
    # tools_technology: Used to store tools and technology of the Project
    # project_descr: Used to store the project_descr of the Project
    
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(50), unique=False, nullable=False)
    tools_technology = db.Column(db.String(150), unique=False, nullable=False)
    project_descr = db.Column(db.String(200), unique=False, nullable=False)
 
    def __init__(self,project_title,tools_technology,project_descr):
        self.project_title = project_title
        self.tools_technology = tools_technology
        self.project_descr = project_descr

db.create_all()
db.session.commit()

 
# function to render index page
# @app.route('/')
# def index():
#     projects = Project.query.all()
#     # print(projects)
#     return render_template('index.html', projects=projects)

# function to render introduction page 
@app.route('/')
@app.route('/introduction.html')
def introduction():
    return render_template('introduction.html')

# function to render skillset page 
@app.route('/skillset.html')
def skillset():
    return render_template('skillset.html')   

# function to render education page 
@app.route('/education.html')
def education():
    return render_template('education.html')  

# function to render education page 
@app.route('/project.html')
def project():
    # return render_template('project.html')
    projects = Project.query.all()
    return render_template('project.html', projects=projects)

# function to render add_projects page 
@app.route('/add_data')
def add_data():
    return render_template('add_projects.html')
    
# function to add profiles
@app.route('/add', methods=["POST"])
def Projects():
    # In this function we will input data from the
    # form page and store it in our database. Remember
    # that inside the get the name should exactly be the same
    # as that in the html input fields
    project_title = request.form.get("project_title")
    tools_technology = request.form.get("tools_technology")
    project_descr = request.form.get("project_descr")
 
    # create an object of the Profile class of models and
    # store data as a row in our datatable
    if project_title!= '' and tools_technology != '' and project_descr != '':
        p = Project(project_title=project_title,tools_technology=tools_technology, project_descr=project_descr)
        db.session.add(p)
        db.session.commit()
        return redirect('/project.html')
    else:
        return redirect('/project.html')
 
@app.route('/delete/<int:id>')
def erase(id):
     
    # deletes the data on the basis of unique id and
    # directs to home page
    data = Project.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/project.html')
 
if __name__ == '__main__':
    # db.create_all()
    app.run(debug = True)