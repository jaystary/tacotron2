from flask import Flask
from flask import request, render_template
from flask import send_file

from inference import Inference


model = None
waveglow = None
inference = Inference()
model, waveglow = inference.load_model()



app = Flask(__name__, template_folder='static')


@app.route('/',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form['sentence']
        output = inference.infer(result, waveglow, model)
        templateData = {
            'sentence': output
        }
        return render_template('index.html', **templateData)

    return render_template('index.html')



'''@app.route('/', methods=['GET','POST'])
def start():

    req_data = request.get_json()
    input= req_data['sentence']
    print(req_data)

    output = inference.infer(input, waveglow, model)
    return "Hello World"
    return send_file(
        open(output, "rb"),
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="output.wav")
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug = True)