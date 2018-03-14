import os
import errno
import logging
import getpass
import ConfigParser

logger = logging.getLogger(__name__)


class TlushimConfig(object):
    DEFAULT_SECTION = "tlushim"

    def __init__(self, namespace):
        self.parser = ConfigParser.SafeConfigParser()
        if not self.parser.read(self.__get_config_file_path()) or namespace.configure:
            self.parser.remove_section(self.DEFAULT_SECTION)
            self.__configure(self.parser)

    def read(self):
        params = dict()
        for item in self.parser.items(self.DEFAULT_SECTION):
            params[item[0]] = item[1]
        return self.TlushimConfigRecord(**params)

    def __get_config_file_path(self):
        return os.path.join(os.getenv('LOCALAPPDATA'), "tlushim", "tlushim.config")

    def __configure(self, parser):
        """
        :param ConfigParser.SafeConfigParser parser:
        :return:
        """
        user_id = raw_input("Please enter your id number: ")
        password = getpass.getpass("Please enter your password in plain text (very safe): ")
        parser.add_section(self.DEFAULT_SECTION)
        parser.set(self.DEFAULT_SECTION, "user_id", user_id)
        parser.set(self.DEFAULT_SECTION, "password", password)

        path = self.__get_config_file_path()
        # https://stackoverflow.com/a/12517490
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(path, mode='w') as fp:
            parser.write(fp)
            logger.debug('Configuration file saved successfully at {}'.format(path))

    class TlushimConfigRecord(object):
        def __init__(self, user_id, password):
            self.user_id = user_id
            self.password = password
