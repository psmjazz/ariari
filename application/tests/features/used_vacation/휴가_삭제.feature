Feature: used_vacation API
  사용자가 등록했던 휴가를 취소하거나 관리자가 임의로 삭제하려고 하는 경우,
  DB에 등록된 휴가를 삭제한다


Scenario: 등록되어있던 휴가를 취소하면 휴가 삭제
  Given google calendar에 등록되어 있는 휴가가 있다
  When 등록된 휴가를 삭제하는 경우
  Then used_vacation DB에서 삭제한다


Scenario: 관리자가 일반사용자가 등록한 휴가를 삭제
  Given 현재 사용자가 관리자이다
  Given DB에 일반 사용자의 등록된 휴가가 있다
  When 관리자가 일반 사용자가 등록한 휴가를 삭제할 때
  Then 특정 사용자의 사용 휴가 정보가 DB에서 삭제된다


Scenario: 일반 사용자가 다른 사용자의 휴가 삭제
  Given 현재 사용자가 일반 사용자이다
  Given DB에 다른 사용자의 등록된 휴가가 있다
  When 일반 사용자가 다른 사용자의 휴가를 삭제할 때
  Then 권한이 없으므로 삭제가 실패한다