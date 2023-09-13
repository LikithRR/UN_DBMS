#from services import prediction
from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'UN_Project'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select count(*) from Member_Nations")   
    records = cur.fetchall()
    cur.close()
    return render_template("index.html",data=records)

@app.route('/mn')
def mn():
    cur = mysql.connection.cursor()
    cur.execute("select * from Member_Nations")   
    records = cur.fetchall()
    cur.close()
    return render_template("Member_Nations.html",data=records)

@app.route('/ch_le',methods=["POST"])
def ch_le():
    details=request.form
    cur = mysql.connection.cursor()
    country_name=details['cn']
    country_leader=details["cl"]
    cur.execute("select * from Member_Nations where country_name=%s",[country_name])
    check=cur.fetchall()
    if(check):
        cur.execute("update Member_Nations set country_leader=%s where country_name=%s ",(country_leader,country_name))
        mysql.connection.commit()
        msg="THANK YOU!!! NEW COUNTRY LEADER IS UPDATED"
    else:
        msg='PLEASE ENTER VALID COUNTRY NAME'
    cur.execute("SELECT * from Member_Nations")
    records = cur.fetchall()
    cur.close()
    return render_template('Member_Nations.html',msg=msg,data=records)

@app.route('/fb')
def fb():
    cur = mysql.connection.cursor()
    cur.execute("select * from Functional_Bodies left outer join UN_Bodies_Awards on name=functional_body_name")
    records = cur.fetchall()
    cur.close()
    return render_template("Functional_Bodies.html",data=records)

@app.route('/le')
def le():
    cur = mysql.connection.cursor()
    cur.execute("select * from Leaders left outer join UN_Leader_Awards on fname = first_name")   
    records = cur.fetchall()
    cur.close()
    return render_template("Leaders.html",data=records)

@app.route('/re')
def re():
    cur = mysql.connection.cursor()
    cur.execute("select * from Representatives left outer join UN_Representatives_Awards on fname = first_name")   
    records = cur.fetchall()
    cur.close()
    return render_template("Representatives.html",data=records)

@app.route('/aw')
def aw():
    cur = mysql.connection.cursor()
    cur.execute("select * from Awards")   
    records = cur.fetchall()
    cur.close()
    return render_template("Awards.html",data=records)

@app.route('/de_aw',methods=["POST"])
def de_aw():
    details=request.form
    cur = mysql.connection.cursor()
    award_name=details['awa']
    cur.execute("select * from Awards where award_name=%s",[award_name])
    check=cur.fetchall()
    if(check):
        cur.execute("delete from Awards where award_name =%s",[award_name])
        mysql.connection.commit()
        msg="THANK YOU!!! THE AWARD HAS BEEN DELETED"
    else:
        msg='PLEASE ENTER VALID AWARD NAME'
    cur.execute("SELECT * from Awards")
    records = cur.fetchall()
    cur.close()
    return render_template('Awards.html',msg=msg,data=records)

@app.route("/in_mn_o")
def in_mn_o():
    return render_template("Insert_Member_Nations.html")

@app.route("/in_mn",methods=["POST"])
def in_mn():
    details = request.form
    veto1 = request.form.getlist("veto")
    veto = veto1
    country_name = details["country_name"]
    country_leader = details["country_leader"]
    year_of_joining = details["year_of_joining"]
    funding = details["funding"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT into Member_Nations(country_name,country_leader,year_of_joining,funding,veto_power) values(%s,%s,%s,%s,%s)",(country_name,country_leader,year_of_joining,funding,veto))
    mysql.connection.commit()
    cur.close()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)