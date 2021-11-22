from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task=Task(title=title,desc=desc)
        db.session.add(task)
        db.session.commit()
    # tasks = Task(title="First Task", desc="Start MFs")
    # db.session.add(tasks)
    # db.session.commit()
    alltasks = Task.query.all()
    #print(alltasks)
    return render_template('index.html',alltasks=alltasks)


@app.route("/Update/<int:sno>", methods=['GET','POST'])
def update(sno):
    task=Task.query.filter_by(sno=sno).first()
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task=Task.query.filter_by(sno=sno).first()        
        task.title=title
        task.desc=desc
        db.session.add(task)
        db.session.commit() 
        return redirect("/")
        #task=Task(title=title,desc=desc)
        #db.session.add(task)
        #db.session.commit()
    return render_template('update.html', task=task)

@app.route("/Delete/<int:sno>")
def delete(sno):
    task=Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")
    
    #return render_template('update.html',sno=sno)


if __name__ == "__main__":
    app.run(debug=True, port=5000)