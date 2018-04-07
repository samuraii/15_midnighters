import requests
from pytz import timezone
from datetime import datetime


def load_attempts_data():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        page_param = {'page': page}
        attempts_data = requests.get(url, params=page_param).json()
        number_of_pages = attempts_data['number_of_pages']
        for attempt in attempts_data['records']:
            yield attempt
        page += 1
        if page > number_of_pages:
            break


def get_midnighters(attempts_data):
    owl_users = []
    midnight = 0
    morning = 6
    for attempt in attempts_data:
        user_timezone = timezone(attempt['timezone'])
        attempt_time_local = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=user_timezone
        )
        if midnight < attempt_time_local.hour < morning:
            owl_users.append(attempt['username'])
    return set(owl_users)


def print_owl_users(user_list):
    print('Made attempts between 00:00 and 06:00:')
    for user in user_list:
        print(user)


if __name__ == '__main__':
    owl_users = get_midnighters(load_attempts_data())
    print_owl_users(owl_users)
