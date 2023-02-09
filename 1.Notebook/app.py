from flask import flash, redirect, url_for, render_template


import click


from flask import render_template



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length,ValidationError

from datetime import datetime
from flask import flash, redirect, url_for, render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "sss"
# app.config.from_pyfile('settings.py')
# app.= True
app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True
app.config["jinja_env.trim_blocks"] = True
app.config["jinja_env.lstrip_blocks"] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/notebook"
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def is_pw(msg=None):
    if msg is None:
        msg = "ちゃんと考えてみてくださいね"
    def _is_pw(form,field):
        if field.data !="":
            raise ValidationError(msg)
    return _is_pw


class HelloForm(FlaskForm):
    name = StringField('タッグ', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('メッセージ', validators=[DataRequired(), Length(1, 200)])
    pw = IntegerField("暗号は覚えるよね？",validators=[is_pw()])
    submit = SubmitField()



# model
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # def __repr__(self):
    #     return '<Tag %r>' % self.tag






# error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


# views
@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('最高です！')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages)



if __name__ == "__main__":

    app.run(debug=True)
