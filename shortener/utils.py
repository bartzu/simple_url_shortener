from urllib.parse import urlparse
from random import choice
from string import ascii_letters, digits

from .models import Shortcut

# characters for creating random shortcuts
CHARS = ascii_letters + digits + "-_"


def url_within_domain(request, url):
    '''Checks if request and url have the same domain'''
    return urlparse(url).netloc == request.get_host()


def get_sc_length():
    '''Chooses correct length for new shortcut'''
    db_len = Shortcut.objects.count()
    num = 2
    while db_len / 4 > pow(len(CHARS), num):
        num += 1
    return num


def get_random_str(length, chars=CHARS):
    '''Returns random subset of given length'''
    random_str = [choice(CHARS) for _ in range(length)]
    return ''.join(random_str)


def random_shortcut_value():
    '''Returns random shortcut value which is not yet used'''

    sc_length = get_sc_length()

    while True:
        sc_proposition = get_random_str(sc_length)
        # break from the loop when generated value is not in DB
        try:
            sc = Shortcut.objects.get(value=sc_proposition)
        except Shortcut.DoesNotExist:
            break
    
    return sc_proposition
