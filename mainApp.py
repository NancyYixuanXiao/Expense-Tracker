from flask import Flask, render_template, flash, request, url_for, redirect, session
from passlib.hash import sha256_crypt
from datetime import date

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Registration, Expenses, Base

engine = create_engine('sqlite:///userexpenses.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

@app.route('/')
@app.route('/main')
def homepage():
	return render_template("main.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
	try:
		if request.method == 'POST':
			attemped_username = request.form['username']
			attemped_password = request.form['password']

			user = dbsession.query(Registration).filter_by(username = attemped_username).one()

			if user:
				if sha256_crypt.verify(attemped_password, user.password):
					session['logged_in'] = True
					session['username'] = user.username
					flash("You are logged in")
					return redirect(url_for('loggedInHome', user_id = user.id))
				else:
					flash("Incorrect password.")
					return render_template("login.html")
			else:
				flash("Username does not exist.")
				return render_template("login.html")
		flash("Please enter form data.")
		return render_template("login.html")

	except:
		return render_template("login.html")

@app.route('/logout/')
def logout():
	if session:
		session.clear()
		flash("You are logged out.")
		return redirect(url_for('homepage'))
	else:
		flash("You are not logged in.")
		return redirect(url_for('homepage'))

@app.route('/register/', methods = ['GET', 'POST'])
def register():
	try: 
		if request.method == 'POST':
			if (request.form['password'] != request.form['confirm']):
				flash("Passwords do not match!")
				return render_template("register.html")

			attemped_username = request.form['username']
			attemped_password = sha256_crypt.encrypt(request.form['password'])

			query = dbsession.query(Registration).filter_by(username = attemped_username).first()
			if query:
				flash("Username already taken.")
				return render_template("register.html")
			else:
				newUser = Registration(username = attemped_username, password = attemped_password)
				dbsession.add(newUser)
				dbsession.commit()
				session['logged_in'] = True
				session['username'] = newUser.username
				return redirect(url_for('loggedInHome', user_id = newUser.id))

		flash("Please enter form data")
		return render_template("register.html")

	except Exception as e:
		return render_template("register.html")

@app.route('/user/<int:user_id>/', methods = ['GET', 'POST'])
# @app.route('/user/<int:user_id>/timerange', methods = ['GET', 'POST'])
def loggedInHome(user_id):
	try:
		if request.method == 'POST':
			expenses = dbsession.query(Expenses).filter(user_id == user_id, date >= request.form['time1'], date <= request.form['time2']).all()
			return render_template("loggedInHome.html", user_id = user_id, expenses = expenses)
		else:
			expenses = dbsession.query(Expenses).filter_by(user_id = user_id).all()
			return render_template("loggedInHome.html", user_id = user_id, expenses = expenses)
	except:
		expenses = dbsession.query(Expenses).filter_by(user_id = user_id).all()
		return render_template("loggedInHome.html", user_id=user_id, expenses=expenses)

@app.route('/user/<int:user_id>/add', methods = ['GET', 'POST'])
def add_expense(user_id):
	try: 
		if request.method == 'POST':
			newExpense = Expenses(price = request.form['price'],
								  date = date.today(),
								  description = request.form['description'],
								  user_id = user_id)
			dbsession.add(newExpense)
			dbsession.commit()
			flash("Add a new expense!")
			return redirect(url_for('loggedInHome', user_id = user_id))
		print("get method called")
		flash("Please enter form data")
		return render_template("add_expense.html", user_id = user_id)

	except:
		return render_template("add_expense.html", user_id = user_id)


@app.route('/user/<int:user_id>/<int:expense_id>/edit', methods = ['GET', 'POST'])
def edit_expense(user_id, expense_id):
	try:
		editedExpense = dbsession.query(Expenses).filter_by(id = expense_id).one()
		if request.method == 'POST':
			editedExpense.price = request.form['price']
			editedExpense.description = request.form['description']
			dbsession.add(editedExpense)
			dbsession.commit()
			return redirect(url_for('loggedInHome', user_id = user_id))
		else:
			return render_template('edit_expense.html', user_id = user_id, expense_id = expense_id, expense = editedExpense)
	except:
		return redirect(url_for('loggedInHome', user_id = user_id))

@app.route('/user/<int:user_id>/<int:expense_id>/delete', methods = ['GET', 'POST'])
def delete_expense(user_id, expense_id):
	try:
		expenseToDelete = dbsession.query(Expenses).filter_by(id = expense_id).one()
		if request.method == 'POST':
			dbsession.delete(expenseToDelete)
			dbsession.commit()
			return redirect(url_for('loggedInHome', user_id = user_id))
		else:
			return render_template('delete_expense.html', user_id = user_id, expense_id = expense_id, expense = expenseToDelete)
	except:
		pass

@app.route('/user/<int:user_id>/<expenses>/', methods = ['GET', 'POST'])
def weekly_report(user_id, expenses):
	render_template('weekly_report.html', user_id = user_id, expenses = expenses)


if __name__ == '__main__':
	app.secret_key = "supper_secret_key"
	app.debug = True
	app.run(host = "127.0.0.1", port = 8080)