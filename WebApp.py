from flask import Flask, render_template, request, jsonify
import setproctitle
import config


__author__ = 'joe'
setproctitle.setproctitle("neatlightsflask")
app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    if request.method == "GET":
        return render_template("index.html")


@app.route('/schedule', methods=["GET", "POST"])
def schedule():
    response = {}
    return jsonify(response)


@app.route('/activate', methods=["GET", "POST"])
def send():
    response = {"status": "None"}
    #  thash = request.args.get('hash')
    #  /send?count=630&brightness=50&senselight=0&style=Room%20Lighting&color=orange&method_name=room_lighting

    # try:
    #     message = {
    #         'led_count': int(request.args.get('count')),  # 630,
    #         'brightness': int(request.args.get('brightness')),  # 10,
    #         'senselight': int(request.args.get('senselight')),  # 0,
    #         'style_name': request.args.get('style'),  # 'Room Lighting',
    #         'color': [request.args.get('color').lower()],  # ['blue'],
    #         'method_name': request.args.get('method')  # 'room_lighting'
    #     }
    # except Exception as e:
    #     response['status'] = "error"
    #     response[
    #         'info'] = "Something went wrong when parsing message.  Please check query params."
    #     response['error'] = str(e)
    #     return jsonify(response)

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=config.PORT, threaded=True)
