import fnmatch
import Foundation
import subprocess

class Tags:
    NSURLTagNamesKey = 'NSURLTagNamesKey'

    def __init__(self):
        pass

    @classmethod
    def get_tags(cls, path):
        url = Foundation.NSURL.fileURLWithPath_(path)
        metadata, error = url.resourceValuesForKeys_error_([ cls.NSURLTagNamesKey ], None)
        if not metadata:
            return set()
        elif cls.NSURLTagNamesKey not in metadata:
            return set()
        else:
            return set(metadata[cls.NSURLTagNamesKey])

    @classmethod
    def set_tags(cls, path, tags):
        tags = list(tags)
        url = Foundation.NSURL.fileURLWithPath_(path)
        result, error = url.setResourceValue_forKey_error_(tags, cls.NSURLTagNamesKey, None)
        if not result:
            raise Exception('Could not set tags', unicode(error).encode('ascii', 'ignore'))

    @staticmethod
    def add_tag(self, path, tag):
        tags = Tags.get_tags(path)
        if tag in tags:
            return
        tags.add(tag)
        Tags.set_tags(path, tags)

    @staticmethod
    def add_tags(self, path, new_tags):
        if not new_tags:
            return
        tags = Tags.get_tags(path)
        tags.update(new_tags)
        Tags.set_tags(path, tags)

    @staticmethod
    def remove_tag(path, tag):
        tags = Tags.get_tags(path)
        if tag in tags:
            tags.remove(tag)
            Tags.set_tags(path, tags)

    @staticmethod
    def remove_tags(path, tags):
        old_tags = Tags.get_tags(path)
        new_tags = [tag for tag in old_tags if tag not in tags]
        Tags.set_tags(path, new_tags)

    @staticmethod
    def remove_tags_glob(path, patterns):
        tags = Tags.get_tags(path)
        found_tags = set()
        for pattern in patterns:
            for tag in tags:
                if fnmatch.fnmatch(tag, pattern):
                    found_tags.add(tag)
        remove_tags(path, found_tags)
