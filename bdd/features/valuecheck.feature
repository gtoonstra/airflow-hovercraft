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

Feature: ValueCheckOperator
  The value check operator performs quick data quality checks against a database.

  Scenario: ValueCheckOperator can be created
    Given no specific state
    And a specific initializer
    | sql      | conn_id | pass_value |
    | fake_sql | fake    |  1.0       |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then no exception is raised

  Scenario: ValueCheckOperator returns good result
    Given hook mocked with FakeNoneHook
    And a specific initializer
    | sql      | conn_id | pass_value |
    | fake_sql | fake    |  None      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised

  Scenario: ValueCheckOperator raises exception on False
    Given hook mocked with FalseHook
    And a specific initializer
    | sql      | conn_id | pass_value |
    | fake_sql | fake    |  False     |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator can deal with multiple true's
    Given hook mocked with MultiTrueHook
    And a specific initializer
    | sql      | conn_id | pass_value |
    | fake_sql | fake    |  True      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator raises exception when None is returned
    Given hook mocked with Fake42Hook
    And a specific initializer
    | sql      | conn_id | pass_value |
    | fake_sql | fake    |  42.0      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised
