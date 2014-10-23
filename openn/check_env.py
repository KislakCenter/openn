#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pkg_resources
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from distutils.version import StrictVersion

required_version = '2.6'

def load_settings():
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openn.settings')
        from django.conf import settings
        return settings
    except ImportError:
        print 'Could not load django.conf.settings'


def check_version():
    status = True
    curr_version = sys.version.split()[0]
    if StrictVersion(required_version) > StrictVersion(curr_version):
        print 'Python version must be equal to or higher than v%s; found: v%s' % (required_version, curr_version)
        status = False

    return status

def check_env_vars(settings):
    status = True
    for var in settings.REQUIRED_ENV_VARS:
        if var not in os.environ:
            print 'Required environment variable not set: %s' % (var, )
            status = False
        elif var.endswith('_DIR'):
            dir = os.environ.get(var)
            if not os.path.exists(dir):
                print 'Required directory not found %s=%s' % (var, dir)
                status = False
    return status

def check_requirements():
    status = True
    reqs = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    if os.path.exists(reqs):
        deps = [line for line in open(req)]
        try:
            pkg_resources.require(deps)
        except (DistributionNotFound, VersionConflict) as ex:
            print "Dependency problem found: %s" % (ex, )
            status = False
    else:
        print 'Requirements file not found: %s' % (reqs, )
        status = False

    return status

def check_env():
    settings = load_settings()
    if settings:
        return (check_version() and
                check_env_vars(settings) and
                check_requirements() and 0 or 1)
    else:
        return 1


def main():
    """
    Main: confirm that environment can run mm python scripts

    """

    return check_env()

if __name__ == "__main__":
    sys.exit(main())
