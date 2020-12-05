# -*- coding:utf-8 -*-
from proxy import mitm_run


class ParseResponse:

    def __init__(self, proxy_ip, task_id):
        self.proxy_ip = proxy_ip
        self.task_id = task_id

    def request(self, flow):
        if self.proxy_ip:
            flow.request.headers["X-Forwarded-For"] = self.proxy_ip
            if flow.live:
                proxy = (self.proxy_ip.split(":")[0], int(self.proxy_ip.split(":")[1]))
                flow.live.change_upstream_proxy_server(proxy)

    def response(self, flow):
        if "xxx" in flow.request.url:
            pass


mitm_run(9999, ParseResponse("127.0.0.1", 1))
