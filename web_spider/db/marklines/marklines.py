# -*- coding:utf-8 -*-
from db import sql


class MarklinesSupplier(object):

    @staticmethod
    def get_info(supplier_code):
        sql.execute(
            'select * from marklines_supplier_detail where is_delete = 0  and supplier_code ="%s" ' % supplier_code)
        return sql.fetchone()

    @staticmethod
    def create_info(supplier_code, company_name, address, tel, url, country, province):
        sql.execute(
            """insert into marklines_supplier_detail (supplier_code, company_name, address, TEL, URL, country, province)
             VALUES ("{}","{}","{}","{}","{}","{}","{}")
               """.format(supplier_code, company_name, address, tel, url, country, province))
        return sql.lastrowid

    @staticmethod
    def update_info(supplier_code, other_basic_info, product_type, other_type_cn, other_type_en, matching_info,
                    clients):
        sql.execute(
            """update marklines_supplier_detail set other_basic_info='{}', product_type='{}', other_type_cn='{}', 
               other_type_en='{}', matching_info='{}',clients='{}' where supplier_code="{}"
            """.format(other_basic_info, product_type, other_type_cn, other_type_en, matching_info, clients,
                       supplier_code))
        return sql.rowcount

    @staticmethod
    def delete_detail(supplier_code):
        sql.execute('update marklines_supplier_detail set is_delete = 0 where supplier_code = "%s"' % supplier_code)
        return sql.rowcount
