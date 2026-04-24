from flask import Flask, request, render_template_string
import pickle
import os

app = Flask(__name__)

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct file paths
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load files
model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Cyberbullying Detection</title>
<style>
body{
font-family:Arial;
background:#0f172a;
color:white;
text-align:center;
padding:50px;
}
.box{
background:#1e293b;
padding:30px;
border-radius:15px;
width:60%;
margin:auto;
}
textarea{
width:90%;
height:120px;
padding:10px;
border-radius:10px;
border:none;
margin-top:20px;
}
button{
margin-top:20px;
padding:12px 25px;
background:#38bdf8;
border:none;
font-weight:bold;
border-radius:10px;
cursor:pointer;
}
</style>
</head>
<body>
<div class="box">
<h1>Cyberbullying Detection</h1>

<form method="POST">
<textarea name="text" placeholder="Enter text here..."></textarea><br>
<button type="submit">Predict</button>
</form>

{% if prediction %}
<h2>{{ prediction }}</h2>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""

    if request.method == "POST":
        text = request.form["text"]

        transformed = vectorizer.transform([text])
        result = model.predict(transformed)[0]

        if result == 1:
            prediction = "⚠️ Cyberbullying Detected"
        else:
            prediction = "✅ No Cyberbullying"

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == "__main__":
    app.run()