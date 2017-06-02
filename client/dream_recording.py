from logging import getLogger
from datetime import datetime
from os import makedirs
from os.path import isdir

from client.config import MEMORY_DIR
from client.audio import recognize_audio

logger = getLogger('__main__')


def gen_filename(directory):
    if not isdir(directory):
        makedirs(directory)
    return '{0}dream_{1}.txt'.format(directory, datetime.now().strftime('%y-%m-%d'))


def save(filename, memory):
    assert isinstance(filename, str)
    assert isinstance(memory, str)

    logger.info('writing to file: {}'.format(filename))
    with open(filename, 'a') as file:
            file.write('{}\n'.format(memory))


def record_dream():
    memory = recognize_audio()
    if memory is not None:
        logger.info("audio collected and decoded: {0}".format(memory))
        save(gen_filename(MEMORY_DIR), memory)
        return True

    logger.info("failed to collect/decode")
    return False


