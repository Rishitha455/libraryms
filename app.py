from flask import Flask, redirect, url_for, render_template, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database configurations (example, you need to adjust based on your environment)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin'
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/allinfo', methods=['GET', 'POST'])
def info():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM library')
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        sno = request.form['sno']
        bookname = request.form['bookname']
        author = request.form['author']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO library(sno, bookname, author) VALUES(%s, %s, %s)', [sno, bookname, author])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        sno = request.form['sno']
        bookname = request.form['bookname']
        author = request.form['author']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE library SET bookname=%s, author=%s WHERE sno=%s', [bookname, author, sno])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home'))
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        sno = request.form['sno']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM library WHERE sno=%s', [sno])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home'))
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
