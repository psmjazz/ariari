Feature: Google Calendar API
  API를 application에 적용할 때, 환경이 올바르게 설정되어 있는지 확인

#
#  Scenario: credential key가 올바르지 않는 경우 권한이 없어서 실패
#    Given 잘못된 credentail key를 가지고 있다
#    When Google calendar api를 사용하려고 할 때
#    Then credential key가 잘못 되었으므로 실패한다

#
#  Scenario: service를 올바르게 설정하지 않은 경우, service를 build하지 못해서 실패
#    Given 올바른 scope와 cedentail key값을 가지고 있다
#    When 잘못된 service를 build하려고 할 때
#    Then service가 잘못됐으므로 실패
