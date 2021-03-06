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

Feature: DummyOperator
  The dummy operator serves no real purpose in airflow, except
  to verify that an operator can be scheduled and is executable.

  Scenario: DummyOperator can be created
    Given no specific state
    When the airflow.operators.dummy_operator.DummyOperator is created
    Then the operator is executed
    And no exception is raised
