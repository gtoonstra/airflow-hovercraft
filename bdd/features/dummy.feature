Feature: DummyOperator
  The dummy operator serves no real purpose in airflow, except
  to verify that an operator is schedulable and executable.

  Scenario: DummyOperator can be created
    Given no special preconditions
    When the hovercraft.operators.dummy_operator.DummyOperator is created
    Then it does not raise an exception
