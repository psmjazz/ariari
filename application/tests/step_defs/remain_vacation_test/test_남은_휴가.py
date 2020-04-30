from pytest_bdd import scenario, given, when, then
from application.models.user import User
from application.models.remain_vacation import RemainVacation
from application.schemata.remain_vacation import RemainVacationSchema
from application.models.used_vacation import UsedVacation
import pytest
import random
import datetime


remain_vacation_schema = RemainVacationSchema()


@pytest.fixture
def general_user(session):
    try:
        general_user = User.query.filter_by(google_id="khtks@naver.com").first()
        assert not general_user

        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", entry_date=datetime.datetime(2017,1,1), admin=False)
        session.add(general_user)

    except BaseException:
        general_user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", entry_date=datetime.datetime(2017,1,1), admin=False)
        general_user.google_id = str(random.randint(1, 1000)) + "_" + general_user.google_id
        session.add(general_user)

    session.commit()
    return general_user


@pytest.fixture
def admin_user(session):
    try:
        admin_user = User.query.filter_by(google_id="konghs@naver.com").first()
        assert not admin_user

        admin_user = User(google_id="konghs@naver.com", en_name="Sam", ko_name="Kong", admin=True)
        session.add(admin_user)

    except BaseException:
        admin_user = User(google_id="konghs@naver.com", en_name="Sam", ko_name="Kong", admin=True)
        admin_user.google_id = str(random.randint(1, 1000)) + "_" + admin_user.google_id
        session.add(admin_user)

    session.commit()
    return admin_user


# Scenario 1

@scenario('../../features/remain_vacation/남은_휴가.feature', '사용자 등록')
def test_사용자_등록():
    pass


@given("사용자의 정보가 user DB에 있다")
def user_is_in_db(client, general_user):

    assert User.query.all()
    return general_user


@given("remain vacation db가 존재한다")
def user_vacation_db():

    assert RemainVacation.query


@then("사용자의 남은 휴가 정보가 reamin vacation db에 등록된다")
def remain_vacation_is_in_db(client, user_is_in_db):
    response = client.post('/users/vacations/' + str(user_is_in_db.id) + '/remain')

    assert response.status_code == 201
    assert RemainVacation.query.all()


# Scenario 2

@scenario('../../features/remain_vacation/남은_휴가.feature', 'used vacation에 휴가가 등록되면 남은 휴가 자동 계산')
def test_남은_휴가_계산():
    pass


@given("db에 사용자의 정보가 저장되어 있다")
def user_in_db(session):
    user = User.query.first()

    assert RemainVacation.query.filter_by(user=user).all()
    return user


@when("used vacation에 휴가가 등록될 때")
def registered_vacation(client, user_in_db):
    response = client.post('users/vacations/used')

    assert response.status_code == 201
    assert UsedVacation.query.filter_by(user=user_in_db).all()


@then("remain vacation의 남은 휴가가 수정된다")
def modify_remain_vacation(client, user_in_db):
    uri = '/users/vacations/' + str(user_in_db.id) + '/remain'
    response = client.put(uri)

    assert response.status_code == 200


# Scenario 3

@scenario('../../features/remain_vacation/남은_휴가.feature', '남은 휴가 검색')
def test_남은_휴가_검색():
    pass


@given("현재 db에 사용자가 있다")
def user_exist(client, session, general_user, admin_user):
    user = User.query.first()
    try:
        assert RemainVacation.query.filter_by(user=user).all()

    except BaseException:
        uri = '/users/vacations/' + str(user.id) + '/remain'
        response = client.post(uri)

        assert response.status_code == 201


@given("현재 사용자가 관리자이다")
def user_is_admin(admin_user):
    assert admin_user.admin == True

    return admin_user


@pytest.yield_fixture
@when("남은 휴가 검색을 요청했을 때")
def request_remain_vacation(client, session, user_is_admin):
    response = client.get('/users/vacations/remain', data=dict(id=user_is_admin.id))

    assert response.status_code == 200
    yield remain_vacation_schema.load(response.json, many=True, session=session)


@then("remain vacation의 남은 휴가가 검색된다")
def search_result(request_remain_vacation):
    assert request_remain_vacation == RemainVacation.query.all()


# Scenario 4

@scenario('../../features/remain_vacation/남은_휴가.feature', '일반 사용자의 다른 사람의 휴가 검색 실패')
def test_일반_사용자의_검색_싶패():
    pass


@given("현재 사용자가 일반 사용자이다")
def user_is_general(general_user):
    assert general_user.admin == False

    return general_user


@pytest.yield_fixture
@when("다른 사람의 남은 휴가 검색을 요청할 때")
def request_another_user_vacation(client, session, user_is_general):
    response = client.get('/users/vacations/1/remain', data=dict(id=user_is_general.id))

    assert response.status_code == 401


@then("권한이 없어서 검색에 실패한다")
def fail_caused_by_no_authority():
    pass


# Scenario 5

@scenario('../../features/remain_vacation/남은_휴가.feature', '사용자 정보 수정')
def test_사용자_정보_수정():
    pass


@pytest.yield_fixture
@when("user db에서 사용자의 정보가 수정될 때")
def modify_user_info(client):
    general_user = User.query.filter_by(google_id="khtks@naver.com").first()
    admin_user = User.query.filter_by(google_id="konghs@naver.com").first()

    uri = '/users/' + str(general_user.id)
    user_response = client.put(uri, data=dict(id=admin_user.id, entry_date=datetime.datetime(2010,2,28)))
    vacation_response = client.put('users/vacations/1/remain')

    assert vacation_response.status_code == 200
    assert user_response.status_code == 200
    yield vacation_response.json


@then("해당 user의 remain vacation 정보도 수정된다")
def modified_user_info(modify_user_info):
    pass


# Scenario 6

@scenario('../../features/remain_vacation/남은_휴가.feature', '사용자 삭제')
def test_사용자_삭제():
    pass


@when("user db에서 사용자가 삭제될 때")
def delete_user(client):
    general_user = User.query.filter_by(admin=False).first()
    admin_user = User.query.filter_by(admin=True).first()

    id = str(general_user.id)
    uri = '/users/' + id
    user_response = client.delete(uri, data=dict(id=admin_user.id))
    vacation_response = client.delete('/users/vacations/' + id + '/remain', data=dict(id=admin_user.id))

    assert user_response.status_code == 200
    assert vacation_response.status_code == 200


@then("해당 user의 remain vacation 정보도 삭제된다")
def deleted_vacation():
    pass