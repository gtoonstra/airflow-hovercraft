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

Feature: CheckOperator
  The check operator performs quick data quality checks against a database.

  Scenario: CheckOperator can be created
    Given no specific state
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then no exception is raised

  Scenario: CheckOperator returns good result
    Given hook mocked with TrueHook
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: CheckOperator raises exception on False
    Given hook mocked with FalseHook
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised

  Scenario: CheckOperator can deal with multiple true's
    Given hook mocked with MultiTrueHook
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: CheckOperator raises exception when one value is False
    Given hook mocked with FakeMultiTrueOneFalseHook
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised

  Scenario: CheckOperator raises exception when None is returned
    Given hook mocked with FakeNoneHook
    And a specific initializer
    | sql      | conn_id |
    | fake_sql | fake    |
    When the airflow.operators.check_operator.CheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised
