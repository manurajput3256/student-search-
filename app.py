import pandas as pd
from flask import Flask, request, render_template_string
from rapidfuzz import process

# load excel file
EXCEL_PATH = "students.xlsx"
df = pd.read_excel(EXCEL_PATH)

df["name_lower"] = df["Name"].astype(str).str.lower()
df["roll_str"] = df["Roll No"].astype(str)
df["mobile_str"] = df["Mobile"].astype(str)

app = Flask(__name__)

HTML_PAGE = """
<html>
<head>
<title>Student Information System</title>

<script>
function speakText(text){
var speech = new SpeechSynthesisUtterance(text);
window.speechSynthesis.speak(speech);
}

function stopSpeech(){
window.speechSynthesis.cancel();
}
</script>

</head>

<body>

<h2>Student Information System</h2>

<form method="post">
<input type="text" name="query" placeholder="Enter Name / Roll / Mobile">
<button type="submit">Search</button>
</form>

{% if student %}

<table border="1">
{% for key,value in student.items() %}
<tr>
<td>{{key}}</td>
<td>{{value}}</td>
</tr>
{% endfor %}
</table>

<button onclick="speakText(`{{speech_text}}`)">Speak</button>
<button onclick="stopSpeech()">Stop</button>

{% endif %}

</body>
</html>
"""

@app.route("/",methods=["GET","POST"])
def home():

    student=None
    speech_text=""

    if request.method=="POST":

        query=request.form["query"].lower()

        roll_match=df[df["roll_str"]==query]
        mobile_match=df[df["mobile_str"]==query]

        if not roll_match.empty:
            row=roll_match.iloc[0]

        elif not mobile_match.empty:
            row=mobile_match.iloc[0]

        else:
            match=process.extractOne(query,df["name_lower"])
            row=df[df["name_lower"]==match[0]].iloc[0]

        student=row.to_dict()

        speech_text=f"{row['Name']} is a student of {row['Branch']} branch."

    return render_template_string(HTML_PAGE,student=student,speech_text=speech_text)

if __name__=="__main__":
    app.run()