from datetime import datetime
from os.path import isdir, isfile
from os import rmdir, remove
from unittest import TestCase
from unittest.mock import patch


class TestAudio(TestCase):
    """Testing audio.py"""

    @patch('client.audio.r.adjust_for_ambient_noise',
           side_effects=lambda x: None)
    def test_adjust_source(self, mock_adjust_for_ambient_noise):
        from client.audio import adjust_source, micro

        adjust_source()

        mock_adjust_for_ambient_noise.assert_called_with(micro)
        self.assertEquals(mock_adjust_for_ambient_noise.call_count, 1)

    @patch('client.audio.r.recognize_google')
    @patch('client.audio.r.listen')
    def test_recognize_audio(self, mock_listen, mock_recognize_google):
        from client.audio import \
            recognize_audio, micro, UnknownValueError, RequestError

        def dummy(positional, **kwargs):
            return True

        mock_listen.side_effect = dummy
        mock_recognize_google.side_effect = dummy
        self.assertIsNotNone(recognize_audio())
        self.assertEqual(mock_listen.call_count, 1)
        mock_listen.assert_called_with(micro, phrase_time_limit=None)
        self.assertEqual(mock_recognize_google.call_count, 1)

        def raise_unknown_value_error(positional):
            raise UnknownValueError

        mock_listen.side_effect = dummy
        mock_recognize_google.side_effect = raise_unknown_value_error
        self.assertIsNone(recognize_audio(None))
        self.assertEqual(mock_listen.call_count, 2)
        mock_listen.assert_called_with(micro, phrase_time_limit=None)
        self.assertEqual(mock_recognize_google.call_count, 2)

        def raise_request_error(positional, **kwargs):
            raise RequestError

        mock_listen.side_effect = dummy
        mock_recognize_google.side_effect = raise_request_error
        self.assertIsNone(recognize_audio(2))
        self.assertEqual(mock_listen.call_count, 3)
        mock_listen.assert_called_with(micro, phrase_time_limit=2)
        self.assertEqual(mock_recognize_google.call_count, 3)


class TestKeywordResponses(TestCase):
    """Testing keyword_responses.py"""

    def test_keyword_NONE(self):
        from client.keyword_responses import get_keyword_response

        keyword, response = get_keyword_response(None)

        self.assertIsNone(keyword)
        self.assertIsNone(response)

    def test_keyword_INVALID(self):
        from client.keyword_responses import get_keyword_response
        from client.keyword_responses import default_response

        keyword, response = get_keyword_response('not_mapped')

        self.assertEquals(keyword, 'Unknown')
        self.assertEquals(response, default_response)
        self.assertFalse(response())

    def test_keyword_RECORD_DREAM(self):
        from client.keyword_responses import get_keyword_response
        from client.config import DREAM_RECORD_KW
        from client.dream_recording import record_dream

        keyword, response = get_keyword_response(DREAM_RECORD_KW)

        self.assertEquals(keyword, DREAM_RECORD_KW)
        self.assertEquals(response, record_dream)


class TestDreamRecording(TestCase):
    """Testing dream_recording.py"""
    directory = 'test_dir/'
    filename = 'test_file.txt'

    def tearDown(self):
        if isdir(TestDreamRecording.directory):
            rmdir(TestDreamRecording.directory)

        if isfile(TestDreamRecording.filename):
            remove(TestDreamRecording.filename)

    def test_gen_filename(self):
        from client.dream_recording import gen_filename

        filename = gen_filename(TestDreamRecording.directory)
        expected_filename =\
            '{0}dream_{1}.txt'.format(TestDreamRecording.directory, datetime.now().strftime('%y-%m-%d'))

        self.assertTrue(isdir(TestDreamRecording.directory))
        self.assertEquals(filename, expected_filename)

    def test_save(self):
        from client.dream_recording import save

        memory_0 = "today i dreamed i had 100% test coverage"
        save(TestDreamRecording.filename, memory_0)
        memory_1 = "it was then i realized it was just a dream"
        save(TestDreamRecording.filename, memory_1)

        self.assertTrue(isfile(TestDreamRecording.filename))

        with open(TestDreamRecording.filename) as f:
            file_memories = f.readlines()

        self.assertTrue(len(file_memories), 2)
        self.assertEquals(file_memories[0], '{}\n'.format(memory_0))
        self.assertEquals(file_memories[1], '{}\n'.format(memory_1))

    @patch('client.dream_recording.save', side_effect=lambda x, y: None)
    @patch('client.dream_recording.gen_filename', side_effect=lambda x: None)
    @patch('client.dream_recording.recognize_audio')
    def test_record_dream(self, mock_recognize_audio, m_gen_filename, m_save):
        from client.dream_recording import record_dream

        mock_recognize_audio.side_effect = lambda: None

        self.assertFalse(record_dream())
        self.assertEqual(mock_recognize_audio.call_count, 1)
        mock_recognize_audio.assert_called_with()
        self.assertEqual(m_save.call_count, 0)
        self.assertEqual(m_gen_filename.call_count, 0)

        mock_recognize_audio.side_effect = lambda: True

        self.assertTrue(record_dream())
        self.assertEqual(mock_recognize_audio.call_count, 2)
        mock_recognize_audio.assert_called_with()
        self.assertEqual(m_save.call_count, 1)
        self.assertEqual(m_gen_filename.call_count, 1)


class TestDreamJournal(TestCase):

    @patch('client.dream_journal.recognize_audio')
    def test_capture_audio_keyword(self, mock_recognize_audio):
        from client.dream_journal import capture_audio_keyword, KEYWORD_PHRASE_TIME_LIMIT

        def dummy(**kwargs):
            pass

        mock_recognize_audio.side_effect = dummy

        capture_audio_keyword()
        self.assertEqual(mock_recognize_audio.call_count, 1)
        mock_recognize_audio.assert_called_with(time=KEYWORD_PHRASE_TIME_LIMIT)












