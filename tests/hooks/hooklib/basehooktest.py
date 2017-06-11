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

import unittest
import time
from .dockermanager import DockerManager


class BaseHookTest(unittest.TestCase):
    def __init__(self, 
                 docker_image_name, 
                 container_name, 
                 environment, 
                 ports, 
                 *args, 
                 **kwargs):
        super(BaseHookTest, self).__init__(*args, **kwargs)
        self.docker_manager = DockerManager(docker_image_name, 
                                            container_name,
                                            environment,
                                            ports)

    def setUp(self):
        super(BaseHookTest, self).setUp()
        self.docker_manager.refresh()
        # The docker container takes a while to start, so wait 10s before
        # trying anything
        time.sleep(20)
