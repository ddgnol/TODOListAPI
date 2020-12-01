import logging
import socket
import time
import traceback
from slack import WebClient

TOKEN_AUTH_SLACK = "xoxp-1513369155061-1516457175858-1526347927700-689ff5f994494e5544a55d4bd4629138"
SLACK_CHANNEL = "web-api"
NOTIFY_LEVEL_NUM = 100


class SlackHandler(logging.Handler):
    def emit(self, record):
        try:
            record.exc_info = record.exc_text = None
            content = {'text': self.format(record)}
            # TODO authorize to thread job
            sc = WebClient(TOKEN_AUTH_SLACK)
            sc.chat_postMessage(
                channel="#{}".format(SLACK_CHANNEL),
                text="```{}```".format(content['text'])
            )
        except:
            self.handleError(record)


class Logger:
    @staticmethod
    def __init__():
        format_string = '%(asctime)s {hostname} %(levelname)s %(message)s'.format(**{'hostname': socket.gethostname()})
        format_log = logging.Formatter(format_string)
        format_log.converter = time.gmtime

        logging.basicConfig(level=logging.INFO)
        logging.disable(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(format_log)
        # logging.getLogger().addHandler(stream_handler)
        slack_handler = SlackHandler()
        slack_handler.setFormatter(format_log)
        logging.getLogger().addHandler(slack_handler)

        logging.addLevelName(NOTIFY_LEVEL_NUM, "NOTIFY")

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def notify(message):
        logging.log(NOTIFY_LEVEL_NUM, message)

    @staticmethod
    def debug(message):
        logging.debug(message)
    @staticmethod
    def error(trace=None):
        if trace is None:
            tb = traceback.format_exc()
            trace = 'Something was wrong' if tb is None else tb
        logging.error(trace)

logger = Logger()



