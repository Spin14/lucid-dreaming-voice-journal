import logging

from dream_journal.config import LOG_FILENAME, KEYWORD_PHRASE_TIME_LIMIT
from dream_journal.audio import recognize_audio, adjust_source
from dream_journal.keyword_responses import get_keyword_response


# logging
logger = logging.getLogger(__name__)


def capture_audio_keyword():
    return recognize_audio(time=KEYWORD_PHRASE_TIME_LIMIT)


def ready_for_keyword():
    logger.info('waiting for audio keyword')
    keyword, keyword_response = get_keyword_response(capture_audio_keyword())

    if keyword is not None:
        logger.info('running response for keyword: {0}'.format(keyword))
        keyword_response()
        logger.info('finished running response for keyword: {0}'.format(keyword))
        return True

    return False


def main():
    adjust_source()
    try:
        while True:
            ready_for_keyword()
    except KeyboardInterrupt:
        logger.info('Exiting')


if __name__ == '__main__':
    file_handler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    main()