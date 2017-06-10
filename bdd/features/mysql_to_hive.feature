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

Feature: MySqlToHiveTransfer
  Verify the operator processes data correctly when transferring mysql to hive

  Scenario: MySqlToHiveTransfer can be created
    Given mysql hook mocked out
    And hivecli hook mocked out
    And a specific initializer
    | sql   | hive_table    |
    | "any" | "destination" |
    When the airflow.operators.mysql_to_hive.MySqlToHiveTransfer is created
    Then no exception is raised

  Scenario: MySqlToHiveTransfer can execute
    Given mysql hook mocked out
    And hivecli hook mocked out
    And a specific initializer
    | sql                  | hive_table    |
    | "testdata/input.csv" | "destination" |
    When the airflow.operators.mysql_to_hive.MySqlToHiveTransfer is created
    Then the operator is executed
    And no exception is raised
