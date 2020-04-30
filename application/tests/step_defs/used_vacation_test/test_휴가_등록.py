from pytest_bdd import scenario, given, when, then
from application.models.used_vacation import UsedVacation
from application.models.user import User
from flask import session
import pytest
import random


@pytest.fixture
def user(session):

    try:
        user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        session.add(user)
        session.commit()

    except BaseException:
        user = User(google_id="khtks@naver.com", en_name="Hammington", ko_name="Hee San", admin=False)
        user.google_id = str(random.randint(1, 1000)) + "_" + user.google_id
        print(user)
        session.add(user)
        session.commit()

    return user


# Background

@given("Google social login이 되어있다")
def check_authorize(client):

    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email',
              'https://www.googleapis.com/auth/userinfo.profile', 'openid']

    session['credentials'] = {'token': 'ya29.Il-_B58wT_WtACmi7NdqABpYMLoMxtTnK6PdMX3SotwU8TEVpWP46cHbRld2qLia0SyWSdHIhCWwpHqhgYjIxaYadKSna4gCwDqVtB5hTOfDn-BBU_G85c70Y-Fj5qaEeg', 'refresh_token': None, 'token_uri': 'https://oauth2.googleapis.com/token', 'client_id': '681480247057-33j28u2nbttjv6mq5j841967ackqb6fl.apps.googleusercontent.com', 'client_secret': 'f-FgdVVi_bnESelGmZbBaP0M', 'scopes': ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'], 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc5YzgwOWRkMTE4NmNjMjI4YzRiYWY5MzU4NTk5NTMwY2U5MmI0YzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2ODE0ODAyNDcwNTctMzNqMjh1Mm5idHRqdjZtcTVqODQxOTY3YWNrcWI2ZmwuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2ODE0ODAyNDcwNTctMzNqMjh1Mm5idHRqdjZtcTVqODQxOTY3YWNrcWI2ZmwuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDc3NzQ3MzUyMjcwODc0OTQ4MzQiLCJlbWFpbCI6ImtodGtzQG5hdmVyLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiZGlLZE5NdWw3TDFWMnNpUF9vUmhMQSIsIm5hbWUiOiJraHRrc0BuYXZlci5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDQuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy0zVnVLNGI0TDB0ay9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS83VkNaMHJ2eEtxSS9zOTYtYy9waG90by5qcGciLCJsb2NhbGUiOiJrbyIsImlhdCI6MTU4MjUyNjQ3NSwiZXhwIjoxNTgyNTMwMDc1fQ.avdhSvrDnvgm0PJqRzzbk4taK5GJZoYKP9ZrxIH0DShvmTAodP9V9504mgeGBFMXYsCuuzCoNTzAL_4KtY_WKQKXGTkBxwogTkeV0Uuxs8F412aKAdnF4TU3_MB_1qRa4SAPFbqAOo37Cq6VN7yfAZIkZ8fLB0wbhMUf1FL749vImiGjI8_WXrkcnu7tA1o0WvKAOkdsZLJ9cwWaSgLsgmQNo9ZLqVDn9evEBe8bTmedUReVr3WVnyfrSJ3uDeKGu0FjcjqnQ96a7qQibBYDCnKdjrQ8xtsgceVSWGAYeFJFBtM-6fUOVmrmvm6PZWAl-wZ4R21mmt4BjIHTje6CJg'}
    if 'credentials' not in session:
        print(session)


# Scenario 1

@scenario("../../features/used_vacation/휴가_등록.feature", "휴가 등록하기")
def test_휴가_등록():
    pass


@given("used_vacation DB가 존재한다")
def used_vacation_db(session, check_authorize):

    assert UsedVacation


@given("user의 정보가 DB에 존재한다.")
def user_in_db(session, user):
    assert user


@when("새로운 휴가가 등록되었을 때")
def new_vacation():
    pass


@then("used_vacation db에 휴가를 등록한다")
def register_used_vacation(client):
    response = client.post('users/vacations/used')
    assert response.status_code == 201


# Scenario 2

@pytest.mark.xfail(strict=False)
@scenario('../../features/used_vacation/휴가_등록.feature', 'event의 creator email이 User DB에 없는 경우 휴가 등록 실패')
def test_일치하는_사용자_없어서_실패():
    pass


@when("event의 creator와 일치하는 user가 db에 없는 경우")
def another_user(session):
    user = User.query.filter_by(google_id="khtks@naver.com").first()
    session.delete(user)
    session.commit()


@then("user가 없으므로 휴가 생성 불가")
def fail_caused_by_no_user(client):
    response = client.post('users/vacations/used')
