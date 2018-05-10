
import os
from collections import namedtuple

from .environment import EnvVars
from .utils import (
    get_project_name,
    get_project_dir_filepath,
    collapse_path,
)

Environment = namedtuple('Environment', [
    'envpath',
    'envname',
    'project_name',
    'binpath',
    'short_envpath',
    ])


def find_environments(pipenv_home):
    """
    Returns Environment NamedTuple created from list of folders found in the
    Pipenv Environment location
    """
    environments = []
    for folder_name in sorted(os.listdir(pipenv_home)):
        envpath = os.path.join(pipenv_home, folder_name)
        project_name = get_project_name(envpath)
        if not project_name:
            continue
        binpath = find_binary(envpath)
        environment = Environment(project_name=project_name,
                                  envpath=envpath,
                                  envname=folder_name,
                                  binpath=binpath,
                                  short_envpath=collapse_path(envpath),
                                  )
        environments.append(environment)
    return environments


def find_binary(envpath):
    env_ls = os.listdir(envpath)
    if 'bin' in env_ls:
        path = os.path.join(envpath, 'bin')
    elif 'Scripts' in env_ls:
        path = os.path.join(envpath, 'Scripts')
    binpath = os.path.join(path, 'python')
    if os.path.exists(binpath):
        return binpath
    else:
        raise Environment('could not find python binary: {}'.format(envpath))


###############################
# Project Dir File (.project) #
###############################

def read_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def write_project_dir_project_file(envpath, project_dir):
    project_file = get_project_dir_filepath(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def delete_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file
