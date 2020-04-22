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

def get_servable_pictures(json, picture_path):
    if 'error' not in json:
        print(json)
        if picture_path in json['data']:
            if json['data'][picture_path] == '' or json['data'][picture_path] is None:
                json['data'][picture_path] = User_Requests.get_default_image()
            elif json['data'][picture_path] == []:
                json['data'][picture_path] = [ User_Requests.get_default_image() ]
            elif isinstance(json['data'][picture_path], str):
                json['data'][picture_path] = get_image_url(
                    json['data']['User_ID'],
                    json['data'][picture_path]
                )
            else:
                picture_links = []
                for pic in json['data'][picture_path]:
                    picture_links.append(
                        get_image_url(
                            json['data']['User_ID'],
                            pic
                        )
                    )
                json['data'][picture_path] = picture_links
     
    return json

def get_list_servable_pictures(json, picture_path):
    if 'error' not in json:
        if len(json['data']) >= 1:
            for i in range(len(json['data'])):
                if picture_path in json['data'][i]:
                    if json['data'][i][picture_path] == '' or json['data'][i][picture_path] is None:
                        json['data'][i][picture_path] = User_Requests.get_default_image()  
                    elif isinstance(json['data'][i][picture_path], str):
                        json['data'][i][picture_path] = get_image_url(
                            json['data'][i]['User_ID'],
                            json['data'][i][picture_path]
                        )
    return json

def check_req_success(response, picture_path=None):
    if 200 <= response.status_code <= 203:
        return response.json()
    else:
        return { 'error': loads(response.text) }

def get_image_url(user_id, image_path):
    return api_url + get_route('images', user=user_id, image=image_path)

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
        image_path = r'{}'.format(image_path)
        with open(image_path, 'rb') as image:
            print('Opened: {img}'.format(img=image_path))
            #print(guess_type(image)[0])
            resp = requests.post(
                api_url + get_route('images', assign_user=True),
                data = image,
                headers = get_request_headers(
                    token=auth_token, 
                    content_type=guess_type(image_path)[0]
                )
            )
            print('{s}: {r}'.format(s=resp.status_code, r=resp.reason))
            return check_req_success(resp)
    
    @staticmethod
    def get_default_image():
        return get_image_url('default','user.png')

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
            api_url + get_route('user_verify', effected_id=user_id),
            json = {'Verification_Code':code},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def get_info(user_id, auth_token):
        resp = requests.get(
            api_url + get_route('user', effected_id=user_id),
            headers = get_request_headers(token=auth_token)
        )
        return get_servable_pictures(check_req_success(resp), 'pictures')

    @staticmethod
    def get_friends(user_id, auth_token):
        resp = requests.get(
            api_url + get_route('user_friends', effected_id=user_id),
            headers = get_request_headers(token=auth_token)
        )
        return get_list_servable_pictures(check_req_success(resp), 'Picture_Path')

    @staticmethod    
    def get_feed(auth_token, offset=0, limit=15):
        resp = requests.get(
            api_url + get_route('user_feed', offset=offset, limit=limit),
            headers = get_request_headers(token=auth_token)
        )
        return get_list_servable_pictures(check_req_success(resp), 'Picture_Path')

    @staticmethod
    def get_matches(auth_token, offset=0, limit=15):
        resp = requests.get(
            api_url + get_route('user_matches', offset=offset, limit=limit),
            headers = get_request_headers(token=auth_token)
        )
        return get_list_servable_pictures(check_req_success(resp), 'Picture_Path')

    @staticmethod
    def edit(user_id, auth_token, user_edits):
        resp = requests.patch(
            api_url + get_route('user', effected_id=user_id),
            json = user_edits,
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def get_change_password_code(auth_token):
        resp = requests.get(
            api_url + get_route('user_change_password'),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def check_change_password_code(auth_token, code):
        resp = requests.patch(
            api_url + get_route('user_change_password'),
            json = { 'Password_Code': code },
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def change_password(auth_token, password):
        resp = requests.post(
            api_url + get_route('user_change_password'),
            json = { 'Password': password },
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user', effected_id=user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def add_tags(user_id, auth_token, tags):
        resp = requests.post(
            api_url + get_route('user_tags', effected_id=user_id),
            json = {'User_Tags': tags},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def delete_tags(user_id, auth_token, tags):
        resp = requests.delete(
            api_url + get_route('user_tags', effected_id=user_id),
            json = {'User_Tags': tags},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def get_friend_requests(user_id, auth_token):
        resp = requests.get(
            api_url + get_route('user_friend_requests', effected_id=user_id),
            headers = get_request_headers(token=auth_token)
        )
        return get_list_servable_pictures(check_req_success(resp), 'Picture_Path')

    @staticmethod
    def send_friend_request(user_id, auth_token):
        resp = requests.post(
            api_url + get_route('user_friend_requests', effected_id=user_id),
            json = {},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete_friend_request(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user_friend_requests', effected_id=user_id),
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def accept_friend_request(user_id, auth_token):
        resp = requests.patch(
            api_url + get_route('user_friend_requests', effected_id=user_id),
            json = {},
            headers = get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete_friendship(user_id, auth_token):
        resp = requests.delete(
            api_url + get_route('user_friends', effected_id=user_id),
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
    def get(event_id, auth_token):
        resp = requests.get(
            api_url + get_route('event', effected_id=event_id),
            headers=get_request_headers(token=auth_token)
        )

        return get_servable_pictures(check_req_success(resp), 'Picture_Path')

    @staticmethod
    def edit(event_id, auth_token, event_data):
        resp = requests.patch(
            api_url + get_route('event', effected_id=event_id),
            json = event_data,
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)

    @staticmethod
    def delete(event_id, auth_token):
        resp = requests.delete(
            api_url + get_route('event', effected_id=event_id),
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def attending(event_id, auth_token):
        resp = requests.post(
            api_url + get_route('event_users', effected_id=event_id),
            json = {},
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def delete_attending(event_id, auth_token):
        resp = requests.delete(
            api_url + get_route('event_users', effected_id=event_id),
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def upload_image(auth_token, image_path):
        image_path = r'{}'.format(image_path)
        with open(image_path, 'rb') as image:
            print('Opened: {img}'.format(img=image_path))
            #print(guess_type(image)[0])
            resp = requests.post(
                api_url + get_route('images', assign_user=False),
                data = image,
                headers = get_request_headers(
                    token=auth_token, 
                    content_type=guess_type(image_path)[0]
                )
            )
            print('{s}: {r}'.format(s=resp.status_code, r=resp.reason))
            return check_req_success(resp)

class Report_Requests:

    @staticmethod
    def report_user(user_id, auth_token, reason):
        resp = requests.post(
            api_url + get_route('report_user', effected_id=user_id),
            json = { 'Report_Reason':reason },
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)
    
    @staticmethod
    def report_event(event_id, auth_token, reason):
        resp = requests.post(
            api_url + get_route('report_event', effected_id=event_id),
            json = { 'Report_Reason':reason },
            headers=get_request_headers(token=auth_token)
        )
        return check_req_success(resp)