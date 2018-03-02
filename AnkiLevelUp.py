from AnkiLevelUp import webpy

from AnkiTools.tools.read import readAnki2
import webview
from time import sleep

anki = readAnki2('Chinese.anki2')


def url_ok(url, port):
    # Use httplib on Python 2
    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

    try:
        conn = HTTPConnection(url, port)
        conn.request("HEAD", "/")
        r = conn.getresponse()
        return r.status == 200
    except:
        return False


if __name__ == '__main__':
    webpy.initServer(anki).start()

    while not url_ok("localhost", 8080):
        sleep(0.1)

    webview.create_window('Anki Level Up', 'http://localhost:8080',
                          width=800, height=600, resizable=True, fullscreen=False)
