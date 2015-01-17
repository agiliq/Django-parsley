#!/usr/bin/env python

import sys
import os
from os.path import dirname, abspath
from optparse import OptionParser

from django.conf import settings

# For convenience configure settings if they are not pre-configured or if we
# haven't been provided settings to use by environment variable.
if not settings.configured and not os.environ.get('DJANGO_SETTINGS_MODULE'):
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'parsley',
        ],
        STATIC_URL = "/static/",
    )

    # Setup Django 1.7+ (AppRegistryNotReady).
    import django
    if hasattr(django, 'setup'):
        django.setup()

from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['parsley']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    test_runner = DjangoTestSuiteRunner(
        verbosity=kwargs.get('verbosity', 1),
        interactive=kwargs.get('interactive', False),
        failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')
    (options, args) = parser.parse_args()
    runtests(failfast=options.failfast, *args)
