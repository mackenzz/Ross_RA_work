# -*- coding:utf-8 -*-
import json

from lxml.html import etree
from proxy import mitm_run
from cache.marklines_cache import MarkLinesRedis


class ParseResponse:
    def __init__(self, port, proxy_ip):
        self.port = port
        self.proxy_ip = proxy_ip
        self.counter = 0
        self.supplier_info_rds = MarkLinesRedis("title")

    def request(self, flow):
        if self.proxy_ip:
            flow.request.headers["X-Forwarded-For"] = self.proxy_ip
            if flow.live:
                proxy = (self.proxy_ip.split(":")[0], int(self.proxy_ip.split(":")[1]))
                flow.live.change_upstream_proxy_server(proxy)

    def response(self, flow):
        if "?no_frame=true" in flow.request.url:
            data = flow.response.get_text()
            data = data.replace("\n", "").replace("\r", "").replace("\t", "")
            ele = etree.HTML(data)

            product = ele.xpath('//div[@class="row product"]')
            supplier_code = ele.xpath('//div[@class="supplier-code pull-right"]//text()')[1]
            basic_info = ele.xpath('//div[@id="basic-info"]')[0]
            keys = basic_info.xpath('./h4')
            values = basic_info.xpath('./p')

            founded_time = ""
            person_in_charge = ""
            annual_sales = ""
            employees = ""
            quality_certification = []
            environment_certification = []
            remark = ""
            for index, k in enumerate(keys):
                if "成立" in k.xpath('./text()'):
                    founded_time = values[index].xpath('./text()')[0]
                elif "公司负责人" in k.xpath('./text()'):
                    person_in_charge = values[index].xpath('./text()')[0]
                elif "年销售额" in k.xpath('./text()'):
                    annual_sales = values[index].xpath('./text()')[0]
                elif "员工人数" in k.xpath('./text()'):
                    employees = values[index].xpath('./text()')[0]
                elif "质量认证" in k.xpath('./text()'):
                    quality_certification = k.xpath('./following::p/text()')
                elif "环境认证" in k.xpath('./text()'):
                    environment_certification = k.xpath('./following::p/text()')
                elif "备注" in k.xpath('./text()'):
                    remark = k.xpath('./following::p/text()')[0]

            if quality_certification:
                for i in environment_certification:
                    quality_certification.remove(i)
                if environment_certification:
                    if remark:
                        environment_certification.remove(remark)

            other_basic_info = {"founded_time": founded_time, "person_in_charge": person_in_charge,
                                "annual_sales": annual_sales,
                                "employees": employees, "quality_certification": quality_certification,
                                "environment_certification": environment_certification, "remark": remark}

            product_type = product[0].xpath('.//div[@class="col-md-9 product-names-area disp-table"]//text()')

            try:
                other_type_cn = ele.xpath('//div[@class="col-md-9 comment"]')[0].xpath(".//text()")
                other_type_cn = [i for i in other_type_cn if i != ","]
            except Exception:
                other_type_cn = []
            try:
                other_type_en = ele.xpath('//div[@class="col-md-9 comment"]')[1].xpath(".//text()")
                other_type_en = [i for i in other_type_en if i != ","]
            except Exception:
                other_type_en = []

            matching_info = []
            titles = []
            try:
                matching = ele.xpath('//table[@class="table table-condensed table-bordered"]//tr')
                for index, i in enumerate(matching):
                    if index == 0:
                        titles = i.xpath('.//text()')
                    else:
                        item = {}
                        infos = i.xpath('.//text()')
                        for k, v in zip(titles, infos):
                            item.update({k: v})
                        matching_info.append(item)
            except Exception:
                pass

            try:
                clients = ele.xpath('//div[@class="col-md-9 product-names-area disp-table deliver-top"]//text()')
            except Exception:
                clients = []

            values = {"supplier_code": supplier_code, "other_basic_info": other_basic_info,
                      "product_type": product_type, "other_type_cn": other_type_cn, "other_type_en": other_type_en,
                      "matching_info": matching_info, "clients": clients}
            self.supplier_info_rds.rpush_info(self.port, json.dumps(values, ensure_ascii=False))
            self.counter += 1
            number = self.counter % 10 if self.counter % 10 != 0 else 10
            print("\r", end="")
            print("加载完【%s】个详情信息，累计【%s】个" % (number, self.counter), end="")


def mitm_start(port, proxy_ip=None):
    mitm_run(port, ParseResponse(port, proxy_ip), proxy_ip=proxy_ip)


if __name__ == '__main__':
    mitm_start(9999, 0)
