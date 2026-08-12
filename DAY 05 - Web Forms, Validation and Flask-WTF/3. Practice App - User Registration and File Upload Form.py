"""
===============================================================================
Day 05 Practice Script: Web Forms, Validation & File Upload System
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Raw HTML form submission (`request.form.get()`) to demonstrate why manual forms lack CSRF security.
2. STEP 2: Basic Flask-WTF form (`LoginForm`) demonstrating automatic CSRF protection.
3. STEP 3: Full Registration form with built-in validators (`DataRequired`, `Email`, `Length`, `EqualTo`).
4. STEP 4: Custom validators (In-line `validate_username` & standalone `ComplexPassword`).
5. STEP 5: Secure file uploads (`FileField`, `FileAllowed`, `secure_filename`, `MAX_CONTENT_LENGTH`).
6. STEP 6: Rendering categorized flash messages.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - User Registration and File Upload Form.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Secret key required by Flask-WTF for CSRF token generation
app.config['SECRET_KEY'] = 'day05-csrf-protection-secret-key-30-days'

# Enforce Maximum 5 Megabytes File Upload Limit
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Define folder path for uploaded avatar images
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# =============================================================================
# STEP 4: Custom Standalone Reusable Password Validator Factory
# =============================================================================

def ComplexPassword(min_length=8):
    """Factory function returning a custom validator enforcing password strength."""
    def _validator(form, field):
        password = field.data or ''
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters long.")
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter (A-Z).")
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one numeric digit (0-9).")
    return _validator


# =============================================================================
# STEP 2 & 3: Flask-WTF Form Definitions
# =============================================================================

class SimpleLoginForm(FlaskForm):
    """Step 2: Basic Flask-WTF Form with automatic CSRF protection."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationUploadForm(FlaskForm):
    """Step 3 & 4 & 5: Full Registration and Avatar Upload Form."""
    
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters.")
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(message="Email address is required."),
        Email(message="Invalid email address format.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        ComplexPassword(min_length=8)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords do not match!")
    ])
    
    avatar = FileField('Profile Avatar Image', validators=[
        FileRequired(message="Profile avatar image is required."),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="Images only (.jpg, .png, .gif)!")
    ])
    
    submit = SubmitField('Complete Registration')

    # Step 4: In-line Custom Validator for Username
    def validate_username(self, field):
        """Executed automatically when validating the username field."""
        forbidden = ['admin', 'root', 'superuser', 'administrator', 'system']
        if field.data and field.data.strip().lower() in forbidden:
            raise ValidationError(f"The username '{field.data}' is reserved by system administrators.")


# =============================================================================
# STEP 1: Raw HTML Form Route Handler (Manual Parsing)
# =============================================================================

@app.route('/raw-login', methods=['GET', 'POST'])
def raw_login():
    """
    Step 1: Demonstrating Raw HTML form handling via request.form.get()
    Notice how manual validation requires multiple if/else statements and lacks CSRF tokens!
    """
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        
        # Manual Validation Logic
        if not uname or not pwd:
            flash("Manual Validation Error: Both username and password are required!", "danger")
        elif uname == 'admin':
            flash("Logged in successfully via Raw HTML Form!", "success")
            return redirect(url_for('raw_login'))
        else:
            flash(f"User '{uname}' submitted raw form.", "warning")
            
    return render_template('raw_login.html')


# =============================================================================
# STEP 3 & 5: Flask-WTF Registration & File Upload Handler
# =============================================================================

@app.route('/', methods=['GET', 'POST'])
def register():
    """
    Form view handler processing registration and secure file uploads using Flask-WTF.
    """
    form = RegistrationUploadForm()
    
    # Executes ONLY when request is POST and form data + CSRF token are valid
    if form.validate_on_submit():
        file_obj = form.avatar.data
        
        # Step 5: Sanitize filename to prevent Directory Traversal attacks (../etc/passwd)
        filename = secure_filename(file_obj.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_obj.save(save_path)
        
        flash(f"Account for '{form.username.data}' created successfully! Avatar saved as '{filename}'.", "success")
        return redirect(url_for('register'))
    elif request.method == 'POST':
        flash("Form validation failed. Please correct the highlighted errors below.", "danger")
        
    return render_template('register.html', form=form)


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 05 Forms & File Upload Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
