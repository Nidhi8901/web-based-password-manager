from flask import Flask, request, redirect, render_template_string, session
from app import (
    init_db, register_user, login_user, add_password,
    list_passwords, update_password, view_password,
    generate_password, view_password_as_superadmin
)

app = Flask(__name__)
app.secret_key = "supersecretkey"
init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Manager</title>
</head>
<body>
    <h2>🔐 Password Manager</h2>

    {% if not session.get('user_id') %}
        <h3>Register</h3>
        <form method="POST" action="/register">
            Username: <input name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Register</button>
        </form>

        <h3>Login</h3>
        <form method="POST" action="/login">
            Username: <input name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
    {% else %}
        <p>✅ Logged in as {{ session['role'] }}</p>

        <h3>Add Password</h3>
        <form method="POST" action="/add">
            Service: <input name="service" required><br>
            Account: <input name="account" required><br>
            Password: <input name="password" id="pwd" required>
            <button type="button" onclick="generate()">Generate</button><br>
            Expiry (YYYY-MM-DD): <input name="expiry" required><br>
            <button type="submit">Save</button>
        </form>

        <h3>Your Passwords</h3>
        <ul>
            {% for p in passwords %}
                <li>
                    {{ p[1] }} ({{ p[2] }}) — Expires: {{ p[3] }}
                    <form style="display:inline" method="POST" action="/update/{{ p[0] }}">
                        New Password: <input name="new_password" required>
                        New Expiry: <input name="new_expiry" required>
                        <button type="submit">Update</button>
                    </form>
                    {% if session['role'] == 'superadmin' %}
                        <a href="/view/{{ p[0] }}">[View Password]</a>
                    {% endif %}
                </li>
            {% endfor %}
        </ul>

        <form method="GET" action="/logout">
            <button type="submit">Logout</button>
        </form>
    {% endif %}

<script>
function generate() {
    fetch('/generate')
      .then(res => res.text())
      .then(pwd => document.getElementById('pwd').value = pwd);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    if "user_id" in session:
        passwords = list_passwords(session["user_id"])
        return render_template_string(HTML_TEMPLATE, passwords=passwords)
    return render_template_string(HTML_TEMPLATE)

@app.route("/register", methods=["POST"])
def register():
    try:
        register_user(request.form["username"], request.form["password"])
        return redirect("/")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/login", methods=["POST"])
def login():
    try:
        user_id, role = login_user(request.form["username"], request.form["password"])
        session["user_id"] = user_id
        session["role"] = role
        return redirect("/")
    except Exception as e:
        return f"Login failed: {str(e)}"

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/")
    try:
        add_password(
            session["user_id"],
            request.form["service"],
            request.form["account"],
            request.form["password"],
            request.form["expiry"]
        )
        return redirect("/")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/update/<int:pid>", methods=["POST"])
def update(pid):
    if "user_id" not in session:
        return redirect("/")
    try:
        update_password(
            session["user_id"],
            pid,
            request.form["new_password"],
            request.form["new_expiry"]
        )
        return redirect("/")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/view/<int:pid>")
def view(pid):
    if session.get("role") != "superadmin":
        return "Unauthorized"
    try:
        password = view_password(session["user_id"], pid)
        return f"🔓 Password: {password}"
    except Exception:
        return "Password not found"

@app.route("/generate")
def generate():
    return generate_password()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
