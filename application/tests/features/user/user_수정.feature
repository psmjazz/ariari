Feature: User info API
  Application 사용자가 User의 수정를  요청했을 때,
  user db에서 요청한 user의 정보를를 수정하고 올바른 값을 반환한다

  Background: 관리자만 다른 사용자의 정보를 수정 가능하다
    Given 일반 사용자가 DB에 있어야 한다
    Given 관리자가 DB에 있어야 한다

  Scenario Outline: user 정보 수정
    When 올바른 {uri}에 수정할 사용자의 id와 수정할 값을 넘겨준다
    Then 지정한 user의 정보가 변경된다

    Examples:
      | uri    |
      | users/ |


  Scenario Outline: 자신의 정보 수정
    When 올바른 {uri}에 넘겨준 id가 본인의 id와 일치하는 경우
    Then 자신의 user의 정보가 변경된다

    Examples:
      | uri    |
      | users/ |


  Scenario Outline: 수정할 user가 관리자인 경우 수정 불가
    Given 사용자가 관리자이다
    Given DB에 관리자가 2명 이상이다
    When 올바른 {uri}에 수정할 관리자의 user의 id와 수정할 값을 넘겨준다
    Then 정보 수정이 실패한다
    Examples:
     | uri    |
     | users/ |



  Scenario Outline: 일반 사용자가 admin을 수정하려는 경우 실패
    When 올바른 {uri}에 사용자가 자신의 admin을 수정하려고 할 때
    Then 권한이 없으르모 정보 수정이 실패한다

    Examples:
     | uri    |
     | users/ |


  Scenario Outline: DB의 조건을 위배해 수정 불가
    When 올바른 {uri}에 조건을 위배하는 값을 넘겨줄 때
    Then DB의 조건을 위배해 수정 불가

    Examples:
      | uri    |
      | users/ |