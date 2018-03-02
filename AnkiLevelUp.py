from AnkiTools.tools.read import readAnki2
from AnkiLevelUp import webpy
import webview
from time import sleep

anki = readAnki2('Chinese.anki2')

if __name__ == '__main__':
    webpy.initServer(anki).start()

    sleep(1)

    webview.create_window('Anki Level Up', 'http://localhost:8080',
                          width=800, height=600, resizable=True, fullscreen=False)
