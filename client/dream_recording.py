def record_dream():
    pass


# def record_dream():
#     r.pause_threshold = ENTRY_PAUSE_THRESHOLD
#     dream = list()
#
#     while True:
#         logger.debug('waiting for audio')
#         memory = recognize_audio()
#         logger.debug('audio collected and decoded: {}'.format(memory))
#
#         if memory is None:
#             play_fail()
#         elif memory == STOP_KEYWORD:
#             logger.debug('Keyword match [{}]'.format(STOP_KEYWORD))
#             play_stop()
#             return dream
#         else:
#             play_success()
#             logger.debug('saving new memory')
#             dream.append(memory)
#
#
# def save(dream):
#     filename = '{0}dream_{1}.txt'.format(OUTPUT_DIR, datetime.now().strftime('%y-%m-%d'))
#     logger.debug('filename: {}'.format(filename))
#
#     with open(filename, 'a') as file:
#         for memory in dream:
#             file.write('{}\n'.format(memory))