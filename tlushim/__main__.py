import sys
import datetime
import argparse
import tlushim_log

from argparse import RawTextHelpFormatter
from application import Application


def main(args=None):
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    user_input_grp = parser.add_argument_group('user input')
    user_input_grp.add_argument('-m', '--month', help='Provide specific month in format mm',
                                default=datetime.datetime.now().strftime('%m'))
    user_input_grp.add_argument('-y', '--year', help='Provide specific year in format yyyy',
                                default=datetime.datetime.now().strftime('%Y'))
    config_grp = parser.add_argument_group('configuration')
    config_grp.add_argument('-c', '--configure', help='Start with configuration wizard', action='store_true')

    logging_grp = parser.add_argument_group('logging')
    logging_grp.add_argument('-v', '--verbose', help='Verbose logging', action='store_true')
    logging_grp.add_argument('-d', '--debug', help='Debug log level', action='store_true')

    namespace = parser.parse_args(args)
    root_logger = tlushim_log.configure_logging(namespace)

    sys.exit(calculate_exit_code(lambda: Application(namespace).run(), root_logger))


def calculate_exit_code(app_lambda, logger):
    try:
        app_lambda()
        exit_code = 0
    except BaseException as e:
        exit_code = 1
        logger.error(e.message)
    return exit_code


if __name__ == "__main__":
    main()
