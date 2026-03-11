#!/usr/bin/env python

# Copyright 2016 Coursera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Coursera's OAuth2 client

You may install it from source, or via pip.
"""

from courseraoauth2client import oauth2
import argparse
import logging
import time


def authorize(args):
    """
    Authorizes Coursera's OAuth2 client for using coursera.org API servers for
    a specific application
    """
    oauth2_instance = oauth2.build_oauth2(args.app, args)
    oauth2_instance.build_authorizer()
    logging.info('Application "%s" authorized!', args.app)


def display_auth_cache(args):
    '''
    Writes to the screen the state of the authentication cache. (For debugging
    authentication issues.) BEWARE: DO NOT email the output of this command!!!
    You must keep the tokens secure. Treat them as passwords.
    '''
    oauth2_instance = oauth2.build_oauth2(args.app, args)
    quiet = args.quiet or 0
    if quiet <= 0:
        token = oauth2_instance.token_cache['token']
        if not args.no_truncate and token is not None:
            token = token[:10] + '...'
        print("Auth token: %s" % token)

        expires_time = oauth2_instance.token_cache['expires']
        expires_in = int((expires_time - time.time()) * 10) / 10.0
        print("Auth token expires in: %s seconds." % expires_in)

        if 'refresh' in oauth2_instance.token_cache:
            refresh = oauth2_instance.token_cache['refresh']
            if not args.no_truncate and refresh is not None:
                refresh = refresh[:10] + '...'
            print("Refresh token: %s" % refresh)
        else:
            print("No refresh token found.")


def parser(subparsers):
    # create the parser for the configure subcommand. (authentication / etc.)
    parser_config = subparsers.add_parser(
        'config',
        help='Configure %(prog)s for operation!')
    app_subparser = argparse.ArgumentParser(add_help=False)
    app_subparser.add_argument(
        '--app',
        required=True,
        help='Application to configure')
    app_subparser.add_argument(
        '--reconfigure',
        action='store_true',
        help='Reconfigure existing app?')

    config_subparsers = parser_config.add_subparsers()

    parser_authorize = config_subparsers.add_parser(
        'authorize',
        help=authorize.__doc__,
        parents=[app_subparser])
    parser_authorize.set_defaults(func=authorize)

    parser_local_cache = config_subparsers.add_parser(
        'display-auth-cache',
        help=display_auth_cache.__doc__,
        parents=[app_subparser])
    parser_local_cache.set_defaults(func=display_auth_cache)
    parser_local_cache.add_argument(
        '--no-truncate',
        action='store_true',
        help='Do not truncate the keys [DANGER!!]')

    return parser_config
