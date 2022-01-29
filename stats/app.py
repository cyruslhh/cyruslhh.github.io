import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
import math
from random import shuffle
from random import seed
from random import random
import datetime


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'secret!'
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQL("sqlite:///stats_database.db")
seed(datetime.datetime.now())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats/start", methods=["POST"])
def start():
    if request.method == "POST":
        name = request.form.get("inputName")
        email = request.form.get("inputEmail")
        code = request.form.get("inputCode")

        if not name:
            return render_template("error.html", message="Please input a username!")
        if not email:
            return render_template("error.html", message="Please input a email")

        rows = db.execute("SELECT name FROM users WHERE email=?", email)
        if len(rows) > 0:
            return render_template("error.html", message="That email has already been used!")

        referral_index = -1
        if code:
            rows = db.execute(
                "SELECT id FROM users WHERE referral_code=?", code)
            if len(rows) == 0:
                return render_template("error.html", message="That referral code doesn't exist!")
            else:
                referral_index = rows[0]["id"]

        session["name"] = name
        session["email"] = email
        session["referral_index"] = referral_index

        return redirect("/stats/words")


@app.route("/stats/words", methods=["POST", "GET"])
def words():
    if request.method == "GET":
        words_rows = db.execute("SELECT * from words")
        remaining_indexes = list(range(1, len(words_rows)))
        print(remaining_indexes)
        selected_indexes = []
        for i in range(40):
            index = math.floor(random() * len(remaining_indexes))
            selected_indexes.append(remaining_indexes.pop(index))
        session["selected_word_indexes"] = selected_indexes
        session["remaining_word_indexes"] = remaining_indexes
        selected_words = []
        for i in selected_indexes:
            rows = db.execute("SELECT word from words WHERE id=?", int(i))
            if len(rows) > 1:
                print("error, more than one row detected, using first row...", rows, i)
            selected_words.append((rows[0]["word"]))
        session["selected_words"] = selected_words
        return render_template("words.html", words=selected_words, used=False)
    if request.method == "POST":
        new_selected_words = []
        no_remaining_words = False
        for i in range(len(session["selected_words"])):
            print("word", session["selected_words"][i],
                  request.form.get(session["selected_words"][i]))
            if (request.form.get(session["selected_words"][i])):
                if(len(session["remaining_word_indexes"]) < 1):
                    no_remaining_words = True
                    break
                new_word_index = math.floor(
                    random() * len(session["remaining_word_indexes"]))
                session["selected_word_indexes"].pop(i)
                session["selected_word_indexes"].insert(
                    i, session["remaining_word_indexes"].pop(new_word_index))
        for i in session["selected_word_indexes"]:
            rows = db.execute("SELECT word from words WHERE id=?", int(i))
            if len(rows) > 1:
                print("error, more than one row detected, using first row...", rows, i)
            new_selected_words.append((rows[0]["word"]))
        session["selected_words"] = new_selected_words
        return render_template("words.html", words=new_selected_words, used=no_remaining_words)


@ app.route("/stats/experiment")
def experiment():
    session["first_treatment_words"] = []
    first_treatment = random() >= 0.5
    for i in range(math.floor(len(session["selected_words"])/2)):
        index = math.floor(random() * len(session["selected_words"]))
        session["first_treatment_words"].append(
            session["selected_words"].pop(index))
    session["second_treatment_words"] = session["selected_words"]
    first_treatment_pairs = []
    for word in session["first_treatment_words"]:
        rows = db.execute(
            "SELECT definition from words WHERE word=?", str(word))
        first_treatment_pairs.append({"word": word.capitalize(),
                                      "def": rows[0]["definition"]})
    shuffle(first_treatment_pairs)
    shuffle(session["first_treatment_words"])
    session["second_done"] = False
    if (first_treatment):
        session["treatment_1"] = "visual"
        session["treatment_2"] = "audio"
        return render_template("visual.html", word_pairs=first_treatment_pairs,
                               link="/stats/testing")
    else:
        session["treatment_1"] = "audio"
        session["treatment_2"] = "visual"
        return render_template("audio.html", word_pairs=first_treatment_pairs,
                               link="/stats/testing")


@ app.route("/stats/testing")
def testing():
    if (session["second_done"]):
        shuffle(session["second_treatment_words"])
        return render_template("testing.html", words=session["second_treatment_words"], link="/stats/finish")
    else:
        shuffle(session["first_treatment_words"])
        return render_template("testing.html", words=session["first_treatment_words"], link="/stats/experiment2")


@ app.route("/stats/finish", methods=["POST", "GET"])
def finish():
    if request.method == "POST":
        # check if they reloaded the page
        rows = db.execute(
            "SELECT * FROM users WHERE email=?", session["email"])
        if (len(rows) > 0):
            return render_template("error.html", message="account already exists! Did someone make an account while you're doing the experiment or did you refresh the page???")
        second_answers_list = []
        for word in session["second_treatment_words"]:
            second_answers_list.append(
                {"word": word, "ans": request.form.get(word)})
        code = make_code()
        tickets = 1
        if (session["referral_index"] > -1):
            tickets = 2
            db.execute("UPDATE users SET tickets=(tickets + 1) WHERE id=?",
                       session["referral_index"])
        db.execute("INSERT INTO users (name, email, referral_code, referral_index, tickets) VALUES (?, ?, ?, ?, ?)",
                   session["name"], session["email"], code, session["referral_index"], tickets)
        rows = db.execute("SELECT id FROM users WHERE name=?", session["name"])
        id = rows[0]["id"]
        for item in session["first_answers"]:
            if(not item["ans"]):
                continue
            rows = db.execute(
                "SELECT definition FROM words WHERE word=?", item["word"])
            definition = rows[0]["definition"]
            db.execute("INSERT INTO responses (user_id, learning_mode, word, actual_definition, user_definition) VALUES (?, ?, ?, ?, ?)",
                       id, session["treatment_1"], item["word"], definition, item["ans"])
        for item in second_answers_list:
            if(not item["ans"]):
                continue
            rows = db.execute(
                "SELECT definition FROM words WHERE word=?", item["word"])
            definition = rows[0]["definition"]
            db.execute("INSERT INTO responses (user_id, learning_mode, word, actual_definition, user_definition) VALUES (?, ?, ?, ?, ?)",
                       id, session["treatment_2"], item["word"], definition, item["ans"])
        return render_template("finish.html", refer=code)
    if request.method == "GET":
        return render_template("error.html", message="bruh did you really just try to skip the entire experiment or something.")


def make_code():
    code = 0
    while(True):
        code = math.floor(random() * 100000000)
        rows = db.execute("SELECT * FROM users WHERE referral_code=?", code)
        if len(rows) == 0:
            break
    return code


@ app.route("/stats/experiment2", methods=["POST", "GET"])
def experiment2():
    if request.method == "POST":
        first_answers_list = []
        for word in session["first_treatment_words"]:
            first_answers_list.append(
                {"word": word, "ans": request.form.get(word)})
        session["first_answers"] = first_answers_list

    second_treatment_pairs = []
    for word in session["second_treatment_words"]:
        rows = db.execute("SELECT definition from words WHERE word=?", word)
        second_treatment_pairs.append({"word": word.capitalize(),
                                       "def": rows[0]["definition"]})
    shuffle(second_treatment_pairs)
    shuffle(session["first_treatment_words"])
    session["second_done"] = True

    if (session["treatment_1"] == "audio"):
        session["treatment_1"] = "visual"
        return render_template("visual.html", word_pairs=second_treatment_pairs,
                               link="/stats/testing")
    else:
        session["treatment_1"] = "audio"
        return render_template("audio.html", word_pairs=second_treatment_pairs,
                               link="/stats/testing")


if __name__ == "__main__":
    app.run(debug=True)
