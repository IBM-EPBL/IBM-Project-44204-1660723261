from flask import Flask,render_template, request, redirect, url_for, session

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mms40306;PWD=5PHFlcqyBiZ4kWA2",'','')

app = Flask(__name__)

@app.route("/")
def log():
    return render_template('index.html')

@app.route("/logi")
def logi():
  return render_template('login.html', name="login")


@app.route('/register',methods = ['POST'])
def register():
  if request.method == 'POST':

    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    repassword = request.form['repassword']
    contact = request.form['contact']
    role=request.form['role']
 
    sql = "SELECT * FROM login WHERE emailaddress =? "
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO login VALUES (?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, repassword)
      ibm_db.bind_param(prep_stmt, 5, contact)
      ibm_db.bind_param(prep_stmt, 6, role)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Data saved successfuly..Please login using your details")

@app.route('/login',methods=['POST'])
def login():
  
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    print(role)

    sql = "SELECT * FROM login WHERE emailaddress =? AND password=? AND role=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.bind_param(stmt,3,role)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    print(account['ROLE'])
    print(account['ROLE'].strip())
    if (account['ROLE'].strip()=="user"):
            return render_template('user.html') 
     
    elif(account['ROLE'].strip()=="admin"):
            return render_template('admin.html') 
    else:
        return render_template('login.html', msg="Login unsuccessful. Incorrect username / password !") 

@app.route("/about")
def about():
  return render_template('about.html', name="About")


@app.route("/contact")
def contact():
  return render_template('contact.html', name="Contact")


if __name__ == "__main__":
    app.run(debug=True)

