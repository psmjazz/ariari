from google.auth.transport import requests
from google.oauth2 import id_token
from flask import Blueprint, redirect, url_for, request, session, render_template
import google_auth_oauthlib.flow


google_api_bp = Blueprint("google_api", __name__)
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']


@google_api_bp.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='online',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@google_api_bp.route('/oauth2callback')
def oauth2callback():

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('google_api.user_auth'))


@google_api_bp.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']

    return 'Credentials have been cleared.<br><br>' + print_index_table()


@google_api_bp.route('/authenticate-token')
def user_auth():
    cred = session['credentials']

    id_info = id_token.verify_oauth2_token(cred.get('id_token'), requests.Request(), cred.get('client_id'))

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    google_id = id_info.get('email')

    session['google_id'] = google_id

    return redirect(url_for('main'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'id_token': credentials.id_token}


def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/authorize">사용자 인증</a></td>' +
            '<td> 사용자 Google social login. 인증되어 token이 저장되면, 다시 인증하라는 메세지가 ' +
            '표시되지 않을수도 있다. </td></tr>' +
            '<tr><td><a href="/clear">자격증명 지우기</a></td>' +
            '<td> 현재 저장되어있는 인증 token을 지운다. ' +
            'token을 지우면 다시 인증을 해야한다.' +
            '</td></tr></table>')