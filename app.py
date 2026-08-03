from flask import Flask, render_template

app = Flask(__name__)

# Sample habit data
habits = [
    {"id": 1, "name": "Drink Water", "status": "Pending"},
    {"id": 2, "name": "Exercise", "status": "Pending"},
    {"id": 3, "name": "Read 20 Minutes", "status": "Pending"},
    {"id": 4, "name": "Sleep Before 11 PM", "status": "Pending"}
]

# Adaptive coaching tips
tips = {

    "Drink Water": {
        "Busy": "Keep a water bottle on your desk.",
        "Forgot": "Set a reminder every 2 hours.",
        "Low Energy": "Drink one glass of water now.",
        "No Motivation": "Start with one sip.",
        "Other": "Staying hydrated improves your energy."
    },

    "Exercise": {
        "Busy": "Try a quick 10-minute workout.",
        "Forgot": "Keep your shoes near the door.",
        "Low Energy": "Take a 10-minute walk instead of a full workout.",
        "No Motivation": "Start with just 2 minutes.",
        "Other": "Small progress is still progress."
    },

    "Read 20 Minutes": {
        "Busy": "Read for 10 minutes before bed.",
        "Forgot": "Keep your book near your pillow.",
        "Low Energy": "Read just one page today.",
        "No Motivation": "Start reading for 5 minutes.",
        "Other": "Every page counts."
    },

    "Sleep Before 11 PM": {
        "Busy": "Try sleeping 30 minutes earlier.",
        "Forgot": "Set a bedtime reminder.",
        "Low Energy": "Reduce screen time before bed.",
        "No Motivation": "Prepare your bed early.",
        "Other": "Good sleep creates better habits."
    }

}


# Landing Page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    completed = 0

    for habit in habits:

        if habit["status"] == "Completed":

            completed += 1

    total = len(habits)

    return render_template(
        "dashboard.html",
        habits=habits,
        completed=completed,
        total=total
    )


# Complete Habit
@app.route("/complete/<int:habit_id>")
def complete(habit_id):

    for habit in habits:
        if habit["id"] == habit_id:
            habit["status"] = "Completed"

    return render_template("dashboard.html", habits=habits)


# Skip Habit
@app.route("/skip/<int:habit_id>")
def skip(habit_id):

    selected_habit = None

    for habit in habits:
        if habit["id"] == habit_id:
            selected_habit = habit

    return render_template("skip_reason.html", habit=selected_habit)


# Suggestion Page
@app.route("/suggestion/<int:habit_id>/<reason>")
def suggestion(habit_id, reason):

    habit_name = ""

    for habit in habits:
        if habit["id"] == habit_id:
            habit_name = habit["name"]

    suggestion = tips[habit_name][reason]

    return render_template(
        "suggestion.html",
        habit=habit_name,
        reason=reason,
        suggestion=suggestion
    )

@app.route("/motivation")
def motivation():

    completed = 0

    for habit in habits:
        if habit["status"] == "Completed":
            completed += 1

    total = len(habits)

    if completed == total:
        message = "🏆 Amazing! You completed all your habits today."
    elif completed >= total / 2:
        message = "🌱 Great job! You're making steady progress."
    else:
        message = "💪 Don't worry. Every small step counts. Keep going!"

    return render_template(
        "motivation.html",
        completed=completed,
        total=total,
        message=message
    )

# Run Application
if __name__ == "__main__":
    app.run(debug=True)