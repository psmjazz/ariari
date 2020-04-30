Feature: used_vacation API
  다른 사용자들이 Google calendar에 등록한 휴가들을 읽어와
  used_vacation db에 등록한다

Background:
  Given Google social login이 되어있다


Scenario: 휴가 등록하기
  Given used_vacation DB가 존재한다
  Given user의 정보가 DB에 존재한다.
  When 새로운 휴가가 등록되었을 때
  Then used_vacation db에 휴가를 등록한다


Scenario: event의 creator email이 User DB에 없는 경우 휴가 등록 실패
  When event의 creator와 일치하는 user가 db에 없는 경우
  Then user가 없으므로 휴가 생성 불가

