from unittest import TestCase

from client.keyword_responses import get_keyword_response


class TestKeywordResponses(TestCase):

    def test_keyword_NONE(self):
        keyword, response = get_keyword_response(None)

        self.assertIsNone(keyword)
        self.assertIsNone(response)

    def test_keyword_INVALID(self):
        from client.keyword_responses import default_response

        keyword, response = get_keyword_response('not_mapped')

        self.assertEquals(keyword, '',
                          "keyword str for invalid keyword")
        self.assertEquals(response, default_response,
                          "response for invalid keyword")

    def test_keyword_RECORD_DREAM(self):
        from client.config import DREAM_RECORD
        from client.dream_recording import record_dream

        _, response = get_keyword_response(DREAM_RECORD)

        self.assertEquals(response, record_dream,
                          "response for keyword {0}".format(DREAM_RECORD))

        


