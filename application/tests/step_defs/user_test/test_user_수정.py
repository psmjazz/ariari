from pytest_bdd import scenario, given, when, then, parsers
from application.models.user import User
from application.schemata.user import UserSchema
import pytest
import random

user_schema = UserSchema()


# Background

@given("일반 사용자가 DB에 있어야 한다")
def general_user(session):
    try:
        general_user = User.query.filter_by(admin=False).first()
        assert general_user

    except BaseException:
        general_user = User(google_id="konghs@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        general_user.google_id = str(random.randint(1, 9)) + "_" + general_user.google_id
        session.add(general_user)
        session.commit()

    return general_user


@given("관리자가 DB에 있어야 한다")
def admin_user(session):
    try:
        admin_user = User.query.filter_by(admin=True).first()
        assert admin_user

    except BaseException:
        admin_user = User(google_id="khtks@naver.com", en_name="Sam", ko_name="Kong", admin=True)
        admin_user.google_id = str(random.randint(1, 9)) + "_" + admin_user.google_id
        session.add(admin_user)
        session.commit()

    return admin_user


# Scenario 1

@scenario('../../features/user/user_수정.feature', 'user 정보 수정')
def test_사용자_정보_수정():
    pass


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 수정할 사용자의 id와 수정할 값을 넘겨준다"))
def modify_user_info(client, admin_user, general_user, uri, session):
    uri = uri + str(general_user.id)
    response = client.put(uri, data=dict(id = admin_user.id, google_id="google_id", ko_name="ko_name", en_name="en_name", admin=1, entry_date='2018-12-14'))

    assert response.status_code == 200
    yield user_schema.load(response.json, session=session)


@then("지정한 user의 정보가 변경된다")
def modified_user(modify_user_info):
    assert modify_user_info.google_id == "google_id"
    assert modify_user_info.en_name == "en_name"
    assert modify_user_info.ko_name == "ko_name"
    assert modify_user_info.admin == 1


# Scenario 2

@scenario('../../features/user/user_수정.feature', '자신의 정보 수정')
def test_자신의_정보_수정():
    pass


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 넘겨준 id가 본인의 id와 일치하는 경우"))
def modify_own_info(client, uri, session, admin_user):
    uri = uri + str(admin_user.id)
    response = client.put(uri, data=dict(id=admin_user.id, google_id="own_id", ko_name="ko_name", en_name="en_name", admin=0))

    assert response.status_code == 200
    print(user_schema.load(response.json, session=session))
    yield user_schema.load(response.json, session=session)


@then("자신의 user의 정보가 변경된다")
def modified_user(modify_own_info):
    assert modify_own_info.google_id == "own_id"
    assert modify_own_info.en_name == "en_name"
    assert modify_own_info.ko_name == "ko_name"
    assert modify_own_info.admin == 0


# Scenario 3

@scenario('../../features/user/user_수정.feature', '수정할 user가 관리자인 경우 수정 불가')
def test_관리자_수정_실패():
    pass


@given("사용자가 관리자이다")
def admin(admin_user):
    assert admin_user.admin == True


@given("DB에 관리자가 2명 이상이다")
def another_admin(client, session):
    response = client.post('/users/', data=dict(google_id="g_id", en_name="ename", admin=1))

    assert len(User.query.filter_by(admin=True).all()) >= 2
    return user_schema.load(response.json, session=session)


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 수정할 관리자의 user의 id와 수정할 값을 넘겨준다"))
def modify_admin_user(client, uri, session, admin_user, another_admin):
    uri = uri + str(admin_user.id)
    response = client.put(uri, data=dict(id=another_admin.id, google_id="modify_google", en_name="modify_name", admin=0))

    yield response


@then("정보 수정이 실패한다")
def modify_fail(modify_admin_user):
    assert modify_admin_user.status_code == 400


# Scenario 4

@scenario('../../features/user/user_수정.feature', '일반 사용자가 admin을 수정하려는 경우 실패')
def test_일반사용자_admin_수정_실패():
    pass


@given("사용자가 일반 사용자이다")
def general(general_user):
    assert general_user.admin == False


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 사용자가 자신의 admin을 수정하려고 할 때"))
def modify_own_admin(client, uri, session, general_user):
    uri = uri + str(general_user.id)
    response = client.put(uri, data=dict(id=general_user.id, google_id="modify_google", en_name="adj_name", admin=1))

    yield response


@then("권한이 없으르모 정보 수정이 실패한다")
def modify_admin_fail(modify_own_admin):
    assert modify_own_admin.status_code == 401


# Scenario 5

@pytest.mark.xfail(strict=True)
@scenario('../../features/user/user_수정.feature', 'DB의 조건을 위배해 수정 불가')
def test_조건위배_수정_실패():
    pass


@when(parsers.parse("올바른 {uri}에 조건을 위배하는 값을 넘겨줄 때"))
def unconstrained_value(client, session, uri, general_user, admin_user):

    uri = uri + str(general_user.id)
    response = client.put(uri, data=dict(id=admin_user.id, google_id="modified_google_id", en_name="modified_en_name", ko_name="test_name", admin=1))

    assert response
    print(User.query.all())


@then("DB의 조건을 위배해 수정 불가")
def unconstrained_value_fail():
    pass
