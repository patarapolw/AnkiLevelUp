import web
import subprocess
from threading import Thread

from AnkiLevelUp.common import stopSpeaking, speakLoop, toFrontAndSpoken

urls = (
    '/', 'index',
    '/decks/(.*)', 'decks',
    '/speak', 'speak'
)

app = web.application(urls, globals())
render = web.template.render('templates')

class index:
    def GET(self):
        global anki
        stopSpeaking()
        output = ''
        old_length = 0
        for deck_name, deck_id in sorted((deck['name'], did) for (did, deck) in anki.decks.items()):
            names = deck_name.split('::')
            content = '<a href="decks/' + deck_id + '">' + names[-1] + '</a><br />'
            new_length = len(names)

            if new_length > old_length:
                while new_length > old_length:
                    old_length += 1
                    output += '<ul><li>'
                output += names[-1]
            elif new_length == old_length:
                output += wrapHtml(content, '<li></li>')
            elif new_length < old_length:
                while new_length < old_length:
                    old_length -= 1
                    output += '</ul>'
                output += '<li>' + names[-1]

            old_length = new_length

        output = wrapHtml(output, '<ul class="collapsibleList"></ul>')
        return render.index(output)


class decks:
    def GET(self, deck_id):
        global anki
        output = ''
        stopSpeaking()
        speaking = speakLoop(anki, deck_id)
        speaking.start()
        for card in anki.cards.values():
            if card['did'] == deck_id:
                front, spoken = toFrontAndSpoken(card)
                output += '<a href="" onclick="$.post(\'../speak\', { word: \''\
                          + spoken + '\'}); return false;" title="' \
                          + spoken + '">'\
                          + front + '</a><br />'
        return render.index(output)


class speak:
    def POST(self):
        post = web.input()
        subprocess.call(['say','-v','ting-ting',post.word])


class initServer(Thread):
    def __init__(self, a):
        super(initServer, self).__init__()
        self.daemon = True
        global anki
        anki = a

    def run(self):
        app.run()


def wrapHtml(inner, wrapper):
    head, tail = wrapper.split('></')
    return head + '>' + inner + '</' + tail
