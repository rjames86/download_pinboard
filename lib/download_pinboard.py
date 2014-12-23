from datetime import datetime, timedelta
from dateutil.tz import tzutc
import dateutil.parser
import plistlib
import sys
import re
import logging


from lib import (
    pinboard,
    Tags,
    PinboardPrefs,
    configure_log
)

from settings import _SAVE_PATH


def to_dt(thing):
    return dateutil.parser.parse(thing)


class PinboardDownloader:
    def __init__(self, username=None, password=None, token=None, **kwargs):
        self.p = pinboard.open(username, password, token)
        self.logger = configure_log(logging.INFO, 'pinboarddownloader', verbose=kwargs.get('verbose'))
        self.prefs = PinboardPrefs()
        self.pinboard_last_updated = to_dt(self.p.last_update())
        self.last_updated = self.get_last_updated()

    @property
    def needs_update(self):
        return self.last_updated < self.pinboard_last_updated

    def get_last_updated(self):
        last_updated = self.prefs.get('last_updated')
        to_ret = datetime(1970, 1, 1, tzinfo=tzutc()) \
            if not last_updated else to_dt(last_updated)
        self.logger.info("Last updated locally: %s " % to_ret)
        return to_ret

    def set_last_updated(self, reset=0):
        if reset:
            timestamp = self.last_updated - timedelta(days=reset)
        else:
            timestamp = self.pinboard_last_updated
        self.prefs.set('last_updated', timestamp.isoformat())
        self.last_updated = timestamp
        self.logger.info("Setting last updated to %s" % timestamp)

    def get_posts(self, **kwargs):
        to_pass = dict()
        if kwargs.get('tag'):
            to_pass['tag'] = kwargs['tag']
            self.logger.info("Filtering posts by tags: %s" % kwargs['tag'])
            self.set_last_updated(reset=True)
        self.logger.info("Getting posts...")
        return self.p.posts(
            fromdt=self.last_updated,
            **to_pass
        )

    def write_to_file(self, filepath, data):
        self.logger.info("Writing to %s" % filepath.split('/')[-1])
        with open(filepath, 'w') as f:
            f.write(plistlib.writePlistToString(data))

    def download_posts(self, **kwargs):
        if not self.needs_update:
            self.logger.info("Pinboard download is up-to-date. Exiting...")
            sys.exit(1)
        posts_to_download = self.get_posts(**kwargs)
        self.logger.info("got %s posts..." % len(posts_to_download))
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
        return _SAVE_PATH + re.sub(r'[/]', ' ', description) + '.webloc'
