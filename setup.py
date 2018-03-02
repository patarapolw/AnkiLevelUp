from setuptools import setup
import sys

mainscript = 'AnkiLevelUp.py'
setup_requires = ['web.py==0.40.dev1', 'bs4', 'AnkiTools']

if sys.platform == 'darwin':
    setup_requires.extend(['py2app', 'pywebview[cocoa]'])
    extra_options = dict(
        app=[mainscript],
        options=dict(py2app=dict(
            argv_emulation=True,
            includes='web.wsgiserver.wsgiserver3',
            plist=dict(
                CFBundleName='AnkiLevelUp',
            )
        )),
    )
elif sys.platform == 'win32':
    setup_requires.extend(['py2exe', 'pywebview[winforms]'])
    extra_options = dict(
        app=[mainscript],
        options=dict(py2exe=dict(
            includes='web.wsgiserver.wsgiserver3',
        ))
    )
else:
    setup_requires.extend(['pywebview[gtk3]'])
    extra_options = dict(
        scripts=[mainscript],
    )

setup(
    name='AnkiLevelUp',
    data_files=[
        'static',
        'templates',
        'Chinese.anki2'
    ],
    setup_requires=setup_requires,
    **extra_options
)
