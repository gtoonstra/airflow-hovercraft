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

Feature: BashOperator
  The bash operator executes a bash command or a script.

  Scenario: BashOperator can be created
    Given a specific initializer
    | bash_command  |
    | echo 1        |
    When the airflow.operators.bash_operator.BashOperator is created
    Then no exception is raised

  Scenario: When xcom_push is set, it returns value of last line
    Given a specific initializer
    | bash_command  |  xcom_push |
    | echo 1        |  True      |
    When the airflow.operators.bash_operator.BashOperator is created
    Then the operator is executed
    Then no exception is raised
