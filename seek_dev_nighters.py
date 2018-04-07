import requests
from pytz import timezone
from datetime import datetime


def load_attempts_data(pages):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    attempts = []
    for page in range(1, pages + 1):
        page_param = {'page': page}
        attempts_data = requests.get(url, params=page_param).json()['records']
        attempts += attempts_data
    return attempts


def get_midnighters(attempts_data):
    owl_users = []
    midnight = 0
    morning = 6
    for attempt in attempts_data:
        user_timezone = attempt['timezone']
        attempt_time_utc = datetime.fromtimestamp(attempt['timestamp'])
        attempt_time_local = timezone(user_timezone).fromutc(attempt_time_utc)
        if midnight < attempt_time_local.hour < morning:
            owl_users.append(attempt['username'])
    return set(owl_users)


def print_owl_users(user_list):
    print('Made attempts between 00:00 and 06:00:')
    for user in user_list:
        print(user)


if __name__ == '__main__':
    available_pages = 10
    attempts_data = load_attempts_data(available_pages)
    owl_users = get_midnighters(attempts_data)
    print_owl_users(owl_users)
