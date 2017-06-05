"""
from os import system


def _play_wav(s):
    system('aplay {0}{1}.wav &> /dev/null'.format(SOUND_DIR, s))


def _play_mp3(s):
    system('mpg321 {0}{1}.mp3 &> /dev/null'.format(SOUND_DIR, s))


def play_success():
    _play_wav('success')


def play_fail():
    _play_wav('fail')


def play_start():
    play_success()
    _play_mp3('start')


def play_stop():
    play_success()
    _play_mp3('stop')


def play_end():
    _play_mp3('end')

"""