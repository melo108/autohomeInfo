class MyDupeFilter(object):
    def __init__(self):
        self.visited = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        """
        :param request:
        :return: True,已经下载过了；False，没有看过
        """
        # 放在数据库，在一台服务的文件中存储数据
        # 根据当前request.url在数据库中已经存在，表示已经爬取过
        # return True
        # 否则
        # 添加到数据库
        # return False

        # 放在redis中，在一台服务器的内容中存取数据（快）
        # {
        #    http://www.baidu.com:...
        #    http://www.baidu1.com:...
        #    http://www.baidu2.com:...
        #    http://www.baidu3.com:...
        #    http://www.baidu3.com:...
        # }
        if request.url in self.visited:
            return True
        self.visited.add(request.url)
        return False

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass