"""
Day 05 Practice Application: Registration & Secure File Upload System
======================================================================
This application demonstrates:
1. Defining WTForms with built-in and custom validators.
2. In-line field validation for reserved username enforcement.
3. Reusable validator functions for strong password policies.
4. Enforcing file upload security (extensions, file size limits, secure_filename).
5. CSRF protection and categorized flash message rendering.
"""

import os
from flask import Flask, render_template_string, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day05-csrf-protection-secret-key-30-days'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB Max Upload
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ------------------------------------------------------------------------------
# 1. Custom Standalone Password Policy Validator
# ------------------------------------------------------------------------------
def ComplexPassword(min_length=8):
    def _validator(form, field):
        password = field.data or ''
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters long.")
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter (A-Z).")
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one digit (0-9).")
    return _validator


# ------------------------------------------------------------------------------
# 2. Registration & Upload Form Definition
# ------------------------------------------------------------------------------
class RegistrationUploadForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=20)
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(message="Invalid email address format.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        ComplexPassword(min_length=8)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords do not match!")
    ])
    
    avatar = FileField('Profile Avatar Image', validators=[
        FileRequired(message="Profile avatar image is required."),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="Images only (.jpg, .png, .gif)!")
    ])
    
    submit = SubmitField('Complete Registration')

    # In-line Custom Validator for Username
    def validate_username(self, field):
        forbidden = ['admin', 'root', 'superuser', 'administrator', 'system']
        if field.data.strip().lower() in forbidden:
            raise ValidationError(f"The username '{field.data}' is reserved by system administrators.")


# ------------------------------------------------------------------------------
# 3. HTML Template String
# ------------------------------------------------------------------------------
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 05 Form & File Upload Masterclass</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eef2f5; margin: 0; padding: 40px; }
        .card { max-width: 550px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; margin-top: 0; }
        .form-group { margin-bottom: 18px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; color: #34495e; }
        input[type="text"], input[type="password"], input[type="file"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 5px; }
        .error-msg { color: #e74c3c; font-size: 0.85em; margin-top: 4px; }
        .btn { background: #3498db; color: white; padding: 12px 20px; border: none; border-radius: 5px; font-size: 1em; cursor: pointer; width: 100%; }
        .btn:hover { background: #2980b9; }
        .alert { padding: 12px; margin-bottom: 20px; border-radius: 5px; color: white; font-weight: bold; }
        .alert-success { background: #2ecc71; }
        .alert-danger { background: #e74c3c; }
        .alert-warning { background: #f39c12; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 User Registration & Avatar Upload</h2>

        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" enctype="multipart/form-data">
            <!-- CSRF Protection Token -->
            {{ form.csrf_token }}

            <div class="form-group">
                {{ form.username.label }}
                {{ form.username() }}
                {% for err in form.username.errors %}<div class="error-msg">{{ err }}</div>{% endfor %}
            </div>

            <div class="form-group">
                {{ form.email.label }}
                {{ form.email() }}
                {% for err in form.email.errors %}<div class="error-msg">{{ err }}</div>{% endfor %}
            </div>

            <div class="form-group">
                {{ form.password.label }}
                {{ form.password() }}
                {% for err in form.password.errors %}<div class="error-msg">{{ err }}</div>{% endfor %}
            </div>

            <div class="form-group">
                {{ form.confirm_password.label }}
                {{ form.confirm_password() }}
                {% for err in form.confirm_password.errors %}<div class="error-msg">{{ err }}</div>{% endfor %}
            </div>

            <div class="form-group">
                {{ form.avatar.label }}
                {{ form.avatar() }}
                {% for err in form.avatar.errors %}<div class="error-msg">{{ err }}</div>{% endfor %}
            </div>

            {{ form.submit(class="btn") }}
        </form>
    </div>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationUploadForm()
    
    if form.validate_on_submit():
        # Sanitize Filename to prevent Directory Traversal
        file_obj = form.avatar.data
        filename = secure_filename(file_obj.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_obj.save(save_path)
        
        flash(f"Account for '{form.username.data}' registered! Avatar saved as '{filename}'.", "success")
        return redirect(url_for('register'))
    elif request.method == 'POST':
        flash("Form validation failed. Please correct highlighted errors below.", "danger")
        
    return render_template_string(TEMPLATE_HTML, form=form)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 05 Forms & File Upload Application...")
    print("Test endpoint at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
