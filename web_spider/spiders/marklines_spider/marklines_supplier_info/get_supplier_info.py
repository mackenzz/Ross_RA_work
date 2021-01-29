# -*- coding:utf-8 -*-
import json
import time
from multiprocessing import Process
from tools.log import logger

from spiders.marklines_spider import MarklinesBaseScripts
from cache.marklines_cache import MarkLinesRedis
from db import conn
from db.marklines.marklines import MarklinesSupplier
from spiders.marklines_spider.marklines_supplier_info.supplier_info_mitm import mitm_start
from spiders import error_tracker


class MarklinesSupplierScripts(MarklinesBaseScripts):

    def __init__(self, mitm_port, start_page, end_page):
        super(MarklinesSupplierScripts, self).__init__()
        self.mitm_port = mitm_port
        self.supplier_detail_rds = MarkLinesRedis("title")
        self.detail_counter = 0
        self.start_page = start_page
        self.end_page = end_page

    def open_supplier_and_page_down(self):
        self.supplier_detail_rds.ltrim_info(self.mitm_port)  # 清空redis残余数据
        start_time = time.time()
        for i in range(self.start_page, self.end_page + 1):  # 爬数据300页就够了，多1次，让脚本保存上一次的数据
            url = "https://www.marklines.com/cn/supplier_db/partDetail?page=%s&size=10&tb=top&isFromBtn=false&parts[]=1&_is=true&containsSub=true&isPartial=false&oth.place[]=n,2&oth.isPartial=true&oth.inv[]=2" % i
            self.get_to_page(url, 60)  # 60秒页面加载超时时间
            self.scroll_down()
            self.save_supplier_info(start_time)
            time.sleep(5)

    def save_supplier_info(self, start_time):
        while True:
            data = self.supplier_detail_rds.lpop_info(self.mitm_port)
            if not data:
                return
            data = json.loads(data)

            supplier_code = data['supplier_code']
            other_basic_info = json.dumps(data['other_basic_info'], ensure_ascii=False)
            product_type = json.dumps(data['product_type'], ensure_ascii=False)
            other_type_cn = json.dumps(data['other_type_cn'], ensure_ascii=False)
            other_type_en = json.dumps(data['other_type_en'], ensure_ascii=False)
            matching_info = json.dumps(data['matching_info'], ensure_ascii=False)
            clients = json.dumps(data['clients'], ensure_ascii=False)
            values = {"supplier_code": supplier_code, "other_basic_info": other_basic_info,
                      "product_type": product_type, "other_type_cn": other_type_cn, "other_type_en": other_type_en,
                      "matching_info": matching_info, "clients": clients}
            try:
                self.update_supplier_detail(supplier_code, other_basic_info, product_type, other_type_cn, other_type_en,
                                            matching_info, clients)
            except Exception as e:
                logger.error(e)
                logger.error(values)
            total_time = time.time() - start_time
            self.detail_counter += 1
            logger.info("已保存%s条供应商信息，累计用时%.2f秒" % (self.detail_counter, total_time))
            conn.commit()

    def update_supplier_detail(self, supplier_code, other_basic_info, product_type, other_type_cn, other_type_en,
                               matching_info, clients):
        info = MarklinesSupplier.get_info(supplier_code)
        if info:
            MarklinesSupplier.update_info(supplier_code, other_basic_info, product_type, other_type_cn, other_type_en,
                                          matching_info, clients)
        else:
            logger.error("没有找到对应的供应商信息：%s" % supplier_code)

    def run(self):
        self.auto_login(self.mitm_port, "c9464de9ab", "pw1426", "xnwang@umich.edu")  # 自动登录
        self.open_supplier_and_page_down()


@error_tracker
def marklines_supplier_script_run(mitm_port, proxy_ip, start_page, end_page):
    supplier = MarklinesSupplierScripts(mitm_port, start_page, end_page)
    p1 = Process(target=mitm_start, args=(mitm_port,), kwargs={"proxy_ip": proxy_ip})
    p1.start()
    supplier.run()
    p1.terminate()


if __name__ == '__main__':
    marklines_supplier_script_run(9999, 0, 88, 300)
