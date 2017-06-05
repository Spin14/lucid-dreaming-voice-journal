import dream_journal.config as config
from dream_journal.dream_recording import record_dream


def default_response():
    return False

keyword_to_response_dict = {
    config.DREAM_RECORD_KW: record_dream
}


def get_keyword_response(keyword):
    if not isinstance(keyword, str):
        return None, default_response

    if keyword in keyword_to_response_dict:
        return keyword, keyword_to_response_dict[keyword]

    return None, default_response








