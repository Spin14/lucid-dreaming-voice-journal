from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG

from client.audio import recognize_audio

from client.keyword_responses import get_keyword_response

from client.config import LOG_FILENAME, KEYWORD_PHRASE_TIME_LIMIT

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


def capture_audio_keyword():
    return recognize_audio(time=KEYWORD_PHRASE_TIME_LIMIT)


def main():
    try:
        while True:
            logger.info('waiting for audio keyword')
            keyword, keyword_response = get_keyword_response(capture_audio_keyword())

            if keyword_response is not None:
                logger.info('running response for keyword: {0}'.format(keyword))
                keyword_response.run()
                logger.info('finished running response for keyword: {0}'.format(keyword))

    except KeyboardInterrupt:
        logger.info('Exiting')


main()

