# Day 26 Practice App: Security Hardening Infrastructure
from flask import Flask, jsonify
from flask_talisman import Talisman

app = Flask(__name__)

csp = {
    'default-src': "'self'",
    'script-src': "'self'"
}

talisman = Talisman(app, content_security_policy=csp, force_https=False)

@app.route('/secure-endpoint')
def secure():
    return jsonify({"status": "Headers hardened with HSTS, CSP, and X-Frame-Options"})

if __name__ == '__main__':
    app.run(debug=True)
