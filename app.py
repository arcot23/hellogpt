from flask import Flask, render_template, request, Response
from scripts.wrapper import gptwrapper as gw
import scripts.logreader as lr
from markdown2 import markdown
import base64
import json
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listlogs')
def listlogs():
    return render_template('listlogs.html')


@app.route('/', methods=['POST'])
def process():
    prompt_text = request.form["input_text"]
    model = request.form["model"]
    system_prompt = "Start the response with a title."
    g = gw(system_prompt=system_prompt)
    if model == 'dall-e-3':
        g.request_image(prompt_text)
    elif model == 'tts-1':
        g.request_audio(prompt_text)
    elif model == 'gpt-4':
        g.request_text(prompt_text)

    g.dump(request.remote_addr)

    if g.model == "gpt-4":
        rtext = markdown(g.response, extras=["fenced-code-blocks", "tables"])
    elif g.model == "tts-1":
        filepath = g.filepath
        with open(filepath, 'rb') as audio_file:
            encoded_image = base64.b64encode(audio_file.read()).decode('utf-8')
        rtext = f' <audio controls><source src="data:audio/mpeg;base64,{encoded_image}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        return render_template('index.html', prompt_text=markdown(g.user_prompt, extras=["fenced-code-blocks"]),
                           gpt_response_text=rtext)
    elif g.model == "dall-e-3":
        filepath = g.filepath
        with open(filepath, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        rtext = f' <img src="data:image/png;base64,{encoded_image}" alt="{filepath}" style="max-width:400px;width: auto;height: auto;object-fit: contain">'

    return render_template('index.html', prompt_text=markdown(g.user_prompt, extras=["fenced-code-blocks"]),
                       gpt_response_text=rtext)


def d():
    yield from lr.get_log(".\log", last=50)


@app.route('/stream')
def stream():
    def generate():
        yield f"data: Task is complete\n\n"
        for i in d():
            print(i)
            data = markdown2.markdown(i, extras=["fenced-code-blocks", "tables"])
            # data = data.replace('\n', '')
            data = json.dumps({"d": data})
            yield f"data: {data}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host="njbedw2", port=80, debug=True)
