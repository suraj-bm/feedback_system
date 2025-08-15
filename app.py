from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///feedback.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class feedback(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
with app.app_context():
    db.create_all()

@app.route("/")
def Index():
    return render_template('index.html')
@app.route("/save_feedback",methods=["POST"])
def save_feedback():
    data = request.get_json()
    feedback_content = data.get("feedback")

    if not feedback_content:
        return jsonify({"status": "error", "message": "No feedback provided"}), 400

    new_feedback = feedback(content=feedback_content)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({"status": "success", "message": "Feedback saved"})



if __name__=="__main__":
    app.run(debug=True)