import requests
import asyncio
from json import loads, dumps
from mimetypes import guess_type

from .settings import get_route, api_url

def get_request_headers(token=None, content_type='application/json'):
    output = { 'Content-Type':content_type }
    if token is not None:
        output['Authorization'] = 'jwt {token}'.format(token=token)
    return output

def check_req_success(response):
    if 200 <= response.status_code <= 203:
        return response.json()
    else:
        print (response.reason)
        return None

class User_Requests:

    @staticmethod
    def create(user_data):
        if 'tags' in user_data:
            user_data['tag_rels'] = []
            for t in user_data['tags']:
                user_data['tag_rels'].append({
                    'User_Tag':t
                })
            del user_data['tags']
        resp = requests.post(
            api_url + get_route('create_user'),
            json = user_data,
            headers = get_request_headers()
        )
        return check_req_success(resp)
    
    @staticmethod
    def upload_image(auth_token, image_path):
        with open(image_path, 'rb') as image:
            print('Opened: {img}'.format(img=image_path))
            resp = requests.post(
                api_url + get_route('images', assign_user=True),
                data = image,
                headers = get_request_headers(
                    token=auth_token, 
                    content_type=guess_type(image_path)
                )
            )
            print('{s}: {r}'.format(s=resp.status_code, r=resp.reason))

    @staticmethod
    def login(login_data, auth_token=None):
        resp = requests.get(
            api_url + get_route('login'),
            json = login_data,
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod    
    def verify(user_id, auth_token, code):
        resp = requests.patch(
            api_url + get_route('user_verify', user_id),
            json = {'Verification_Code':code},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def get_info(user_id, auth_token):
        resp = requests.get(
            api_url + get_route('user', user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod    
    def get_feed(auth_token, offset=0, limit=15):
        resp = requests.get(
            api_url + get_route('user_feed', offset=offset, limit=limit),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def edit(user_id, auth_token, user_edits):
        resp = requests.patch(
            api_url + get_route('user', user_id),
            json = user_edits,
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def delete(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user', user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def add_tags(user_id, auth_token, tags):
        resp = requests.post(
            api_url + get_route('user_tags', user_id),
            json = {'User_Tags': tags},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def delete_tags(user_id, auth_token, tags):
        resp = requests.delete(
            api_url + get_route('user_tags', user_id),
            json = {'User_Tags': tags},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def send_friend_request(user_id, auth_token):
        resp = requests.post(
            api_url + get_route('user_friend_requests', user_id),
            json = {},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete_friend_request(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user_friend_requests', user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def accept_friend_request(user_id, auth_token):
        resp = requests.patch(
            api_url + get_route('user_friend_requests', user_id),
            json = {},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete_friendship(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user_friends', user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

class Event_Requests:

    @staticmethod
    def create(auth_token, event_data):
        resp = requests.post(
            api_url + get_route('create_event'),
            json = event_data,
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def edit(event_id, auth_token, event_data):
        resp = requests.patch(
            api_url + get_route('event', event_id),
            json = event_data,
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete(event_id, auth_token):
        resp = requests.delete(
            api_url + get_route('event', event_id),
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def attending(event_id, auth_token):
        resp = requests.post(
            api_url + get_route('event_users', event_id),
            json = {},
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def delete_attending(event_id, auth_token):
        resp = requests.delete(
            api_url + get_route('event_users', event_id),
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

class Report_Requests:

    @staticmethod
    def report_user(user_id, auth_token, reason):
        resp = requests.post(
            api_url + get_route('report_user', user_id),
            json = { 'Reason':reason },
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def report_event(event_id, auth_token, reason):
        resp = requests.post(
            api_url + get_route('report_event', event_id),
            json = { 'Reason':reason },
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)