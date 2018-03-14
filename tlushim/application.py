import logging

from tlushim import Tlushim
from config import TlushimConfig

logger = logging.getLogger(__name__)


class Application(object):
    def __init__(self, namespace):
        self.namespace = namespace

    def run(self):
        record = TlushimConfig(self.namespace).read()
        requested_month = "_".join([self.namespace.year, self.namespace.month])
        (days, differe, ahead_or_behind) = Tlushim(record.user_id, record.password).calculate(requested_month)

        logger.info('Per {0} days processed this month , you are {1:.2f} hours {2}'
                    .format(days, differe, ahead_or_behind))
