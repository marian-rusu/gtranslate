from setuptools import setup

setup(
    name='gtranslate',
    version='1.0',
    packages=[
        'gtd', 'translator'
    ],
    entry_points={
        'console_scripts': [
            'gtranslate = gtd.gtranslate:gtranslate',
            'gtd = gtd.gtd:start_daemon'
        ]
    }
)
