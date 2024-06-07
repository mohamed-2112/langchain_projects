from flask import Flask, render_template, request, jsonify
from main.applications_with_langchain.ice_breaker.ice_breaker import IceBreaker
from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    ice_breaker_app = IceBreaker()
    summary, profile_pic_url = ice_breaker_app.ice_break_with(name=name)
    print("this is the finale result")
    print(summary)
    print("the pic is")
    print(profile_pic_url)
    summary_dict = summary.to_dict()
    print(summary_dict)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


class IceBreakerApp(Application):
    @override
    def run(self, **kwargs):
        app.run(host="0.0.0.0", debug=True)
