from flask import Flask, render_template, url_for, request, redirect

# configure SQLALchemy and Flask to work together.
from flask_migrate import Migrate


from models import db, Student

app = Flask(__name__)

# provide a location for our database.
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///school.db'
# initialize
db.init_app(app)
migrate = Migrate(app=app, db=db)



@app.route('/')
def home():
    return f'Welcome!'


@app.route('/student/<int:id>/')
def single_student(id):
    student = Student.query.filter_by(id=id).first()
    return render_template('index.html', student= student)


@app.route('/students')
def all_students():
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/add_student', methods=['POST', 'GET'])
def create_student():
    if request.method == 'POST':
        data = request.form
        new_student = Student(first_name = data.get('first_name'), last_name = data.get('last_name'), email = data.get('email'))
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('all_students'))

    return render_template('add_student.html')


@app.route('/update_student/<int:id>/', methods=['POST','GET'])
def update_student(id):
    student = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        data = request.form
        student.first_name = data.get('first_name')
        student.last_name = data.get('last_name')
        student.email = data.get('email')
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('all_students'))
    return render_template('update-student.html', student= student)

@app.route('/delete_student/<int:id>/', methods=['POST','GET'])
def delete_student(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('all_students'))
