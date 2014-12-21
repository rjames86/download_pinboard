from datetime import datetime
from dateutil.tz import tzutc
import dateutil.parser
import plistlib
import os
import sys
import re

from lib import (
    pinboard,
    Tags,
    PinboardPrefs
)

HOME = os.path.expanduser('~')
BASEPATH = HOME + '/Dropbox/Sync/Bookmarks/'

# Token can be found at https://pinboard.in/settings/password
_PINBOARD_TOKEN = 'Your token here'


def to_dt(thing):
    return dateutil.parser.parse(thing)


class PinboardDownloader:
    def __init__(self, username=None, password=None, token=None):
        self.p = pinboard.open(username, password, token)
        self.prefs = PinboardPrefs()
        self.pinboard_last_updated = to_dt(self.p.last_update())
        self.last_updated = self.get_last_updated()

    @property
    def needs_update(self):
        return self.last_updated < self.pinboard_last_updated

    def get_last_updated(self):
        last_updated = self.prefs.get('last_updated')
        return datetime(1970, 1, 1, tzinfo=tzutc()) \
            if not last_updated else to_dt(last_updated)

    def set_last_updated(self, reset=False):
        if reset:
            timestamp = datetime(1970, 1, 1, tzinfo=tzutc())
        else:
            timestamp = self.pinboard_last_updated
        self.prefs.set('last_updated', timestamp.isoformat())
        self.last_updated = timestamp

    def get_posts(self):
        return self.p.posts(fromdt=self.last_updated)

    def write_to_file(self, filepath, data):
        with open(filepath, 'w') as f:
            f.write(plistlib.writePlistToString(data))

    def download_posts(self):
        if not self.needs_update:
            print "Pinboard download is up-to-date. Exiting..."
            sys.exit(1)
        posts_to_download = self.get_posts()
        print "got %s posts..." % len(posts_to_download)
        for post in posts_to_download:
            filename = self._clean_filename(post['description'])
            data = {
                'URL':  post['href']
            }
            self.write_to_file(
                filename,
                data
            )
            Tags.set_tags(filename, post['tags'])
        self.set_last_updated()

    def _clean_filename(self, description):
        return BASEPATH + re.sub(r'[/]', ' ', description) + '.webloc'

if __name__ == '__main__':
    p = PinboardDownloader(token=_PINBOARD_TOKEN)
    p.download_posts()
