from Foundation import (
    CFPreferencesAppSynchronize,
    CFPreferencesCopyAppValue,
    CFPreferencesCopyKeyList,
    CFPreferencesSetValue,
    kCFPreferencesAnyUser,
    kCFPreferencesCurrentUser,
    kCFPreferencesCurrentHost
)

import logging


def configure_log(level=None, name=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # file_handler = logging.FileHandler('../logs/%s' % name,'w','utf-8')
    # file_handler.setLevel(logging.DEBUG)
    # file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
    # file_handler.setFormatter(file_format)
    # logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    return logger


class Preferences(object):
    """Class which directly reads/writes Apple CF preferences."""

    def __init__(self, bundle_id, user=kCFPreferencesAnyUser):
        """Init.

        Args:
            bundle_id: str, like 'ManagedInstalls'
        """
        if bundle_id.endswith('.plist'):
            bundle_id = bundle_id[:-6]
        self.bundle_id = bundle_id
        self.user = user

    def __iter__(self):
        keys = CFPreferencesCopyKeyList(
            self.bundle_id, self.user, kCFPreferencesCurrentHost)
        if keys is not None:
            for i in keys:
                yield i

    def __contains__(self, pref_name):
        pref_value = CFPreferencesCopyAppValue(pref_name, self.bundle_id)
        return pref_value is not None

    def __getitem__(self, pref_name):
        return CFPreferencesCopyAppValue(pref_name, self.bundle_id)

    def __setitem__(self, pref_name, pref_value):
        CFPreferencesSetValue(
            pref_name, pref_value, self.bundle_id, self.user,
            kCFPreferencesCurrentHost)
        CFPreferencesAppSynchronize(self.bundle_id)

    def __delitem__(self, pref_name):
        self.__setitem__(pref_name, None)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.bundle_id)

    def get(self, pref_name, default=None):
        if pref_name not in self:
            return default
        else:
            return self.__getitem__(pref_name)

    def set(self, pref_name, pref_value):
        self.__setitem__(pref_name, pref_value)


class PinboardPrefs(Preferences):
    def __init__(self):
        self.bundle_id = 'com.ryanmo.downloadpinboard'
        self.user = kCFPreferencesCurrentUser
