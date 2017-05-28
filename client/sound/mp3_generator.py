from sys import argv
from os import system
from gtts import gTTS

for arg in argv[1:]:
    tts = gTTS(text=arg, lang='en')
    tts.save('{}.mp3'.format(arg))
    system('mpg321 {}.mp3'.format(arg))