import datetime
import json
import random
import time
from pathlib import Path
from sys import exit

from instagram_private_api import Client
from tqdm import tqdm

excluded_users = []
suspicious_likes = []
s_min = 0.5
s_max = 2.0


def is_suspicious(liked_item):
    friendship = liked_item['user']['friendship_status']
    return not friendship['following']


def get_taken_at_timestamp(liked_item):
    return datetime.datetime.fromtimestamp(liked_item['taken_at'])


def get_username(liked_item):
    return liked_item['user']['username']


# For future version with UI
def get_image_url(liked_item):
    url = None
    if 'carousel_media' in liked_item:
        image = liked_item['carousel_media'].get('image_versions2')
    else:
        image = liked_item.get('image_versions2')
    if image is not None:
        url = image['candidates'][0]['url']
    return url


def process_like_page(client, date_threshold, next_max_id=None):
    print('Processing like page...')
    kwargs = {'max_id': next_max_id} if next_max_id is not None else {}
    liked = client.feed_liked(**kwargs)
    next_max_id = liked.get('next_max_id')
    process_next_page = False
    has_next_page = liked['more_available'] and next_max_id is not None
    for item in liked["items"]:
        if is_suspicious(item):
            suspicious_likes.append(item)
        if get_taken_at_timestamp(item) > date_threshold:
            process_next_page = has_next_page
    return process_next_page, next_max_id


def remove_likes(client):
    print('Removing suspicious likes...\n')
    for l in tqdm(suspicious_likes):
        media_id = l['id']
        client.delete_like(media_id, module_name='feed_liked')
        sleep()
    print('\nRemoved suspicious likes')


def print_suspicious_users():
    if len(suspicious_likes) == 0:
        print('No suspicious likes found. Exiting.')
        exit(0)
    usernames = set()
    for l in suspicious_likes:
        usernames.add(get_username(l))
    s = '\n'.join(usernames)
    print(f'\nWill remove {len(suspicious_likes)} total likes to users:\n\n{s}\n')


def display_exclude_menu():
    while True:
        username = input('Write a username to exclude. Leave empty to stop excluding usernames:\n')
        username = username.strip()
        if not username:
            break
        else:
            excluded_users.append(username)


def exclude_likes():
    suspicious_likes[:] = [l for l in suspicious_likes if get_username(l) not in excluded_users]


def display_menu(client):
    print_suspicious_users()
    operation = input(f'Select operation:\n[1] Remove {len(suspicious_likes)} likes\n[2] Exclude usernames\n[3] Exit\n')
    if operation == '1':
        operation = input(f'Are you sure you wish to remove {len(suspicious_likes)} likes from the above users? [(y)es/(n)o]: ').strip().lower()
        if operation in ['y', 'yes']:
            remove_likes(client)
        elif operation in ['n', 'no']:
            exit(0)
        else:
            print("\nWrong choice\n")
            display_menu(client)
    elif operation == '2':
        display_exclude_menu()
        exclude_likes()
        display_menu(client)
    elif operation == '3':
        exit(0)
    else:
        print("\nWrong choice\n")
        display_menu(client)


def sleep():
    time.sleep(round(random.uniform(s_min, s_max), 2))


def main():
    date_threshold_str = '2020/09/01'
    username = None
    password = None

    config_path = Path("./config.json")
    if config_path.is_file():
        with open(config_path, mode='r') as config_file:
            config = json.load(config_file)
            username = config.get('username')
            password = config.get('password')
            if 'date_threshold_str' in config:
                date_threshold_str = config['date_threshold_str']
            global s_min
            s_min = config.get('s_min', s_min)
            global s_max
            s_max = config.get('s_max', s_max)

    if username is None:
        username = input("Enter insta username\n").strip()
    if password is None:
        password = input("Enter insta password\n").strip()

    date_threshold = datetime.datetime.strptime(date_threshold_str, '%Y/%m/%d')

    client = Client(username, password)

    (process_next_page, next_max_id) = process_like_page(client, date_threshold)
    while process_next_page:
        sleep()
        (process_next_page, next_max_id) = process_like_page(client, date_threshold, next_max_id)
    print(f'Processed likes. Found {len(suspicious_likes)} suspicious likes.')

    display_menu(client)


if __name__ == "__main__":
    main()
