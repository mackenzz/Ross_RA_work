import pandas as pd

import time
from init_web_driver import initdriver
from lxml import etree


driver = initdriver()

url = "https://abstracts.societyforscience.org/"
driver.get(url)

driver.find_element_by_xpath('//label[@class="checkBoxLabel"][8]').click()
driver.find_element_by_xpath('//input[@id="IsGetAllAbstracts"][2]').click()
driver.find_element_by_xpath('//input[@type="submit"]').click()

time.sleep(3)
input("Change the entries per page from 10 to 100, then click return")

years, names, titles = [], [], []
categories, countries, awards = [], [], []

for j in range(93):
    for i in range(1, 100):
        year_path = '//tr[' + str(i) + ']/td[1]'   # like '//tr[2]/td[1]/text()'
        year = driver.find_element_by_xpath(year_path).text
        name_path = '//tr[' + str(i) + ']/td[2]'
        name = driver.find_element_by_xpath(name_path).text
        title_path = '//tr[' + str(i) + ']/td[3]'
        title = driver.find_element_by_xpath(title_path).text
        category_path = '//tr[' + str(i) + ']/td[4]'
        category = driver.find_element_by_xpath(category_path).text
        country_path = '//tr[' + str(i) + ']/td[5]'
        country = driver.find_element_by_xpath(country_path).text
        award_path = '//tr[' + str(i) + ']/td[8]'
        award = driver.find_element_by_xpath(award_path).text

        years.append(year)
        names.append(name)
        titles.append(title)
        categories.append(category)
        countries.append(country)
        awards.append(award)
        # print(i, year, name, title, award)
    if j != 92:
        print('page', j, 'is finished')
        try:
            driver.find_element_by_xpath('a[@class="paginate_button next"]').click()
            time.sleep(3)
            print(years, names, titles, categories, countries, awards)
        except Exception:
            print(j)
            driver.close()
            driver.quit()


driver.close()
driver.quit()


df_dict = {'years': years, 'names': names, 'titles': titles, 'categories': categories, 'countries': countries, 'awards': awards}
df = pd.DataFrame(df_dict)
df.to_excel('abstract.xlsx', sheet_name='data')

