import subprocess
from time import sleep
import threading
from bs4 import BeautifulSoup


def toFrontAndSpoken(card):
    front_num = spoken_num = -1
    model_name = card['note']['model']['name']
    if model_name == 'SpoonFed':
        if card['ord'] == 0:
            front_num = 2
            spoken_num = 2
        elif card['ord'] == 1:
            front_num = 0
            spoken_num = 2
    elif model_name == 'Chinese Vocab':
        if card['ord'] == 0:
            front_num = 3
            spoken_num = 0
        elif card['ord'] == 1:
            front_num = 0
            spoken_num = 0
        elif card['ord'] == 2:
            front_num = 1
            spoken_num = 1
    elif model_name == 'Chinese Hanzi Freq':
        if card['ord'] == 0:
            front_num = 5
            spoken_num = 1
        elif card['ord'] == 1:
            front_num = 1
            spoken_num = 1
        elif card['ord'] == 2:
            front_num = 1
            spoken_num = 1
    else:
        raise ValueError('No model to compare')

    return card['note']['content'][front_num], card['note']['content'][spoken_num]


class speakLoop(threading.Thread):
    def __init__(self, anki, deck_id):
        super().__init__()
        self.daemon = True
        self.anki = anki
        self.deck_id = deck_id
        self.running = True

    def run(self):
        while self.running:
            for card in self.anki.cards.values():
                if card['did'] == self.deck_id:
                    front, spoken = toFrontAndSpoken(card)
                    subprocess.call(['say', '-v', 'alex', BeautifulSoup(front, 'html.parser').text])
                    sleep(1)
                    subprocess.call(['say', '-v', 'ting-ting', spoken])
                    sleep(2)
                if not self.running:
                    break

    def stop(self):
        self.running = False


def stopSpeaking():
    for t in threading.enumerate():
        try:
            t.stop()
        except AttributeError:
            pass
