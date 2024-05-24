Feature: test

@test
Scenario: test
    Given i navigate to the Admin page 
    Then admin button should be visible

@test1
Scenario: test
    Given i navigate to the Admin page
    When i click to admin button
    Then admin page is visible