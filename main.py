import json
import duolingo

with open("config.json", "r") as config:
    data = json.load(config)

lingo  = duolingo.Duolingo(data["username"], data["password"])
words = lingo.vocabulary["vocab_overview"]

dico = {}

for i in words:
    if i["skill"] in dico:
        dico[i["skill"]].append({
            "infinitive": i["infinitive"],
            "word_string": i["word_string"],
            "pos": i["pos"],
            "gender": i["gender"],
            "audio": lingo.get_audio_url(i["word_string"], language_abbr=data["learningLanguage"]),
            "translation": lingo.get_translations([i["word_string"]], source=data["learningLanguage"], target=data["yourLanguage"])
        })
    else:
        dico[i["skill"]] = [{
            "infinitive": i["infinitive"],
            "word_string": i["word_string"],
            "pos": i["pos"],
            "gender": i["gender"],
            "audio": lingo.get_audio_url(i["word_string"], language_abbr=data["learningLanguage"]),
            "translation": lingo.get_translations([i["word_string"]], source=data["learningLanguage"], target=data["yourLanguage"])
        }]

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

    for key, values in dico.items():
        text += f"\n<h1>{key}</h1>\n<table>\n"
        for value in values:
            text += f"<tr><td>{value['word_string']}</td><td>{', '.join(value['translation'][value['word_string']])}</td><td><audio controls><source src='{value['audio']}' type='audio/ogg'></audio></td></tr>\n"
        text += "</table>\n"

    text += "</body></html>"
    file.write(text)