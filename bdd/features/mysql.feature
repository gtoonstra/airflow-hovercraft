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

Feature: MySqlOperator
  The mysql operator check verifies the function of the MySql Operator
  (not the mysql hook).

  Scenario: MySqlOperator can be created
    Given mysql hook mocked out
    And a specific initializer
    | sql   |
    | "any" |
    When the airflow.operators.mysql_operator.MySqlOperator is created
    Then no exception is raised

  Scenario: MySqlOperator can be created
    Given mysql hook mocked out
    And a specific initializer
    | sql                  | 
    | "SELECT 1 FROM TEST" |
    When the airflow.operators.mysql_operator.MySqlOperator is created
    Then the operator is executed
    And no exception is raised
