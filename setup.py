# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

import imp
import logging
import os
import pip
import sys

logger = logging.getLogger(__name__)

# Kept manually in sync with airflow.__version__
version = imp.load_source(
    'airflow-hovercraft.version', os.path.join('airflow-hovercraft', 'version.py')).version


class Tox(TestCommand):
    user_options = [('tox-args=', None, "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(args=self.tox_args.split())
        sys.exit(errno)


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


def git_version(version):
    """
    Return a version to identify the state of the underlying git repo. The version will
    indicate whether the head of the current git-backed working directory is tied to a
    release tag or not : it will indicate the former with a 'release:{version}' prefix
    and the latter with a 'dev0' prefix. Following the prefix will be a sha of the current
    branch head. Finally, a "dirty" suffix is appended to indicate that uncommitted changes
    are present.
    """
    repo = None
    try:
        import git
        repo = git.Repo('.git')
    except ImportError:
        logger.warning('gitpython not found: Cannot compute the git version.')
        return ''
    except Exception as e:
        logger.warning('Git repo not found: Cannot compute the git version.')
        return ''
    if repo:
        sha = repo.head.commit.hexsha
        if repo.is_dirty():
            return '.dev0+{sha}.dirty'.format(sha=sha)
        # commit is clean
        # is it release of `version` ?
        try:
            tag = repo.git.describe(
                match='[0-9]*', exact_match=True,
                tags=True, dirty=True)
            assert tag == version, (tag, version)
            return '.release:{version}+{sha}'.format(version=version,
                                                     sha=sha)
        except git.GitCommandError:
            return '.dev0+{sha}'.format(sha=sha)
    else:
        return 'no_git_version'


def write_version(filename=os.path.join(*['airflow-hovercraft',
                                          'git_version'])):
    text = "{}".format(git_version(version))
    with open(filename, 'w') as a:
        a.write(text)


def do_setup():
    write_version()
    setup(
        name='airflow-hovercraft',
        description='Reference implementation for airflow hooks and operators',
        license='Apache License 2.0',
        version=version,
        packages=find_packages(),
        package_data={'': ["airflow-hovercraft/git_version"]},
        include_package_data=True,
        zip_safe=False,
        scripts=[],
        install_requires=[
            'apache-airflow >= 1.8.1',
        ],
        extras_require={
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.4',
            'Topic :: System :: Monitoring',
        ],
        author='gtoonstra',
        author_email='',
        url='https://github.com/gtoonstra/airflow-hovercraft/',
        cmdclass={
            'test': Tox,
            'extra_clean': CleanCommand,
        },
    )


if __name__ == "__main__":
    do_setup()
