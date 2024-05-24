Feature: test

@test
Scenario: test
    Given i navigate to the Welcome page 
    Then admin button should be visible

@test1
Scenario: test
    Given i navigate to the Welcome page
    When i click to admin button
    Then user management section is visible