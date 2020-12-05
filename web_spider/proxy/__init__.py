# -*- coding:utf-8 -*-
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster

import mitmproxy.addons.dumper  # 点进去注释掉166和214行，避免打印不必要的信息
import mitmproxy.proxy.server  # 点进去注释掉115和153行，避免打印不必要的信息
import mitmproxy.proxy.protocol.tls  # 点进去注释掉第452和453行，并添加pass，避免打印不必要的信息
import mitmproxy.proxy.server  # 点进去注释掉126到130避免打印不必要的信息


def mitm_run(port, addon, proxy_ip=None):
    if proxy_ip:
        opts = options.Options(listen_port=port, mode="upstream:http://%s" % proxy_ip, ssl_insecure=True)
    else:
        opts = options.Options(listen_port=port, ssl_insecure=True)
    proxy_config = proxy.config.ProxyConfig(opts)
    master = DumpMaster(opts)
    master.server = proxy.server.ProxyServer(proxy_config)
    master.addons.add(addon)

    try:
        master.run()
    except KeyboardInterrupt:
        master.shutdown()
