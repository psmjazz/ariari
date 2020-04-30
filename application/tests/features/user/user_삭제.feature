Feature: User info API
  Application 사용자가 다른 user의 삭제를  요청했을 때,
  user_info db에서 user info를 삭제하고 올바른 값을 반환한다

  Background: user의 삭제는 관리자만 가능하다

  Scenario Outline: 사용자 삭제
    Given 현재 사용자가 관리자이다
    Given 관리자 이외의 user가 db에 있다
    When 올바른 {uri}에 삭제할 id를 넘겨 주었을 때
    Then user가 삭제된다

    Examples:
      | uri        |
      | users/     |


  Scenario Outline: 사용자가 관리자가 아니면 삭제 거부
    Given 현재 사용자가 관리자가 아니다
    When 올바른 {uri}에 삭제할 id을 넘겨 주었을 때
    Then user의 삭제가 거부된다

    Examples:
      | uri        |
      | users/     |


  Scenario Outline: 삭제하려는 user가 없는 경우 삭제 실패
    Given 현재 사용자가 관리자이다
    When 올바른 {uri}에 삭제할 id을 넘겨 주면
    Then user가 없으므로 삭제 실패

    Examples:
      | uri        |
      | users/     |


  Scenario Outline: 삭제하려는 user가 관리자일 경우 삭제 실패
    Given 관리자가 2명 이상이다
    When 올바른 {uri}에 삭제할 관리자의 id을 넘겨 주었을 때
    Then 삭제할 대상이 관리자 이므로 삭제 실패

    Examples:
      | uri        |
      | users/     |




