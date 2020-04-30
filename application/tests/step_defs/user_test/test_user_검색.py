from application.models.user import User
from application.schemata.user import UserSchema
from pytest_bdd import scenario, given, when, then, parsers
import pytest
import random

user_schema = UserSchema()


@pytest.fixture
def user(session):
    user = User(google_id="khtks@naver.com", en_name="Sam", ko_name="Kong", admin=True)
    return user


# Scenario 1

@scenario('../../features/user/user_검색.feature', '관리자가 전체 user 검색')
def test_전체_사용자_검색():
    pass


@given("DB에 user들이 있어야 한다")
def users_are_in_db(client, user, session):
    for i in range(3):
        user.google_id = str(random.randint(1, 9)) + "_" + user.get_google_id()
        user.en_name = str(random.randint(1, 9)) + "_" + user.get_en_name()
        user.admin = not user.admin
        client.post('users/', data=user_schema.dump(user))
    assert User.query.all()


@pytest.fixture
@when(parsers.parse("올바른 {uri}에 요청했을 때"))
def request_uri_all(client, uri):
    user = User.query.filter_by(admin=True).first()
    response = client.get(uri, data=dict(id=user.id))

    assert response.status_code == 200
    return response


@then("전체 user 정보가 결과로 나온다")
def all_user(request_uri_all):
    assert request_uri_all.json


# Scenario 2

@scenario('../../features/user/user_검색.feature', '관리자가 특정 user 검색')
def test_특정_사용자_검색():
    pass


@given("DB에 user가 있어야 한다")
def user_is_in_db():
    user_in_db = User.query.first()
    assert user_in_db
    return user_in_db


@given("관리자의 계정이어야 한다")
def admin_user():
    user = User.query.filter_by(admin=True).first()

    assert user.admin == 1
    return user


@pytest.yield_fixture
@when(parsers.parse("올바른 {uri}에 요청했을 때"))
def request_uri_specific(client, admin_user, user_is_in_db, uri, session):
    uri = uri + str(user_is_in_db.id)

    response = client.get(uri, data=dict(id=admin_user.id))
    data = user_schema.load(response.json, session=session)

    assert response.status_code == 200
    yield data


@then("특정 user의 정보가 결과로 나온다")
def specific_user(request_uri_specific):
    assert User.query.get(request_uri_specific.id)


# Scenario 3

@scenario('../../features/user/user_검색.feature', '일반 사용자가 자신의 user 정보 검색')
def test_일반_사용자가_자신의_정보_검색():
    pass


@given("DB에 user의 정보가 있어야 하고")
def user_in_db():
    users = User.query.all()
    assert users


@given("일반 사용자의 계정이어야 한다")
def general_user(session):
    user = session.query(User).filter(User.admin == False).first()
    assert user
    return user


@pytest.fixture
@when(parsers.parse("올바른 {uri}에 자신의 정보를 요청했을 때"))
def request_uri(client, general_user, uri, session):
    uri = uri + str(general_user.id)

    response = client.get(uri, data=dict(id=general_user.id))
    user = user_schema.load(response.json, session=session)

    assert response.status_code == 200
    return user


@then("자신의 정보가 결과로 나온다")
def check_user_info(general_user, request_uri):
    assert general_user == request_uri


# Scenario 4

@scenario('../../features/user/user_검색.feature', '일반 사용자가 다른 사람의 user 정보 검색')
def test_사용자_권한_없어서_검색_실패():
    pass


@given("일반 사용자의 계정이어야 하고")
def user_is_general(session):
    user = User.query.filter(User.admin == False).first()
    assert user

    return user


@given("DB에 자신과 다른 user가 있어야 한다.")
def users_in_db(general_user):
    another_user = User.query.filter(User.id != general_user.id).first()
    assert another_user

    return another_user


@pytest.yield_fixture
@when("올바른 {uri}에 다른 사람의 user 정보를 요청했을 때")
def request_no_authorize(client, users_in_db, user_is_general, uri, session):
    uri = uri + str(users_in_db.id)
    response = client.get(uri, data=dict(id=user_is_general.id))

    yield response


@then("권한이 없으므로 검색에 실패하게 되고, status code 400이 반환된다")
def no_authority(request_no_authorize):
    assert request_no_authorize.status_code == 401


# Scenario 5

@pytest.mark.xfail(strict=True)
@scenario('../../features/user/user_검색.feature', 'DB에 user가 없어서 검색 불가')
def test_user_없음_실패():
    pass


@given("DB에 사용자가 존재하지 않는다")
def no_user_in_db():
    User.query.delete()
    assert not User.query.all()


@pytest.yield_fixture
@when(parsers.parse("{uri}에 user의 정보 검색을 요청했을 때"))
def request_uri_delete(client, uri, user):
    response = client.get(uri, data=dict(id=user.id))
    assert response.status_code == 500


@then("DB에 user가 없으므로 검색이 불가능하다")
def error_caused_by_empty_db():
    assert not User.query.first()




