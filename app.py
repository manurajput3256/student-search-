import os
import pandas as pd
from flask import Flask, request, render_template_string, redirect, session
from rapidfuzz import process

# ================= APP =================
app = Flask(__name__)
app.secret_key = "super_secret_key_2026"

# ================= LOGIN =================
USERNAME = "admin"
PASSWORD = "12345"

# ================= LOAD DATABASE =================
DATA_FILE = "students.xlsx"

df = pd.read_excel(DATA_FILE)

df["name_lower"] = df["Name"].astype(str).str.lower()
df["roll_str"] = df["Roll No"].astype(str)
df["mobile_str"] = df["Mobile"].astype(str)

# ================= LOGIN PAGE =================
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body{font-family:Arial;background:#f2f2f2;text-align:center}
.box{background:white;padding:30px;width:300px;margin:auto;margin-top:120px;border-radius:10px}
input{padding:8px;width:90%;margin:5px}
button{padding:10px;width:95%}
</style>
</head>

<body>

<div class="box">

<h2>Login</h2>

<form method="post">

<input type="text" name="username" placeholder="Username" required><br>

<input type="password" name="password" placeholder="Password" required><br>

<button type="submit">Login</button>

</form>

</div>

</body>
</html>
"""

# ================= MAIN PAGE =================
HTML_PAGE = """
<!DOCTYPE html>
<html>

<head>

<title>Student Information System</title>

<style>

body{font-family:Arial;background:#f2f2f2}

.container{
background:white;
width:80%;
margin:auto;
margin-top:40px;
padding:20px;
border-radius:10px
}

input{
padding:10px;
width:60%
}

button{
padding:10px
}

table{
border-collapse:collapse;
width:100%;
margin-top:20px
}

td,th{
border:1px solid black;
padding:8px
}

</style>

</head>

<body>

<div class="container">

<h2>Student Information System</h2>

<form method="post">

<input type="text" name="query" placeholder="Enter Name / Roll / Mobile" required>

<button type="submit">Search</button>

</form>

{% if student %}

<table>

<tr><th>Field</th><th>Value</th></tr>

{% for key,value in student.items() %}

<tr>

<td>{{key}}</td>

<td>{{value}}</td>

</tr>

{% endfor %}

</table>

{% endif %}

<br>

<a href="/logout">Logout</a>

</div>

</body>

</html>
"""

# ================= LOGIN ROUTE =================
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            session["user"] = username
            return redirect("/")

    return render_template_string(LOGIN_PAGE)

# ================= HOME =================
@app.route("/", methods=["GET","POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    student=None

    if request.method == "POST":

        query = request.form["query"].lower()

        # search name
        match = process.extractOne(query, df["name_lower"])

        if match:

            row = df[df["name_lower"] == match[0]].iloc[0]
            student = row.to_dict()

    return render_template_string(HTML_PAGE, student=student)

# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")

# ================= RUN SERVER =================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
