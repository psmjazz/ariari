Feature: User API
  Application 사용자가 정보를 요청했을 때,
  올바른 정보를 반환해줘야 한다.

  Scenario Outline: 관리자가 전체 user 검색
    Given DB에 user들이 있어야 한다
    When 올바른 {uri}에 요청했을 때
    Then 전체 user 정보가 결과로 나온다
    Examples:
      | uri    |
      | users/ |


  Scenario Outline: 관리자가 특정 user 검색
    Given 관리자의 계정이어야 한다
    When 올바른 {uri}에 요청했을 때
    Then 특정 user의 정보가 결과로 나온다
    Examples:
      | uri    |
      | users/ |


  Scenario Outline: 일반 사용자가 자신의 user 정보 검색
    Given DB에 user의 정보가 있어야 하고
    Given 일반 사용자의 계정이어야 한다
    When 올바른 {uri}에 자신의 정보를 요청했을 때
    Then 자신의 정보가 결과로 나온다
    Examples:
      | uri    |
      | users/ |


  Scenario Outline: 일반 사용자가 다른 사람의 user 정보 검색
    Given 일반 사용자의 계정이어야 하고
    Given DB에 자신과 다른 user가 있어야 한다.
    When 올바른 {uri}에 다른 사람의 user 정보를 요청했을 때
    Then 권한이 없으므로 검색에 실패하게 되고, status code 400이 반환된다
    Examples:
      | uri     |
      | users/  |
      | users/3 |



  Scenario Outline: DB에 user가 없어서 검색 불가
    Given DB에 사용자가 존재하지 않는다
    When {uri}에 user의 정보 검색을 요청했을 때
    Then DB에 user가 없으므로 검색이 불가능하다
    Examples:
      | uri          |
      | users/  |
      | users/1 |

