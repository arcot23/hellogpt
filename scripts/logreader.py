import os
import json
import markdown2
import base64


def as_html(data):
    return markdown2.markdown(data, extras=["fenced-code-blocks", "tables"])


def get_log(log_path=r"..\log", last=20):
    print(log_path)
    if os.path.exists(log_path) == False:
        print(f"{log_path} doesn't exist.")
        return
    files = os.listdir(log_path)
    files = [f for f in files if f.endswith(".txt")][-last:]
    files.sort(reverse=True)
    for file in files[:10]:
        full_path = os.path.join(log_path, file)
        print(f"- {full_path}")
        # yield as_html(f"## {full_path}")
        f = open(full_path, "r")
        d = json.load(f)
        user_prompt = as_html(f"{d['user_prompt']}")
        user_prompt = f"<div class='space'></div><div id='prompt-input'>{user_prompt}</div>"
        yield user_prompt
        if d['model'] == "tts-1":
            filepath = d['filepath']
            with open(filepath, 'rb') as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
            response = f' <audio controls><source src="data:audio/mpeg;base64,{encoded_audio}">Your browser does not support the audio element.</audio>'
        elif d['model'] == "dall-e-3":
            filepath = d['filepath']
            with open(filepath, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            response = f' <img src="data:image/png;base64,{encoded_image}" alt="{filepath}" style="max-width:400px;width: auto;height: auto;object-fit: contain">'
        else:
            response = as_html(d['response'])
        response = f"<div class='space'></div><div id='prompt-response'>{response}</div>"
        yield response


def write_logs_to_html(log_path=r"..\log"):
    md = ""
    for record in get_log(log_path):
        md += record

    html = rf"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Log</title>
        <style>body{{font-family:calibri; padding: 1px 1px 1px 1px; line-height: 140%;}} code, pre{{background-color:whitesmoke; padding: 0.5em;}}</style>
    </head>
    <body>
    {md}
    </body>
    </html>
    """
    with open(os.path.join(log_path, "index.html"), "w") as f:
        f.write(html)

# write_logs_to_html(".\log")
