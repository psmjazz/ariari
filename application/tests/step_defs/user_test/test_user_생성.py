from application.models.user import User
from application.schemata.user import UserSchema
from pytest_bdd import scenario, given, when, then, parsers
import pytest


user_schema = UserSchema()


@pytest.fixture
def user():
    user = User(google_id="khtks@naver.com", en_name="Sam", ko_name="Kong", admin=False)
    return user


# Scenario 1

@scenario('../../features/user/user_생성.feature', '캘린더가 공유될 때, User info 입력 및 정상 생성')
def test_user_생성():
    pass


@pytest.mark.skip(reason="현재는 테스트 불가")
@given("캘린더가 공유되었고, user의 정보가 db에 없다")
def no_user_in_db(session):
    pass


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 값을 넘겨줄 때"))
def request_uri(client, user, uri, session):
    response = client.post(uri, data=user_schema.dump(user))
    data = user_schema.load(response.json, session=session)
    print(response)

    assert response.status_code == 201
    yield data


@then("user가 생성되고, 정보가 저장된다")
def create_user_info(request_uri):
    assert User.query.get(request_uri.id)


# Scenario 2

@pytest.mark.xfail(strict=True)
@scenario('../../features/user/user_생성.feature', 'User의 정보 중복으로 인한 생성 불가')
def test_중복생성_실패():
    pass


@given("DB에 user의 정보가 존재한다")
def user_is_in_db(client, user):
    try:
        assert User.query.all()
    except:
        response = client.post('user-info/', data=user_schema.dump(user))
        assert response.status_code == 201


@when(parsers.parse("중복되는 값으로 {uri}에 요청할 때"))
def duplicate_values(client, user, uri):
    response = client.post(uri, data=user_schema.dump(user))


@then("중복된 값으로 인해 user 생성 불가")
def error_caused_by_duplicate():
    pass


# Scenario 3

@pytest.mark.xfail(strict=True)
@scenario('../../features/user/user_생성.feature', 'User의 attribute의 조건 위배로 안한 생성 불가')
def test_조건위배_생성_실패():
    pass


@given("일반 사용자의 계정이어야 한다")
def general_user(session):
    user = session.query(User).filter(User.admin == False).first()
    assert user

    return user


@given("user를 구성하는 attribute에 조건이 있다")
def attribute_constraint():
    assert User


@when(parsers.parse("attribute의 조건에 위배하는 값으로 {uri}에 요청을 보낼 때"))
def unconstrained_user(client, user, uri):
    user.ko_name = "겁나 긴 이름입니다"

    response = client.post(uri,  data=user_schema.dump(user))


@then("attribute의 조건 위배로 인해 user 생성 불가")
def error_caused_by_unconstrained_user():
    pass