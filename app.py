
from flask import Flask, request, render_template
import os
import random
import matplotlib.pyplot as plt

app = Flask(__name__)
crash_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    result = None
    graph_url = None

    if request.method == "POST":
        if "simulate" in request.form:
            new_val = round(random.uniform(1.0, 10.0), 2)
            crash_history.append(new_val)

        elif "predict" in request.form:
            prediction = round(random.uniform(1.0, 5.0), 2)

        elif "strategy" in request.form:
            try:
                cashout = float(request.form.get("cashout"))
                wins = sum(1 for val in crash_history if val >= cashout)
                losses = sum(1 for val in crash_history if val < cashout)
                total = len(crash_history)
                if total > 0:
                    result = f"Cashout @ {cashout}x → Wins: {wins}, Losses: {losses}, Win Rate: {wins/total*100:.1f}%"
                else:
                    result = "No data yet."
            except:
                result = "Invalid input."

    # Generate graph
    if crash_history:
        plt.figure(figsize=(8, 4))
        plt.plot(crash_history[-50:], marker="o")
        plt.title("Crash History")
        plt.xlabel("Round")
        plt.ylabel("Multiplier (x)")
        plt.tight_layout()
        graph_path = os.path.join("static", "graph.png")
        plt.savefig(graph_path)
        plt.close()
        graph_url = "/" + graph_path

    return render_template(
        "index.html",
        prediction=prediction,
        result=result,
        graph_url=graph_url,
        history=crash_history[-10:]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # For Render
    app.run(host="0.0.0.0", port=port)
