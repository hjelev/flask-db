from flask import Flask, request, redirect, url_for, render_template
import sqlite3 as sql
from functools import wraps

from urllib.parse import quote, unquote
app = Flask(__name__)


@app.route('/')
def home():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("home.html",rows = rows)

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        cur.execute("select * from students")
        
        rows = cur.fetchall();
        return render_template("list.html",msg = msg, rows = rows)
        con.close()

@app.route('/updaterec',methods = ['POST', 'GET'])
def updaterec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         id = request.form['id']

         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("UPDATE students SET name = ?, addr = ?, city = ?, pin = ? WHERE id = ?",
            (nm,addr,city,pin,id))
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        cur.execute("select * from students")
        
        rows = cur.fetchall();
        return render_template("list.html",msg = msg, rows = rows)
        con.close()

@app.route('/delete/<id>',methods = ['POST', 'GET'])
def deleterec(id):
   id = request.view_args['id']
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute(f"delete from students where id = {id}")
   con.commit()
   cur.execute("select * from students")
   rows = cur.fetchall();
   return render_template("list.html",rows = rows, id=id)


@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/edit/<id>')
def edit(id):
   id = request.view_args['id']
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute(f"select * from students where id = {id}")
   
   rows = cur.fetchall();
   return render_template("edit.html",rows = rows, id=id)

if __name__ == '__main__':
   app.run(debug = True)