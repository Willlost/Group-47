from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app= Flask(__name__)
app.secret_key="flash message"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="fdmapp"
mysql=MySQL(app)



@app.route('/')

def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()
    return render_template('home.html' , employees = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_a = request.form['password']

        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("select position from employees where username=%s and password=%s", (username, password_a))


        if result > 0:
            position, = cur.fetchone()
            print(position)
            userid = cur.execute("select id from employees where username=%s", (username,))
            uid, = cur.fetchone()
            flash('You are now logged in', 'success')
            if position == 'Admin':
                return redirect(url_for('Admin'))
            elif position == 'Manager':
                return redirect(url_for('Manager'))
            return redirect(url_for('Employee', id_data=uid))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)

            cur.close()

    return render_template('login.html')


@app.route('/Admin')
def Admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()
    return render_template("index.html", employees=data)


@app.route('/Manager')
def Manager():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses WHERE status=%s",("Unverified",))
    data = cur.fetchall()
    cur.close()
    return render_template('manager.html', expenses=data)


@app.route('/Employee/<string:id_data>', methods=['POST', 'GET'])
def Employee(id_data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses WHERE Uid=%s", (id_data,))
    data = cur.fetchall()
    cur.close()
    return render_template('employee.html', expenses=data)


@app.route('/insert', methods=['POST'])

def insert():
    if request.method=="POST":
        flash('Added Successfully')
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO  employees(name, position, email, username, password) VALUES(%s, %s, %s, %s, %s)",(name, position, email, username, password))
        mysql.connection.commit()
        return redirect(url_for('Admin'))

@app.route('/expense', methods=['POST'])

def expense():
    if request.method =="POST":
        flash('Submitted Successfully')
        id_data = request.form['id']
        subject = request.form['subject']
        comment = request.form['comment']
        cost = request.form['cost']

        cur = mysql.connection.cursor()
        owner = cur.execute("SELECT name FROM employees WHERE id=%s", (id_data))[1]
        cur.execute("INSERT INTO  expenses(owner, subject, comment, cost, status, Uid) VALUES(%s, %s, %s, %s, %s, %s)", (owner, subject, comment, cost, "Unverified", id_data))
        mysql.connection.commit()
        return redirect(url_for('Employee', uid=id_data))

@app.route('/approve/<string:id_data>', methods = ['POST','GET'])
def approve(id_data):
    flash('Expense approved!')
    cur = mysql.connection.cursor()
    cur.execute('UPDATE expenses SET status=%s WHERE id=%s', ("Approved", id_data))
    mysql.connection.commit()
    return redirect(url_for('Manager'))

@app.route('/disapprove/<string:id_data>', methods = ['POST','GET'])
def disapprove(id_data):
    flash('Expense disapproved!')
    cur = mysql.connection.cursor()
    cur.execute('UPDATE expenses SET status=%s WHERE id=%s', ("Disapproved", id_data))
    mysql.connection.commit()
    return redirect(url_for('Manager'))

@app.route('/update', methods=['POST','GET'])
def update():
    if request.method=='POST':
        id_data = request.form['id']
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("""UPDATE employees SET name=%s, position=%s, email=%s, username=%s, password=%s WHERE id=%s""" ,(name,position,email,username,password, id_data))
        flash("Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Admin'))


@app.route('/delete/<string:id_data>', methods = ['POST','GET'])
def delete(id_data):
    flash('Deleted Successfully')
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM employees WHERE id=%s', (id_data,) )
    mysql.connection.commit()
    return redirect(url_for('Admin'))






if __name__=="__main__":
    app.run(debug=True)