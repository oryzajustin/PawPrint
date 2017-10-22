from flask import Flask, send_from_directory, request

app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static/img', path)


@app.route('/test', methods=['POST'])
def test():
    print request.form
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)