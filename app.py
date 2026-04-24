from flask import Flask, request, render_template_string
import pickle
import os

app = Flask(__name__)

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load model and vectorizer
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
        h2{
            margin-top:20px;
        }
    </style>
</head>
<body>

<div class="box">
    <h1>Cyberbullying Detection System</h1>

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
        try:
            text = request.form["text"]

            transformed = vectorizer.transform([text])
            result = model.predict(transformed)[0]

            result_str = str(result).lower()

            if result == 1 or result_str in ["1", "yes", "true", "bullying", "cyberbullying"]:
                prediction = "⚠️ Cyberbullying Detected"
            else:
                prediction = "✅ No Cyberbullying"

        except Exception as e:
            prediction = "Error: " + str(e)

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == "__main__":
    app.run()