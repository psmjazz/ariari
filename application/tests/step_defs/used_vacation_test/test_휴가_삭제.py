from pytest_bdd import scenario, given, when, then
from application.models.used_vacation import UsedVacation
from application.schemata.used_vacation import UsedVacationSchema
from application.models.user import User
import datetime
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

@scenario('../../features/used_vacation/휴가_삭제.feature', '등록되어있던 휴가를 취소하면 휴가 삭제')
def test_휴가_정상_삭제():
    pass


@given("google calendar에 등록되어 있는 휴가가 있다")
def registered_vacation(session):
    used_vacation = UsedVacation(user=User(google_id="khtks@naver.com", en_name="Hammington"), summary="휴가 반차", \
                                 start_date=datetime.datetime(2020,2,2), end_date=datetime.datetime(2020,2,3), type="vacation", event_id='4qnk7nlk6upmfo651asrbs6ncm')
    session.add(used_vacation)
    session.commit()


@pytest.yield_fixture
@when("등록된 휴가를 삭제하는 경우")
def delete_vacation(client):
    response = client.delete('/users/vacations/used')

    assert response.status_code == 200


@then("used_vacation DB에서 삭제한다")
def deleted_vacation():
    pass


# Scenario 2

@scenario('../../features/used_vacation/휴가_삭제.feature', '관리자가 일반사용자가 등록한 휴가를 삭제')
def test_일반사용자의_휴가_삭제():
    pass


@given("현재 사용자가 관리자이다")
def user_is_admin(admin_user):
    assert admin_user.admin == True
    return admin_user


@given("DB에 일반 사용자의 등록된 휴가가 있다")
def general_user_vacation(client):
    response = client.post('/users/vacations/used')
    assert response.status_code == 201
    return UsedVacation.query.first().user


@when("관리자가 일반 사용자가 등록한 휴가를 삭제할 때")
def delete_general_user_vacation(client, session, general_user_vacation, user_is_admin):
    uri = '/users/vacations/' + str(general_user_vacation.id) + '/used'
    response = client.delete(uri, data=dict(id=user_is_admin.id))

    assert response.status_code == 200


@then("특정 사용자의 사용 휴가 정보가 DB에서 삭제된다")
def deleted_general_user_vacation(general_user_vacation):
    used_vacation = UsedVacation.query.filter_by(user=general_user_vacation).all()
    assert not used_vacation


# Scenario 3

@scenario('../../features/used_vacation/휴가_삭제.feature', '일반 사용자가 다른 사용자의 휴가 삭제')
def test_일반사용자가_다른사람의_휴가_삭제_실패():
    pass


@given("현재 사용자가 일반 사용자이다")
def user_is_general(session):
    user = User(google_id="sample@naver.com", en_name="name", admin=False)
    session.add(user)
    session.commit()

    assert user.admin == False
    return user


@given("DB에 다른 사용자의 등록된 휴가가 있다")
def another_user_vacation(client):
    response = client.post('/users/vacations/used')

    assert response.status_code == 201
    assert UsedVacation.query.all()


@when("일반 사용자가 다른 사용자의 휴가를 삭제할 때")
def general_user_delete_used_vacation(client, session, general_user, user_is_general):
    uri = '/users/vacations/' + str(general_user.id) + '/used'
    response = client.delete(uri, data=dict(id=user_is_general.id))

    assert response.status_code == 401


@then("권한이 없으므로 삭제가 실패한다")
def fail_caused_by_no_authority():
    pass