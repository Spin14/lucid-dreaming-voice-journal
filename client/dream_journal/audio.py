from logging import getLogger

from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

from dream_journal.config import AUDIO_PAUSE_THRESHOLD

logger = getLogger('__main__')

r = Recognizer()
r.pause_threshold = AUDIO_PAUSE_THRESHOLD

micro = Microphone()


def adjust_source():
    with micro as source:
        r.adjust_for_ambient_noise(source)


def recognize_audio(time=None):
    logger.debug('listening for for audio..')

    with micro as source:
        audio = r.listen(source, phrase_time_limit=time)

    logger.debug('recorded new audio')

    try:
        # recognize speech using Google Speech Recognition
        return r.recognize_google(audio)

    except UnknownValueError:
        # error feedback sound 1
        return None

    except RequestError:
        # error feedback sound 2
        return None
