from datetime import datetime
from os.path import isdir, isfile
from os import rmdir, remove
from unittest import TestCase

from client.keyword_responses import get_keyword_response


test_dir = 'test_dir/'
test_file = 'test_file.txt'


class TestKeywordResponses(TestCase):
    """Testing keyword_responses.py"""

    def test_keyword_NONE(self):
        keyword, response = get_keyword_response(None)

        self.assertIsNone(keyword)
        self.assertIsNone(response)

    def test_keyword_INVALID(self):
        from client.keyword_responses import default_response

        keyword, response = get_keyword_response('not_mapped')

        self.assertEquals(keyword, 'Unknown')
        self.assertEquals(response, default_response)
        self.assertFalse(response())

    def test_keyword_RECORD_DREAM(self):
        from client.config import DREAM_RECORD_KW
        from client.dream_recording import record_dream

        keyword, response = get_keyword_response(DREAM_RECORD_KW)

        self.assertEquals(keyword, DREAM_RECORD_KW)
        self.assertEquals(response, record_dream)


from client.dream_recording import gen_filename, save, record_dream

class TestDreamRecording(TestCase):
    """Testing dream_recording.py"""

    def tearDown(self):
        if isdir(test_dir):
            rmdir(test_dir)

        if isfile(test_file):
            remove(test_file)

    def test_gen_filename(self):
        filename = gen_filename(test_dir)
        expected_filename =\
            '{0}dream_{1}.txt'.format(test_dir, datetime.now().strftime('%y-%m-%d'))

        self.assertTrue(isdir(test_dir))
        self.assertEquals(filename, expected_filename)

    def test_save(self):
        memory_0 = "today i dreamed i had 100% test coverage"
        save(test_file, memory_0)
        memory_1 = "it was then i realized it was just a dream"
        save(test_file, memory_1)

        self.assertTrue(isfile(test_file))

        with open(test_file) as f:
            file_memories = f.readlines()

        self.assertTrue(len(file_memories), 2)
        self.assertEquals(file_memories[0], '{}\n'.format(memory_0))
        self.assertEquals(file_memories[1], '{}\n'.format(memory_1))






