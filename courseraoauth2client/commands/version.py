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

import sys
from importlib.metadata import PackageNotFoundError, version


def command_version(args):
    try:
        __version__ = version('courseraoauth2client')
    except PackageNotFoundError:
        __version__ = 'Please install this project with setup.py'

    if args.quiet and args.quiet > 0:
        print(__version__)
    else:
        print("Your %(prog)s's version is:\n\t%(version)s" % {
            "prog": sys.argv[0],
            "version": __version__
        })


def parser(subparsers):
    "Build an argparse argument parser to parse the command line."

    # create the parser for the version subcommand.
    parser_version = subparsers.add_parser(
        'version',
        help="Output the version of %(prog)s to the console.")
    parser_version.set_defaults(func=command_version)

    return parser_version
