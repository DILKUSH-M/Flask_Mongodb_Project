
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Connect to MongoDB Atlas or local MongoDB
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=10000
)

# Verify the database connection
client.admin.command("ping")
print("MongoDB connected successfully!")

# Select database and collection
db = client["beginner_db"]
todos_collection = db["todos"]


@app.route("/")
def index():
    todos = list(todos_collection.find())
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task", "").strip()

    if task:
        todos_collection.insert_one({"task": task})

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
