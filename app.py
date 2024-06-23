from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL
from datetime import timedelta


app = Flask(__name__, template_folder='template')
app.secret_key = 'abc'
app.permanent_session_lifetime = timedelta(minutes=4)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Hari@2822"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/userManagement')
def home():
    if 'userLogin' in session:
        conn = mysql.connection.cursor()
        sql = "SELECT * FROM users"
        conn.execute(sql)
        res = conn.fetchall()
        return render_template('head.html', datas=res)
    return redirect(url_for('login'))


# @app.route('/search', methods=["GET", "POST"])
# def getusers(search):

#     @app.route('/count')
#     def count():
#         conn = mysql.connection.cursor()
#         sql = 'SELECT COUNT(*) FROM USERS'
#         conn.execute(sql)
#         render_template('head.html')

    # @app.route('/<string:id>/userManagement', methods=['POST', 'GET'])
    # def user(id):
    #     conn = mysql.connection.cursor()
    #     if request.method == 'POST':
    #         user = request.form.get('username')
    #         password = request.form.get('password')
    #         sql = "select * from userLogin where name = %s and password = %s"
    #         conn.execute(sql, [user, password, id])
    #         if conn.fetchone() is not None:
    #             session.permanent = True
    #             session['userLogin'] = user
    #             sql = 'select * from users'
    #             conn.execute(sql, [id])
    #             res = conn.fetchall()
    #             return redirect(url_for('home'))
    #     return render_template('head.html', data=res)


@app.route('/register', methods=['POST', 'GET'])
def register():
    conn = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sql = "insert into userLogin(name,email,password) values(%s,%s,%s)"
        conn.execute(sql, [name, email, password])
        mysql.connection.commit()
        conn.close()
        flash('you are successfully registered in!')
        return redirect(url_for('login'))
    return render_template('Signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    conn = mysql.connection.cursor()
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        sql = "select * from userLogin where name = %s and password = %s"
        conn.execute(sql, [user, password])
        if conn.fetchone() is not None:
            session.permanent = True
            session['userLogin'] = user
            flash('you are successfully logged in ')
            return redirect(url_for('home'))
        flash('Wrong username / password')
    return render_template('login page.html')


headings = ('ID', 'NAME', 'AGE', 'CITY')
data = (
    ('1', 'hari', '20', 'Madurai'),
    ('2', 'jeeva', '20', 'Madurai'),
)


@app.route('/dashboard')
def dashboard():
    if "userLogin" in session:
        return render_template('dashboard.html', headings=headings, data=data)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.pop('userLogin', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/addUsers', methods=['GET', 'POST'])
def addUsers():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        conn = mysql.connection.cursor()
        sql = "insert into users(name,age,city) value(%s,%s,%s)"
        conn.execute(sql, [name, age, city])
        mysql.connection.commit()
        conn.close()
        flash('User added successfully!')
        return redirect(url_for('home'))
    return render_template('addusers.html')


@app.route('/editUsers/<string:id>', methods=['POST', 'GET'])
def editUsers(id):
    conn = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        sql = "update users set NAME =%s,AGE=%s,CITY=%s where ID =%s"
        conn.execute(sql, [name, age, city, id])
        mysql.connection.commit()
        conn.close()
        flash('User details updated!')
        return redirect(url_for("home"))

    sql = "select * from users where ID = %s"
    conn.execute(sql, [id])
    res = conn.fetchone()
    return render_template('updateUser.html', datas=res)


# @app.route('/forgetpassword/<string:id>', methods=['POST', 'GET'])
# def forgetPass(id):
#     conn = mysql.connection.cursor()
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         sql = "update userLogin set Name = %s , password = %s where ID = %s"
#         conn.execute(sql, [name, password, id])
#         return redirect(url_for('login'))
#     sql = 'select * from userLogin where ID = %s'
#     conn.execute(sql, [id])
#     res = conn.fetchone()
#     return render_template('forgetPass.html')
# @app.route('/forgetPassword/<string:id>', methods=['POST', 'GET'])
# def forgetPassword(id):
#     conn = mysql.connection.cursor()
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['age']
#         sql = "update userLogin set NAME =%s, PASSWORD=%s where ID =%s"
#         conn.execute(sql, [name, password, id])
#         mysql.connection.commit()
#         conn.close()
#         return redirect(url_for("login"))

#     sql = "select * from userLogin where ID = %s"
#     conn.execute(sql, [id])
#     res = conn.fetchone()
#     return render_template('updateUser.html', datas=res)


@app.route('/deleteUsers/<string:id>', methods=['GET', 'POST'])
def deleteUsers(id):
    conn = mysql.connection.cursor()
    sql = "delete from users where ID = %s"
    conn.execute(sql, [id])
    mysql.connection.commit()
    conn.close()
    flash('One user deleted!')
    return redirect(url_for("home"))


@app.route('/truncate', methods=['GET', 'POST'])
def truncate():
    conn = mysql.connection.cursor()
    sql = 'TRUNCATE TABLE USERS'
    conn.execute(sql)

    mysql.connection.commit()
    conn.close()
    flash('User Details Truncated!')
    return redirect(url_for('home'))


@app.route('/cantact')
def cantact():
    return render_template('cantact.html')


if __name__ == '__main__':
    #app.run(debug=True, port=5000)
    app.run(debug=False,host='0.0.0.0')
