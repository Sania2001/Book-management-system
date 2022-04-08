import flask
from flask import Flask, request, render_template, redirect
import sqlite3

conn = sqlite3.connect("Library.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='book' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE book(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, 
                            author TEXT, 
                            category TEXT, 
                            price INTEGER,
                            publisher TEXT, 
                            username TEXT, 
                            Password TEXT); ''')
print("Table has created")

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='users' ").fetchall()

if listOfTables!=[]:
    print("User table already exists !")

else:
    conn.execute(''' CREATE TABLE users(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                mname TEXT, 
                                address TEXT, 
                                emailid TEXT, 
                                phone INTEGER,
                                mpassword TEXT); ''')


app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUsername = request.form["username"]
        getppass = request.form["password"]

        if getUsername == "admin":
            if getppass == "9875":
                return redirect("/admin")
    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")


@app.route("/bookentry", methods = ["GET","POST"])
def BooksEntry():

    if request.method == "POST":
        getName = request.form["name"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        getUsername = request.form["username"]
        getPassword = request.form["password"]

        print(getName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        print(getUsername)
        print(getPassword)
        try:
            conn.execute("INSERT INTO book(name, author, category, price, publisher, username, password )VALUES('"+getName+"','"+getAuthor+"','"+getCategory+"','"+getPrice+"','"+getPublisher+"','"+getUsername+"','"+getPassword+"')")
            print("Successfully inserted")
            conn.commit()
            return redirect("/view")

        except Exception as e:
            print(e)
    return render_template("booksentry.html")

@app.route("/view")
def view():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    res = cursor.fetchall()
    return render_template("viewall.html", book=res)


@app.route("/cardview")
def cardview():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    result = cursor.fetchall()
    return render_template("cardview.html", book = result)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getName = request.form["name"]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book WHERE name = '"+getName+"' ")
        result = cursor.fetchall()
        return render_template("searchbooks.html", books=result)
    return render_template("search.html")


@app.route("/edit", methods = ['GET','POST'])
def edit():
        if request.method == "POST":
            getName = request.form["name"]
            getAuthor = request.form["author"]
            getCategory = request.form["category"]
            getPrice = request.form["price"]
            getPublisher = request.form["publisher"]
            getUsername = request.form["username"]
            getPassword = request.form["password"]

            conn.execute("UPDATE book SET author = '" + getAuthor + "',category='" + getCategory + "',price = '" + getPrice + "',publisher = '" + getPublisher + "',username = '"+getUsername+"', password = '"+getPassword+"' WHERE name = '" + getName + "' ")
            print("successfully Updated !")
            conn.commit()
            return redirect("/view")
        return render_template("edit.html")


@app.route("/delete", methods =['GET','POST'])
def delete():
        if request.method == "POST":
            getName = request.form["name"]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE name = '" + getName + "' ")
            conn.commit()
        return render_template("delete.html")


@app.route("/", methods=['GET','POST'])
def userlogin():
    if request.method == "POST":
        getMName = request.form["mname"]
        getPassword = request.form["mpassword"]
        print(getMName)
        print(getPassword)
        return redirect("/userpage")
    return render_template("userlogin.html")



@app.route("/user", methods = ["GET","POST"])
def registerUser():

    if request.method == "POST":
        getMName = request.form["mname"]
        getAddress = request.form["address"]
        getEmailid = request.form["emailid"]
        getPhone = request.form["phone"]
        getPassword = request.form["mpassword"]

        print(getMName)
        print(getAddress)
        print(getEmailid)
        print(getPhone)
        print(getPassword)

        try:
            conn.execute("INSERT INTO users( mname, address, emailid, phone, mpassword)VALUES('"+getMName+"','"+getAddress+"','"+getEmailid+"','"+getPhone+"','"+getPassword+"')")
            print("Successfully inserted")
            conn.commit()
            return redirect("/userpage")

        except Exception as e:
            print(e)
    return render_template("user.html")


@app.route("/viewusers")
def viewusers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    return render_template("viewusers.html", user=res)


@app.route("/userpage")
def userpage():
    return render_template("userpage.html")

if(__name__) == "__main__":
    app.run(debug=True)