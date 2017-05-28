from datetime import datetime

from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG

from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

from feedback_sound import play_success, play_fail, play_start, play_stop, play_end

from config import (ENTRY_PAUSE_THRESHOLD, KEYWORD_PAUSE_THRESHOLD, KEYWORD_PHRASE_TIME_LIMIT,
    LOG_FILENAME, OUTPUT_DIR, START_KEYWORD, STOP_KEYWORD)

# logging
logger = getLogger(__name__)
handler = StreamHandler()
file_handler = FileHandler(LOG_FILENAME)
formatter = Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(file_handler)
logger.setLevel(DEBUG)

r = Recognizer()
micro = Microphone()

with micro as source:
    r.adjust_for_ambient_noise(source)


def recognize_audio(time=None):
    logger.debug('listening for for audio..')
    with micro as source:
        audio = r.listen(source, phrase_time_limit=time)

    logger.debug('recorded new audio'.format(KEYWORD_PAUSE_THRESHOLD))
    try:
        # recognize speech using Google Speech Recognition
        return r.recognize_google(audio)

    except UnknownValueError:
        # error feedback sound 1
        return None

    except RequestError:
        # error feedback sound 2
        return None


def capture_keyword(key_work):
    assert isinstance(key_work, str)
    r.pause_threshold = KEYWORD_PAUSE_THRESHOLD

    if key_work == recognize_audio(time=KEYWORD_PHRASE_TIME_LIMIT):
        logger.debug('Keyword match {}'.format(key_work))
        play_start()
        return True


def record_dream():
    r.pause_threshold = ENTRY_PAUSE_THRESHOLD
    dream = list()

    while True:
        logger.debug('waiting for audio')
        memory = recognize_audio()
        logger.debug('audio collected and decoded: {}'.format(memory))

        if memory is None:
            play_fail()
        elif memory == STOP_KEYWORD:
            logger.debug('Keyword match [{}]'.format(STOP_KEYWORD))
            play_stop()
            return dream
        else:
            play_success()
            logger.debug('saving new memory')
            dream.append(memory)


def save(dream):
    filename = '{0}dream_{1}.txt'.format(OUTPUT_DIR, datetime.now().strftime('%y-%m-%d'))
    logger.debug('filename: {}'.format(filename))

    with open(filename, 'a') as file:
        for memory in dream:
            file.write('{}\n'.format(memory))


def main():
    logger.info('main has started')
    try:
        while True:
            logger.info('waiting for audio keyword: [{}]'.format(START_KEYWORD))
            if capture_keyword(START_KEYWORD):
                logger.info('Recording Dream')
                dream = record_dream()
                logger.info('Saving Dream')
                save(dream)  # in the future we will push dream_entries to the cloud instead
                logger.info('Dream saved')
    except KeyboardInterrupt:
        play_end()


main()

