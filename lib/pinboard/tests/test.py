#!/usr/bin/env python

"""Python-Pinboard unit tests.

Before running the tests:

1. Update user credentials at conf.py (see sample_conf.py for example).
2. Consider to backup your data before running this test on real account
or use dedicated sandbox account (the second approach is recommended)."""

import conf
import unittest
import sys
import time

sys.path.insert(0, '..')

import pinboard


def get_tag_names(tags):
    for tag in tags:
        yield tag['name']


class TestPinboardAccount(unittest.TestCase):

    def test_token(self):
        print '\nTest Token Auth and Common Cases'
        p = pinboard.open(token=conf.token)
        self.common_case(p)

    def test_canonical(self):
        print '\nTest Username/Pwd Auth and Common Cases'
        p = pinboard.open(conf.username, conf.password)
        self.common_case(p)

    def common_case(self, p):
        """Add some test bookmark records and than delete them"""
        print 'Executing Common Cases'
        test_url = 'http://github.com'
        test_tag = '__testing__'

        # Adding a test bookmark
        p.add(url=test_url,
              description='GitHub',
              extended='It\'s a GitHub!',
              tags=(test_tag),
              toread=False)

        # Test only_toread parameter. Test bookmark should not be returned.
        posts = p.posts(tag=test_tag, only_toread=True)

        self.assertIs(type(posts), list)
        self.assertFalse(posts)

        # Looks like there is no immediate consistency between API inputs
        # and outputs, that's why additional delays added here and below.
        print 'API Threshold Delay (3 seconds)'
        time.sleep(3)

        print 'API Resuming'

        posts = p.posts(tag=test_tag)

        # Bookmark was added
        self.assertIs(type(posts), list)
        self.assertTrue(posts)

        # Looks like there is no immediate consistency between API inputs
        # and outputs, that's why additional delays added here and below.
        print 'API Threshold Delay (3 seconds)'
        time.sleep(3)

        print 'API Resuming'
        # Tags contains new tag
        tags = p.tags()
        self.assertTrue(type(tags), dict)
        self.assertIn(test_tag, get_tag_names(tags))

        # Deleting test bookmark(s)
        for post in posts:
            p.delete(post['href'])

        print 'API Threshold Delay (3 seconds)'
        time.sleep(3)

        print 'API Resuming'
        # There are no posts with test tag
        posts = p.posts(tag=test_tag)
        self.assertFalse(posts)

        # And no test tag any more
        tags = p.tags()
        self.assertNotIn(test_tag, tags)


if __name__ == '__main__':
    unittest.main()
