from setuptools import setup

setup(
    name="Telegram Desktop decrypter",
    version="1.2",
    packages=['tdesktop_decrypter'],
    install_requires=['tgcrypto'],
    entry_points={
        'console_scripts': ['tdesktop-decrypter=tdesktop_decrypter:main']
    }
)
