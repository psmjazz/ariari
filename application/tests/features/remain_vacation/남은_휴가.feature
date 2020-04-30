Feature: remain vacation API
  사용자가 google calendar에 휴가를 등록하여 used vacation db에 휴가가 등록된 경우,
  자동으로 remain vacation의 남은 휴가를 계산해 준다


Scenario: 사용자 등록
  Given remain vacation db가 존재한다
  Given 사용자의 정보가 user DB에 있다
  Then 사용자의 남은 휴가 정보가 reamin vacation db에 등록된다


Scenario: used vacation에 휴가가 등록되면 남은 휴가 자동 계산
  Given db에 사용자의 정보가 저장되어 있다
  When used vacation에 휴가가 등록될 때
  Then remain vacation의 남은 휴가가 수정된다


Scenario: 남은 휴가 검색
  Given 현재 db에 사용자가 있다
  Given 현재 사용자가 관리자이다
  When 남은 휴가 검색을 요청했을 때
  Then remain vacation의 남은 휴가가 검색된다


Scenario: 일반 사용자의 다른 사람의 휴가 검색 실패
  Given 현재 db에 사용자가 있다
  Given 현재 사용자가 일반 사용자이다
  When 다른 사람의 남은 휴가 검색을 요청할 때
  Then 권한이 없어서 검색에 실패한다


Scenario: 사용자 정보 수정
  Given 현재 db에 사용자가 있다
  When user db에서 사용자의 정보가 수정될 때
  Then 해당 user의 remain vacation 정보도 수정된다


Scenario: 사용자 삭제
  Given 현재 db에 사용자가 있다
  When user db에서 사용자가 삭제될 때
  Then 해당 user의 remain vacation 정보도 삭제된다




