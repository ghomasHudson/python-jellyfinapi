# -*- coding: utf-8 -*-
import os
from collections import defaultdict
from configparser import ConfigParser

from jellyfinapi import utils


class JellyfinConfig(ConfigParser):
    """ JellyfinAPI configuration object. Settings are stored in an INI file within the
        user's home directory and can be overridden after importing jellyfinapi by simply
        setting the value. See the documentation section 'Configuration' for more
        details on available options.

        Parameters:
            path (str): Path of the configuration file to load.
    """

    def __init__(self, path):
        ConfigParser.__init__(self)
        self.read(path)
        self.data = self._asDict()

    def get(self, key, default=None, cast=None):
        """ Returns the specified configuration value or <default> if not found.

            Parameters:
                key (str): Configuration variable to load in the format '<section>.<variable>'.
                default: Default value to use if key not found.
                cast (func): Cast the value to the specified type before returning.
        """
        try:
            # First: check environment variable is set
            envkey = f"PLEXAPI_{key.upper().replace('.', '_')}"
            value = os.environ.get(envkey)
            if value is None:
                # Second: check the config file has attr
                section, name = key.lower().split('.')
                value = self.data.get(section, {}).get(name, default)
            return utils.cast(cast, value) if cast else value
        except:  # noqa: E722
            return default

    def _asDict(self):
        """ Returns all configuration values as a dictionary. """
        config = defaultdict(dict)
        for section in self._sections:
            for name, value in self._sections[section].items():
                if name != '__name__':
                    config[section.lower()][name.lower()] = value
        return dict(config)


def reset_base_headers():
    """ Convenience function returns a dict of all base X-Jellyfin-* headers for session requests. """
    import jellyfinapi
    return {
        'X-Jellyfin-Platform': jellyfinapi.X_PLEX_PLATFORM,
        'X-Jellyfin-Platform-Version': jellyfinapi.X_PLEX_PLATFORM_VERSION,
        'X-Jellyfin-Provides': jellyfinapi.X_PLEX_PROVIDES,
        'X-Jellyfin-Product': jellyfinapi.X_PLEX_PRODUCT,
        'X-Jellyfin-Version': jellyfinapi.X_PLEX_VERSION,
        'X-Jellyfin-Device': jellyfinapi.X_PLEX_DEVICE,
        'X-Jellyfin-Device-Name': jellyfinapi.X_PLEX_DEVICE_NAME,
        'X-Jellyfin-Client-Identifier': jellyfinapi.X_PLEX_IDENTIFIER,
        'X-Jellyfin-Language': jellyfinapi.X_PLEX_LANGUAGE,
        'X-Jellyfin-Sync-Version': '2',
        'X-Jellyfin-Features': 'external-media',
    }
