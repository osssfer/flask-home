from flask import Flask, flash, render_template,request,url_for,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testpydb'
app.secret_key = 'secreat_key'

mysql = MySQL(app)

@app.route('/')
def home ():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contact")
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add',methods = ['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact(fullname,phone,email ) VALUES (%s, %s, %s)", (fullname,phone,email))
        mysql.connection.commit()
        cur.close()
        flash('AGREGADO OK')
        return redirect(url_for('home'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contact WHERE id ={}".format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html',contact = data[0])


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contact WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('BORRADO OK')
    return redirect(url_for('home'))


@app.route('/update/<id>',methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE contact
                    SET fullname = %s,
                        phone = %s,
                        email = %s 
                    WHERE id = %s """,(fullname,phone,email,id))
        mysql.connection.commit()
        flash('ACTUALIZADO')
    else:
        flash('Sin cambios..')
    return redirect(url_for('home'))    

if __name__ == '__main__':
    app.run(port=3000, debug=True)