#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DiskCache.py
# @Author: Wade Cheung
# @Date  : 2018/6/17
# @Desc  : 磁盘缓存 . 将下载的html存入磁盘文件中


import os
import re
import urllib.request
import shutil
import pickle
from datetime import datetime, timedelta


class DiskCache:
    def __init__(self, cache_dir='D:\\data\\test_py\\cache', expires=timedelta(days=30), compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def url_to_path(self, url):
        """Create file system path for this URL"""
        components = urllib.request.urlsplit(str(url))
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query

        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;,]', '_', filename)

        # restrict maximum numer of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def __getitem__(self, url):
        """Load data from disk for this URL
        """
        if url:
            path = self.url_to_path(url)
            if os.path.exists(path):
                with open(path, 'rb') as fp:
                    return pickle.load(fp)
            else:
                # URL has not yet been cache
                raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save data to disk for this URL
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as fp:
            fp.write(pickle.dumps(result))

    def __delitem__(self, url):
        """Remove the value at this key and any empty parent sub-directories
        """
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def has_expired(self, timestamp):
        """Return whether this timestamp has expired
        """
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        """Remove all the cached values
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
