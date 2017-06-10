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
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  1.0       |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then no exception is raised

  Scenario: ValueCheckOperator cannot deal with None result
    Given hook mocked with FakeHook
    | value  |
    | None   |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  None      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised

  Scenario: ValueCheckOperator can deal with False result
    Given hook mocked with FakeHook
    | value   |
    | (False,) |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  False     |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator can deal with True result
    Given hook mocked with FakeHook
    | value             |
    | (True,True,True,) |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  True      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator can deal with float result
    Given hook mocked with FakeHook
    | value   |
    | (42.0,) |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  42.0      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator can deal with result within tolerance
    Given hook mocked with FakeHook
    | value   |
    | (42.0,) |
    And a specific initializer
    | sql        | conn_id   | pass_value | tolerance |
    | "fake_sql" | "fake"    |  41.991    |  0.001    |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator raises exception on value outside tolerance
    Given hook mocked with FakeHook
    | value   |
    | (42.0,) |
    And a specific initializer
    | sql        | conn_id   | pass_value | tolerance |
    | "fake_sql" | "fake"    |  42.991    |  0.001    |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised

  Scenario: ValueCheckOperator can deal with multiple return values
    Given hook mocked with FakeHook
    | value             |
    | (42.0,42.0,42.0,) |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    |  42.0      |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator can deal with string result
    Given hook mocked with FakeHook
    | value      |
    | ("hello",) |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    | "hello"    |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then no exception is raised

  Scenario: ValueCheckOperator raises exception when None is returned
    Given hook mocked with FakeHook
    | value  |
    | None   |
    And a specific initializer
    | sql        | conn_id   | pass_value |
    | "fake_sql" | "fake"    | "hello"    |
    When the airflow.operators.check_operator.ValueCheckOperator is created
    Then the operator is executed
    Then the exception AirflowException is raised
