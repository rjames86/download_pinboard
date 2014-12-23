from sys import exit
# Token can be found at https://pinboard.in/settings/password
try:
    from settings import _PINBOARD_TOKEN
except ImportError:
    print "Settings file not found. Please create settings.py based on settings.py.example"
    exit(1)
from lib import PinboardDownloader
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Pinboard downloader",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--reset', dest='reset', const=10000, nargs='?', default=None, help='Reset Pinboard. Add a value to reset back X number of days')
    parser.add_argument('-t', action='append', dest='tags', help="Download based on specific filter. Maximum 3")
    parser.add_argument('--skip-update', action='store_true', dest='skip_update', default=False, help="Ignores the last updated time")
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default = False, help="Verbose")

    args = parser.parse_args()
    p = PinboardDownloader(token=_PINBOARD_TOKEN, verbose = args.verbose)

    extra_params = dict()
    if args.skip_update:
        p.set_last_updated(reset=args.reset or 10000)
    if args.reset:
        reset = args.reset
        if isinstance(reset, basestring):
            reset = int(reset)
        p.set_last_updated(reset=reset)
    elif args.tags:
        if len(args.tags) > 3:
            p.logger.error("Maximum number of tags is 3")
            exit(1)
        tags = " ".join(args.tags)
        p.download_posts(tag=tags, **extra_params)
    else:
        p.download_posts(**extra_params)
