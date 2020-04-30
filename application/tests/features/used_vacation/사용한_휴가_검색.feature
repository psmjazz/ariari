Feature: used_vacation API
  사용자가 사용한 휴가를 검색할 때,
  올바른 결과와 코드를 반환한다


Scenario: 사용자가 자신이 사용한 휴가 검색
  Given DB에 사용자와 휴가 기록이 있다
  When 사용자가 자신이 사용한 휴가 검색
  Then 사용자의 휴가가 반환된다


Scenario Outline: 관리자가 다른 사용자의 휴가 검색
  Given 현재 사용자가 관리자이다
  When {uri}에 요청하여다른 사용자의 휴가를 검색할 경우
  Then 검색한 사용자의 휴가가 반환된다

  Examples:
    | uri                      |
    | /users/vacations/used   |
#    | /users/vacations/3/used |


Scenario: 일반 사용자가 다른 사람의 휴가를 검색할 경우 실패
  Given 현재 사용자가 일반 사용자이다
  When 다른 사용자의 휴가를 검색할 경우
  Then 권한이 없으므로 검색 실패

