from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
  return render_template('about.html', name="About")


@app.route("/contact")
def contact():
  return render_template('contact.html', name="Contact")

@app.route("/login")
def login():
  return render_template('login.html', name="Register")

if __name__ == "__main__":
    app.run(debug=True)
