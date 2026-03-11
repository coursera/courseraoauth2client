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

from courseraoauth2client import oauth2

import argparse
import configparser
import pickle
from urllib.parse import parse_qs, urlparse
from unittest.mock import MagicMock
import os
import time
import pytest


def test_compute_cache_filename_args_override():
    args = argparse.Namespace()
    args.token_cache_file = '/tmp/cache/override_cache.pickle'
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '/tmp/not_cache')
    assert oauth2.build_oauth2('my_app', args, cfg)\
        .token_cache_file == '/tmp/cache/override_cache.pickle'


def test_compute_cache_filename():
    args = argparse.Namespace()
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '/tmp/cache')
    assert oauth2.build_oauth2('my_app', args, cfg)\
        .token_cache_file == '/tmp/cache/my_app_oauth2_cache.pickle'


def test_cache_filename_sanitized():
    args = argparse.Namespace()
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '/tmp/cache')
    assert oauth2.build_oauth2('@weird$app name', args, cfg) \
        .token_cache_file == '/tmp/cache/_weird_app_name_oauth2_cache.pickle'


def test_compute_cache_filname_expanded_path():
    args = argparse.Namespace()
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '~/.coursera')
    computed = oauth2.build_oauth2('my_app', args, cfg).token_cache_file
    assert '~' not in computed, 'Computed contained "~": %s' % computed


def test_compute_cache_filname_path_no_double_slash():
    args = argparse.Namespace()
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '~/.coursera/')
    computed = oauth2.build_oauth2('my_app', args, cfg).token_cache_file
    assert '//' not in computed, 'Computed contained "//": %s' % computed


def test_compute_cache_filname_expanded_path_overrides():
    args = argparse.Namespace()
    args.token_cache_file = '~/.coursera/override_cache.pickle'
    args.client_id = 'client_id'
    args.client_secret = 'fake-secret'
    args.scopes = 'fake scopes'
    cfg = configparser.ConfigParser()
    cfg.add_section('oauth2')
    cfg.set('oauth2', 'token_cache_base', '~/.coursera')
    computed = oauth2.build_oauth2('my_app', args, cfg).token_cache_file
    assert '~' not in computed, 'Computed contained "~": %s' % computed
    assert 'override_cache.pickle' in computed, 'Computed was not overridden!'


@pytest.mark.parametrize(
    'cache_type,should_be_allowed',
    [
        ({}, False),
        ([], False),
        (3, False),
        ({'token': 'asdfg', 'expires': 12345.0}, True),
    ],
)
def test_check_cache_types(cache_type, should_be_allowed):
    oauth2_client = oauth2.CourseraOAuth2(
        'id', 'secret', 'fake scopes', '/cache.file')
    result = oauth2_client._check_token_cache_type(cache_type)
    assert result == should_be_allowed, \
        'Got %(result)s. Expected: %(expected)s' % {
            'result': result,
            'expected': should_be_allowed,
        }


def test_load_configuration():
    cfg = oauth2.configuration()
    assert cfg.get('oauth2', 'hostname') == 'localhost', 'hostname incorrect'
    assert cfg.getint('oauth2', 'port') == 9876, 'oauth2.port not correct'
    assert cfg.get('oauth2', 'api_endpoint') == 'https://api.coursera.org', \
        'oauth2.api_endpoint incorrect'
    assert cfg.getboolean('oauth2', 'verify_tls'), 'oauth2.verify_tls wrong'


def test_expired_token_serialization():
    authorizer = oauth2.CourseraOAuth2Auth(token='asdf', expires=time.time())
    exception = oauth2.ExpiredToken(authorizer)
    assert len("%s" % exception) > 0


def test_authorizer_throws_when_expired():
    authorizer = oauth2.CourseraOAuth2Auth(token='asdf',
                                           expires=time.time()-10)
    fake_request = MagicMock()
    try:
        authorizer(fake_request)
    except oauth2.ExpiredToken:
        pass
    else:
        assert False, 'authorizer should have thrown an exception'


def test_authorizer_does_not_throw_when_not_expired():
    authorizer = oauth2.CourseraOAuth2Auth(token='asdf',
                                           expires=time.time()+10)
    fake_request = MagicMock()
    authorizer(fake_request)


def test_build_authorization_url():
    oauth2_client = oauth2.CourseraOAuth2(
        'my_fake_client_id',
        'my_fake_secret',
        'view_profile',
        '/cache.file')

    state_token = 'my_fake_state_token'

    actual = oauth2_client._build_authorizaton_url(state_token)

    parsed = urlparse(actual)
    assert parsed.scheme == 'https'
    assert parsed.netloc == 'accounts.coursera.org'
    assert parsed.path == '/oauth2/v1/auth'
    assert parse_qs(parsed.query) == {
        'access_type': ['offline'],
        'state': ['my_fake_state_token'],
        'redirect_uri': ['http://localhost:9876/callback'],
        'response_type': ['code'],
        'client_id': ['my_fake_client_id'],
        'scope': ['view_profile'],
    }


@pytest.mark.parametrize(
    'read_data,expected',
    [
        (pickle.dumps({'token': 'CiCptJ_07TeNA', 'expires': 1438815118.228845, 'refresh': 'STLuX5'})[5:], None),
        (b';lkajsdf;lkjasdlfk;j', None),
        (pickle.dumps({'weird': 'stuff'}), None),
    ],
)
def test_loading_cache(tmp_path, read_data, expected):
    cache_file = tmp_path / 'cache.file'
    cache_file.write_bytes(read_data)
    oauth2_instance = oauth2.CourseraOAuth2(
        'id', 'secret', 'scopes', str(cache_file))
    token_cache = oauth2_instance.token_cache
    assert token_cache == expected, 'Token cache was: %s' % token_cache
