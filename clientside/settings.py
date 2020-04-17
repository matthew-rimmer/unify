api_url = "http://DESKTOP-JITKUGS:8000" # Actual server url needed.

routes = {
    'login':                '/login',

    'create_user':          '/user/create',
    'user':                 '/user/{EFFECTED_ID}',
    'user_tags':            '/user/{EFFECTED_ID}/tags',
    'user_friends':         '/user/{EFFECTED_ID}/friends',
    'user_friend_requests': '/user/{EFFECTED_ID}/friends/requests',
    'user_verify':          '/user/{EFFECTED_ID}/verify',
    'user_feed':            '/feed',

    'create_event':         '/event/create',
    'event':                '/event/{EFFECTED_ID}',
    'event_users':          '/event/{EFFECTED_ID}/users',

    'images':               '/images',

    'report_user':          '/report/user/{EFFECTED_ID}',
    'report_event':         '/report/event/{EFFECTED_ID}'
}

def get_route(route, effected_id=None, **kwargs):
    if route in routes:
        output = routes[route].format(EFFECTED_ID=effected_id)
        
        has_param = False
        for key in kwargs:
            output += '?' if not has_param else '&'
            output += '{arg}={value}'.format(arg=key, value=kwargs.get(key))
            has_param = True

        return output