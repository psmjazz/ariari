from pytest_bdd import scenario, given, when, then, parsers
from application.models.used_vacation import UsedVacation
from application.schemata.used_vacation import UsedVacationSchema
from application.models.user import User
import pytest
import random


used_vacation_schema = UsedVacationSchema()


@pytest.fixture
def general_user(session):
    try:
        general_user = User.query.filter_by(google_id="khtks@naver.com").first()
        assert not general_user

        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        session.add(general_user)


    except BaseException:
        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        general_user.google_id = str(random.randint(1, 1000)) + "_" + general_user.google_id
        session.add(general_user)

    session.commit()
    return general_user


@pytest.fixture
def admin_user(session):
    try:
        admin_user = User(google_id="konghs@naver.com", en_name="Sam", ko_name="Kong", admin=True)
        session.add(admin_user)
        session.commit()


    except BaseException:
        admin_user = User(google_id="konghs@naver.com", en_name="Sam", ko_name="Kong", admin=True)
        admin_user.google_id = str(random.randint(1, 1000)) + "_" + admin_user.google_id
        session.add(admin_user)
        session.commit()

    return admin_user


# Scenario 1

@scenario('../../features/used_vacation/사용한_휴가_검색.feature', '사용자가 자신이 사용한 휴가 검색')
def test_자신의_휴가_검색():
    pass


@given("DB에 사용자와 휴가 기록이 있다")
def data_in_db(client, session, general_user):
    response = client.post('/users/vacations/used')

    assert response.status_code == 201
    assert User.query.all()

    return general_user


@pytest.yield_fixture
@when("사용자가 자신이 사용한 휴가 검색")
def search_used_vacation(client, session, data_in_db):
    uri = '/users/vacations/' + str(data_in_db.id) + '/used'
    response = client.get(uri, data={"id": data_in_db.id})

    assert response.status_code == 200
    # print(response.json)
    yield used_vacation_schema.load(response.json, session=session, many=True)


@then("사용자의 휴가가 반환된다")
def user_used_vacation(search_used_vacation, data_in_db):
    assert search_used_vacation == UsedVacation.query.filter_by(user=data_in_db).all()


# Scenario 2

@scenario('../../features/used_vacation/사용한_휴가_검색.feature', '관리자가 다른 사용자의 휴가 검색')
def test_관리자가_휴가_검색():
    pass


@given("현재 사용자가 관리자이다")
def user_is_admin(admin_user):
    assert admin_user.admin == True
    return admin_user


@pytest.yield_fixture
@when(parsers.parse("{uri}에 요청하여다른 사용자의 휴가를 검색할 경우"))
def request_used_vacation(client, user_is_admin, session, uri):
    response = client.get(uri, data=dict(id=user_is_admin.id))

    assert response.status_code == 200
    yield used_vacation_schema.load(response.json, session=session, many=True)


@then("검색한 사용자의 휴가가 반환된다")
def used_vacation_result(request_used_vacation):
    assert UsedVacation.query.all() == request_used_vacation


# Scenario 3

@scenario('../../features/used_vacation/사용한_휴가_검색.feature', '일반 사용자가 다른 사람의 휴가를 검색할 경우 실패')
def test_권한이_없어서_검색_실패():
    pass


@given("현재 사용자가 일반 사용자이다")
def user_is_general(general_user):
    assert general_user.admin == False
    return general_user


@when("다른 사용자의 휴가를 검색할 경우")
def request_another_used_vacation(client, session, user_is_general):
    response = client.get('/users/vacations/used', data=dict(id=user_is_general.id))

    assert response.status_code == 401


@then("권한이 없으므로 검색 실패")
def no_authority():
    pass
