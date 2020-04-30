# vacation_management

1)	**프로젝트 소개**
    - 사용자가 공유된 구글 캘린더에 등록한 휴가를 읽어와 DB에 등록하고, 
      사용자의 남은 휴가나 사용한 휴가를 확인할 수 있는 프로그램을 만드는 것

2)	**사용한 프레임워크와 라이브러리**
    1.	Flask
        - python의 웹 프레임워크
    2.	Flask-sqlalchemy 
        - flask에서 ORM을 이용하기 위한 라이브러리
    3.	Mysql, Mysqlclient 
        - python에서 mysql과 연동하여 db를 사용하기 위한 라이브러리
    4.	Flask-marshmallow, Marshmallow-sqlalchemy 
        - flask와 sqlalchemy에서 serialize와 deserialize를 사용하기 위한 라이브러리 / marshmallow-sqlalchemy를 이용하면 sqlalchemy model을 
          이용해 schema를 만들 수 있다
    5.	Flask-migrate 
        - flask에서 migration을 사용하기 위한 라이브러리
    6.	Flask-restful 
        - flask에서 restful api를 좀 더 손쉽게 만들기 위한 라이브러리
    7.	Pytest, Pytest-bdd 
        - python에서 테스트를 진행할 수 있도록 도와주는 라이브러리 / pytest-bdd는 pycharm에서 공식적으로 지원해
          주기 때문에, 좀 더 손쉽게 시나리오를 만들어 bdd를 진행할 수 있다.
    8.	Google, Google-outh 등 
        - google oauth와 google api를 이용하기 위한 라이브러리
    9.	Pyopenssl
        - python에서 ssl을 이용하기 위한 라이브러리

3)	**초기 스팩**
    1.	공통(일반 사용자, 관리자)
        - 구글 소셜 로그인으로 사용자 인증
        - 사용자 등록(자신의 정보 등록)
        - 자신의 남은 휴가 확인
        - 자신이 사용한 휴가 확인
        - 일정한 시간마다 휴가를 동기화해 DB에 저장
    2.	관리자
        - 다른 사용자 CRUD
        - 다른 사용자의 사용한 휴가, 남은 휴가를 확인 가능하다

4)	**현재 구현 기능**
    1.	구글 소셜 로그인을 통해 사용자 인증 
        - 인증 후 google id를 이용해 DB를 확인하여 등록된 사용자가 아닐 경우 정보를 입력하게 한다
        - 사용자가 user 테이블에 등록되게 되면, 자동으로 남은 휴가를 계산하여 남은 휴가 테이블에 등록되게 된다
    2.	현재 사용자가 관리자인지 확인하여 사용 가능한 기능을 나눈다
        - 일반 사용자 : 자신의 정보를 등록 및 확인할 수 있고, 사용한 휴가와 남은 휴가를 확인 가능하다
        - 관리자 : 일반 사용자와 동일한 기능을 모두 사용할 수 있고, 추가적으로 다른 사람의 정보와 사용한 휴가, 
                  남은 휴가를 확인 가능하다
    3.  휴가 동기화를 누르게 되면, 자동으로 지정한 google 캘린더에서 event를 읽어와 테이블에 저장되어 있는 휴가와 싱크를 맞추게 되고, 
        변동이 있다면 사용자의 휴가도 다시 계산하게 된다.

5)	**아쉬운 점**
    1.	서버나 네트워크 및 사용했던 라이브러리에 대한 기초 지식이 미흡하여, 초반에 작업을 시작하는 단계에서 시간이 오래 걸렸다.
    2.	http form filed에서는 put이나 delete method를 제공하지 않아서, 초기에 rest api를 적용했을 때 html을 베이스로 쓰는 flask의 jinja   
        template으로는 put과 delete를 사용하지 못하는 문제점이 있었다.
    3.	Front end는 python의 웹 프레임워크인 flask에서 기본적으로 사용하는 jinja template만 사용하였는데, 간단한 기능들을 시연할 때에는 
        큰 불편함이 없었지만, 실제 사용자가 사용하기에는 매끄럽지 못한 것 같다.
    4.	실력부족으로 프로젝트를 제때 마지치 못하여 배포까지는 해보지 못한 점이 아쉽다.

6)	**개선 방향**
    1.	Jinja template이 아닌 부트스트랩이나 플렉스를 이용하여 좀 더 사용하기 쉽게 front end를 바꿔보고 싶다.
    2.	Query의 중복사용이나 레거시 코드들을 수정하여 보완하고 싶다.
    3.	서버와 네크워크를 통해 통신할 필요 없이 로직으로만 처리 가능하여 api를 만들지 않아도 되는 부분은 service 단위로 변경해 보고 싶다
