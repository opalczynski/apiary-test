import base64

import dredd_hooks as hooks
import requests

session = {}


@hooks.before_all
def register_user(transactions):
    response = requests.post(
        'http://localhost/auth/register/',
        data={
            'username': 'jdredd',
            'first_name': 'Judge',
            'last_name': 'Dredd',
            'organization_name': 'Dredd Co.'
        }
    )

    session['username'] = 'jdredd'
    session['access_key'] = response.json()['access_key']


@hooks.before_each
def add_auth_header(transaction):
    token = "{}:{}".format(session['username'], session['access_key'])
    transaction['request']['headers']['Authorization'] = "Basic {}".format(
        base64.b64encode(token.encode('utf-8')).decode('utf-8')
    )


@hooks.after_all
def remove_user(transactions):
    token = "{}:{}".format(session['username'], session['access_key'])
    response = requests.delete(
        'http://localhost/users/{}/'.format(session['username']),
        headers={
            'Authorization': "Basic {}".format(
                base64.b64encode(token.encode('utf-8')).decode('utf-8')
            )
        }
    )
    assert response.status_code, 204
