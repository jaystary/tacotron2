from flask import Flask
from flask import request, render_template
from flask import send_file
import helper
import concurrent.futures

from inference import Inference


model = None
waveglow = None
inference = Inference()



app = Flask(__name__, template_folder='static')


@app.route('/',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        val = request.form['sentence']
        sentence_list = helper.split_sentences(val)
        result_list = []

        with concurrent.futures.ProcessPoolExecutor() as pool:
            for s in sentence_list:
                future_result = pool.submit(inference.infer, s)
                future_result.add_done_callback(result_list)

        print(result)
        output = inference.infer(result)
        templateData = {
            'sentence': output
        }
        return render_template('index.html', **templateData)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug = True)
