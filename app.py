from flask import Flask, render_template, request, jsonify
from routes import routes

app = Flask(__name__)
app.debug = True

app.register_blueprint(routes)


if __name__ == '__main__':
    app.run()