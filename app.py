from flask import Flask,render_template,jsonify,request
import sqlite3


app = Flask(__name__)
# id_store = 0

@app.route("/users",methods=["GET"])
def index():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM logins")
    data = cur.fetchall()
    conn.close()
    users_data = {}
    j = 0
    for i in data:
        dict = {}
        dict["username"] = i[0]
        dict["password"] = i[1]
        dict["id"] = i[2]
        users_data[j] = dict
        j += 1
    return jsonify(users_data)

@app.route("/signup/",methods=["GET","POST"])
def signup():
    res = {}
    username = str(request.args.get('msg'))
    password = str(request.args.get('pass'))
    
    try:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""INSERT INTO logins (username,password) VALUES (?,?)""",(username,password))
        conn.commit()
        conn.close()
        res = {"message":"sign up success"}
    except:
        res = {"message":"sign up failed"}

    return jsonify(res)


@app.route("/login/",methods=["POST","GET"])
def login():
    res = {}
    username = str(request.args.get('msg'))
    password = str(request.args.get('pass'))

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
            SELECT * FROM logins WHERE username=?
        ''',(username,))
    data = cur.fetchall()
    conn.close()
    if (not(len(data) == 0)):
        res = {'result':' success user found'}
    else:
        res = {'result':'error, user not found'}
    
    return jsonify(res)

