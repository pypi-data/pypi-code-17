import sys
import json
from itertools import cycle

from flask import Flask
from flask import request
from flask import jsonify

from placer import print_version
from placer.draw_python import python_logo, python_html

app = Flask(__name__)

goal_str = None


@app.route("/version", methods=["GET", "POST"])
def version():
    if request.method == "GET":
        return print_version()
    else:
        return jsonify({"version": print_version()})


@app.route("/goal", methods=["GET", "POST"])
def get_goal():
    if request.method == "GET":
        return python_html
    else:
        return jsonify({"goal": goal})


@app.route("/instruction", methods=["GET", "POST"])
def instruction():
    move = next(move_cycle)
    move["x"] = move["x"] + offset_x
    move["y"] = move["y"] + offset_y
    return jsonify({"draw": move})


if __name__ == "__main__":
    goal = python_logo
    offset_x = int(sys.argv[1])
    offset_y = int(sys.argv[2])
    if len(sys.argv) == 4:
        goal = json.loads(sys.argv[3])
    move_cycle = cycle(goal)
    app.run(host="0.0.0.0", port=45111)
