import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "flaskblog.sqlite3")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["ADMIN_TOKEN"] = os.environ.get("ADMIN_TOKEN", "changeme")

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Post {self.id} {self.title!r}>"

@app.cli.command("init-db")
def init_db():
    """Initialise the database."""
    db.create_all()
    print("Database initialised at", DB_PATH)

def check_token():
    token = request.args.get("token") or request.form.get("token")
    if not token or token != app.config["ADMIN_TOKEN"]:
        abort(403)

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    posts = Post.query.order_by(Post.created_at.desc())
    if q:
        like = f"%{q}%"
        posts = posts.filter((Post.title.ilike(like)) | (Post.body.ilike(like)))
    return render_template("index.html", posts=posts.all(), q=q)

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route("/create", methods=["GET", "POST"])
def create_post():
    check_token()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            flash("Title and body are required.", "error")
            return render_template("post_form.html", mode="create", token=request.form.get("token"))
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("index"))
    return render_template("post_form.html", mode="create", token=request.args.get("token"))

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    check_token()
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            flash("Title and body are required.", "error")
            return render_template("post_form.html", mode="edit", post=post, token=request.form.get("token"))
        post.title = title
        post.body = body
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("post_detail", post_id=post.id))
    return render_template("post_form.html", mode="edit", post=post, token=request.args.get("token"))

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    check_token()
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "success")
    return redirect(url_for("index"))

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    # Create DB if it doesn't exist
    if not os.path.exists(DB_PATH):
        with app.app_context():
            db.create_all()
    app.run(debug=True)