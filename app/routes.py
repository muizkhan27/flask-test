from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, login_manager

from .models.models import ToDO, User, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def index():
    """Render the home page with a list of todos."""
    todos = ToDO.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
@login_required
def add_todo():
    """Add a new todo to the database."""
    content = request.form.get("content")
    due_date = request.form.get("due_date")
    if content:
        new_todo = ToDO(content=content,
                        user_id=current_user.id, due_date=due_date)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo added!", "success")
    else:
        flash("Todo cannot be empty.", "danger")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_todo(id):
    """Delete a todo from the database."""
    todo = ToDO.query.get_or_404(id)
    if todo.user != current_user:
        return redirect(url_for("index"))
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted!", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login, with optional error message for login failure."""
    login_failed = False  # Initialize a variable to indicate login failure
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            login_failed = True  # Set the variable to True if login fails
    return render_template(
        "login.html", login_failed=login_failed
    )  # Pass the variable to the template


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user registration, with error handling for invalid inputs."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Both username and password are required.", "danger")
        elif User.query.filter_by(username=username).first():
            flash("Username already exists. Choose another.", "danger")
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method="sha256")
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_todo(id):
    """Edit an existing todo in the database."""
    todo = ToDO.query.get_or_404(id)
    if todo.user != current_user:
        return redirect(url_for("index"))

    if request.method == "POST":
        new_content = request.form.get("content")
        new_due_date = request.form.get("due_date")

        if new_content:
            todo.content = new_content
            todo.due_date = new_due_date if new_due_date else None
            db.session.commit()
            flash("Todo updated!", "success")
        else:
            flash("Todo content cannot be empty.", "danger")
        return redirect(url_for("index"))

    return render_template("edit.html", todo=todo)


# Route to mark a todo as completed
@app.route("/mark_complete/<int:id>", methods=["POST"])
@login_required
def mark_complete(id):
    """Mark a todo as completed."""
    todo = ToDO.query.get_or_404(id)
    if todo.user != current_user:
        return redirect(url_for("index"))
    todo.completed = True
    db.session.commit()
    flash("todo marked as completed!", "success")
    return redirect(url_for("index"))


# Route to sort todos by due date
@app.route("/sort_by_due_date", methods=["GET"])
@login_required
def sort_by_due_date():
    """Sort todos by due date, ascending or descending."""
    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        todos = (
            ToDO.query.filter_by(user_id=current_user.id).order_by(
                ToDO.due_date).all()
        )
    else:
        todos = (
            ToDO.query.filter_by(user_id=current_user.id)
            .order_by(ToDO.due_date.desc())
            .all()
        )
    return render_template("index.html", todos=todos)
