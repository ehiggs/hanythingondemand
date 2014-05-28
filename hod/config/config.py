from ConfigParser import SafeConfigParser
import socket
import string
from collections import namedtuple, OrderedDict
import subprocess
import os
import pwd
from os.path import join as mkpath, realpath, dirname
from functools import partial
import logging as log

_HOD_MANIFEST_CONFIG = 'hod.conf'

# hod manifest config sections
_META_SECTION = 'Meta'
_CONFIG_SECTION = 'Config'

# serviceaconfig sections 
_UNIT_SECTION = 'Unit'
_EXEC_SECTION = 'Exec'
_ENVIRONMENT_SECTION = 'Environment'

def manifest_config(basedir):
    return mkpath(basedir, _HOD_MANIFEST_CONFIG)

def service_configs(basedir):
    return [f for f in glob.glob(basedir, '*.conf') if not _HOD_MANIFEST_CONFIG]

def _templated_strings():
    '''Return the template dict with the name fed through.'''
    basedir = _mkhodbasedir()

    _strings = {
        'hostname': socket.getfqdn,
        'basedir': lambda: basedir,
        'configdir': lambda: mkpath(basedir, 'conf'),
        'workdir': lambda:  mkpath(basedir, 'work'),
        'user': _current_user,
        'pid': os.getpid,
        'pbsjobid': lambda: os.getenv('PBS_JOBID'),
        'pbsjobname': lambda: os.getenv('PBS_JOBNAME'),
        'pbsnodefile': lambda: os.getenv('PBS_NODEFILE'),
        }

    return _strings

def load_service_config(fileobj):
    '''
    Load a .ini style config for a service.
    '''
    config = SafeConfigParser()
    # stop ConfigParser from making everything lower case.
    config.optionxform = str 
    config.readfp(fileobj)
    return config

def _resolve_templates(templates):
    '''
    Take a dict of string to either string or to a nullary function and
    return the resolved data
    '''
    v = [v if not callable(v) else v() for k,v in templates.items()]
    return dict(zip(templates.keys(), v))

def resolve_config_str(s):
    template = string.Template(s)
    template_strings = _templated_strings()
    resolved_templates = _resolve_templates(template_strings)
    return template.substitute(**resolved_templates)


def _configs(conf_dir):
    '''Find all the configs in the config_directory'''
    results = []
    for root, dirs, files in os.walk(conf_dir):
        results.append((root, map(lambda f: mkpath(root, f), files)))
    return results

def _basedir():
    return os.getenv('TMPDIR', '/tmp')

def _current_user():
    '''
    Return the current user name as recommended by documentation of
    os.getusername.
    '''
    return pwd.getpwuid(os.getuid()).pw_name

def _mkhodbasedir():
    '''
    Construct the pathname for the hod base dir. This is the username, pid,
    hostname.
    '''
    user = _current_user()
    pid = os.getpid()
    hostname = socket.getfqdn()
    dir_name = ".".join([user, hostname, str(pid)])
    return mkpath(_basedir(), 'hod', dir_name)

def mkpathabs(filepath, working_dir):
    '''
    Take a filepath and working_dir and return the absolute path for the
    filepath. If the filepath is already absolute then just return it.
    '''
    if filepath[0] == '/': # filepath is already absolute
        return filepath

    return realpath(mkpath(working_dir, filepath))
    
def _fileobj_dir(fileobj):
    if hasattr(fileobj, 'name'):
        return dirname(fileobj.name)
    return ''
    
def _parse_runs_on(s):
    '''True if master; False if slave. Error otherwise.'''

    if s.lower() == 'master':
        return True
    elif s.lower() == 'slave':
        return False
    else:
        raise RuntimeError('runs-on field must be either "master" or "slave".')

def _parse_comma_delim_list(s):
    '''
    Convert a string containing a comma delimited list into a list of strings
    with no spaces on the end or beginning.
    '''
    return [x.strip() for x in s.split(',')]


class PreServiceConfigOpts(object):
    r"""
    Manifest file for the group of services responsible for defining service
    level configs which need to be run through the template before any services
    can begin.
    """
    def __init__(self, fileobj):
        _config = load_service_config(fileobj)
        self.version = _config.get(_META_SECTION, 'version')
        self.basedir = _mkhodbasedir()
        self.configdir = mkpath(self.basedir, 'conf')

        fileobj_dir = _fileobj_dir(fileobj)
        def _fixup_path(cfg):
            config_file = mkpathabs(cfg, fileobjdir)

        self.config_files = _parse_comma_delim_list(_config.get(_CONFIG_SECTION, 'config-files'))
        self.config_files = [_fixup_path(cfg) for cfg in self.config_files]


class ConfigOpts(object):
    r"""
    Wrapper for the service configuration.
    Each of the config values can have a $variable which will be replaces
    by the value in the template strings except 'name'. Name cannot be
    templated.
    """
    __slots__ = ['name', 'runs_on_master', 'start_script', 'stop_script', 'env',
            'config_file', 'basedir', 'configdir']

    def __init__(self, fileobj):
        _config = load_service_config(fileobj)
        self.name = _config.get(_UNIT_SECTION, 'name')
        self.runs_on_master = _parse_runs_on(_config.get(_UNIT_SECTION, 'runs-on'))

        _r = partial(resolve_config_str)
        self.start_script = _r(_config.get(_EXEC_SECTION, 'start-script'))
        self.stop_script = _r(_config.get(_EXEC_SECTION, 'stop-script'))

        self.env = OrderedDict([(k, _r(v)) for k, v in _config.items(_ENVIRONMENT_SECTION)])
        self.basedir = _mkhodbasedir()
        self.configdir = mkpath(self.basedir, 'conf')

    def setenv(self):
        for k,v in self.env.items():
            os.environ[k] = v