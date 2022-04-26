import json
import duolingo
from verbecc import Conjugator

with open("config.json", "r") as config:
    data = json.load(config)

cg = Conjugator(lang=data["learningLanguage"])

lingo  = duolingo.Duolingo(data["username"], data["password"])
words = lingo.vocabulary["vocab_overview"]

dico = {}
audio = {}
verbs = []

# read audio.json file
try:
    with open("audio.json", "r", encoding="UTF-8") as audioFile:
        audio = json.load(audioFile)
except IOError:
    audio = {}

for i in words:

    # Get the audio file
    wordAudio = None
    if i["word_string"] in audio:
        wordAudio = audio[i["word_string"]]
    else:
        wordAudio = lingo.get_audio_url(i["word_string"], language_abbr=data["learningLanguage"])
        if wordAudio:
            audio[i["word_string"]] = wordAudio

    # Verbs
    if i["infinitive"]:
        if i["infinitive"] not in verbs: 
            verbs.append(i["infinitive"])
    else:
        if i["skill"] in dico:
            dico[i["skill"]].append({
                "infinitive": i["infinitive"],
                "word_string": i["word_string"],
                "pos": i["pos"],
                "gender": i["gender"],
                "audio": wordAudio,
                "translation": lingo.get_translations([i["word_string"]], source=data["learningLanguage"], target=data["yourLanguage"])
            })

        else:
            dico[i["skill"]] = [{
                "infinitive": i["infinitive"],
                "word_string": i["word_string"],
                "pos": i["pos"],
                "gender": i["gender"],
                "audio": wordAudio,
                "translation": lingo.get_translations([i["word_string"]], source=data["learningLanguage"], target=data["yourLanguage"])
            }]

# Update audio.json
with open('audio.json', 'w', encoding="UTF-8") as audioFile:
    json.dump(audio, audioFile, indent=4)

with open("duolingo.html", "w", encoding="UTF-8") as file:
    text = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>

    <style>
    tr, td {
        border: 1px solid black;
        padding: 5px 10px;
    }
    table {
        border-collapse: collapse;
    }
    </style>
    """

    # Vocabulary
    text += "<details><summary><b>VOCABULARY</b></summary>"

    for key, values in dico.items():
        text += f"\n<h1>{key}</h1>\n<table>\n"
        values = sorted(values, key=lambda value: value["word_string"])
        for value in values:
            text += f"<tr><td>{value['word_string']}</td><td>{', '.join(value['translation'][value['word_string']])}</td><td><audio controls><source src='{value['audio']}' type='audio/ogg'></audio></td></tr>\n"
        text += "</table>\n"

    text += "</details>"

    # Verbs
    text += "<details><summary><b>VERBS</b></summary>"

    for verb in verbs:
        text += f"\n<h1>{verb}</h1>\n<table>\n"
        text += f"\n<h1>Presente</h2>\n<table>\n"

        conjugation = cg.conjugate(verb)
        conj = conjugation["moods"]["indicativo"]["presente"]
        
        for i in conj:
            text += f"<tr><td>{i}</td><tr>"
        
        text += "</table>\n"

    text += "</details>"

    text += "</body></html>"
    file.write(text)