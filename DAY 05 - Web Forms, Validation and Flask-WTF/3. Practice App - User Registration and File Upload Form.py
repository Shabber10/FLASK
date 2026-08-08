# Day 05 Practice App: WTForms & Secure File Upload
import os
from flask import Flask, render_template_string, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-30-days'
app.config['UPLOAD_FOLDER'] = './uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    avatar = FileField('Upload Avatar', validators=[DataRequired()])
    submit = SubmitField('Submit Profile')

FORM_TEMPLATE = '''
<!DOCTYPE html>
<html>
<body>
    <h2>User Profile Registration</h2>
    {% with msgs = get_flashed_messages() %}
        {% for m in msgs %}<p style="color:green;">{{ m }}</p>{% endfor %}
    {% endwith %}
    <form method="POST" enctype="multipart/form-data">
        {{ form.csrf_token }}
        <p>{{ form.full_name.label }}: {{ form.full_name() }}</p>
        <p>{{ form.avatar.label }}: {{ form.avatar() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
</body>
</html>
'''

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        filename = secure_filename(form.avatar.data.filename)
        form.avatar.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"Profile saved! File uploaded as: {filename}")
        return redirect(url_for('profile'))
    return render_template_string(FORM_TEMPLATE, form=form)

if __name__ == '__main__':
    app.run(debug=True)
