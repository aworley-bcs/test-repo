#!/usr/bin/env python3

import argparse
import logging
import sys
import os

LOGGER = logging.getLogger('bcs')

LOGGING_LEVEL = logging.INFO
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'


#
# Decorator for build script main functions
# - Initializes logging
# - Runs argument parsing
# - Calls main function with parsed arguments
# - Skips calling main function if TC_MODE == DEV (optional)
def script_main(parser, skip_on_tc_mode_dev=True):
    def _script_main(main_fun):
        if _is_main_entry_point(main_fun):

            parser.add_argument(
                '--log-level',
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                default='INFO',
                help='Control log verbosity')

            args = parser.parse_args()

            logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
            LOGGER.info('Running: {0}'.format(sys.argv[0]))
            LOGGER.info('Command line: {0}'.format(' '.join(sys.argv[1:])))

            if skip_on_tc_mode_dev and os.environ.get('TC_MODE') == 'DEV':
                LOGGER.info('TC_MODE == DEV : Skipping execution of main')
            else:
                main_fun(args)

    return _script_main


def _is_main_entry_point(f):
    return f.__globals__['__name__'] == '__main__'


#
# Get a logger that is a child of the root bcs. logger
def get_logger(name):
    return logging.getLogger('bcs.'+name)


#
# Get an ArgumentParser for TeamCity REST API credentials
def get_tc_cred_parser(add_help=False):
    parser = argparse.ArgumentParser(add_help=add_help)
    parser.add_argument(
        '--tc-user',
        required=True,
        help='TeamCity Username for REST API')
    parser.add_argument(
        '--tc-password',
        required=True,
        help='TeamCity Password for REST API')
    parser.add_argument(
        '--tc-server',
        required=True,
        default='https://teamcity.bcs.systems',
        help='TeamCity Server Root URI')
    return parser

#
# Get an ArgumentParser for MMS API server credentials
def get_mms_cred_parser(settings, add_help=False):
    parser = argparse.ArgumentParser(add_help=add_help)
    parser.add_argument(
        '--mms-user',
        default=settings.MMS_USERNAME,
        help='MMS API server username')
    parser.add_argument(
        '--mms-url',
        default=settings.MMS_URL,
        help='MMS API server URL')
    return parser
