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

import docker
import logging


SECRET_PW = 'secret'
FORMAT = '%(asctime)-15s %(message)s'

logging.basicConfig(format=FORMAT, level=logging.INFO)


class DockerManager(object):
    def __init__(self, image_name, container_name, environment, ports):
        self.logger = logging.getLogger(__name__)
        self.image_name = image_name
        self.container_name = container_name
        self.environment = environment
        self.client = docker.from_env(version='auto')
        self.ports = ports

    def stop_container(self):
        container_list = self.client.containers.list()
        for container in container_list:
            if container.attrs['Config']['Image'] == self.image_name:
                self.logger.info("Stopping and removing {0}".format(container))
                container.remove(force=True)

    def pull_container(self):
        self.logger.info("Pulling {0}".format(self.image_name))
        image = self.client.images.pull(self.image_name)

    def run_container(self):
        self.logger.info("Starting container {0}".format(self.image_name))
        container = self.client.containers.run(
            image=self.image_name,
            detach=True,
            environment=self.environment,
            name=self.container_name,
            ports=self.ports)

    def refresh(self):
        self.stop_container()
        self.pull_container()
        self.run_container()
