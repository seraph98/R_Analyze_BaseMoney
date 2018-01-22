from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
from util.base.base_util import crype_value


# 对外提供方法:
# 1. get_500_data(id)  id为基金编号, 根据基金的编号返回list数组, 数组内是tuple元组(data, value). 从当日往前500天内的数据
# 2. update_data(id)    id为基金编号, 更新基金数据. 一直更新到当前日期.


def get_500_data(id):
    href = 'http://fund.jd.com/detail/'+str(id)+'.html'
    return crype_value(href)


def update_data(id):
    pass


#创建csv文件表头信息
def new_csv_key(id,value):
    with open('jijin/'+id+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['data', id])
        date = 1
        for i in value:
            writer.writerow([date, i])
            date = date + 1


#爬取内容
def main_crype(driver):
    driver.get('http://fund.jd.com/')
    elem = driver.find_element_by_xpath("//div[@class='sort-btn one-month'][@data-sortid='3,4'][@data-sorttype='3']")
    elem.click()
    time.sleep(2)
    cur_pg = 1
    while True:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tbody = soup.tbody
        for tr in tbody.children:
            td = tr.td
            a = td.a
            span = td.span
            name = a.attrs['title']
            href = a.attrs['href']
            loc = span.string
            id = name+'('+loc+')'
            val = crype_value(href)
            new_csv_key(id,val)
            break
        try:
            cur_pg = cur_pg + 2
            elem = driver.find_element_by_xpath("//a[@data-target='"+str(cur_pg)+"']")
            elem.click()
        except Exception as e:
            print(e)
        break





def go_to_page(driver, page):
    cur_pg = 1
    while cur_pg != page:
        cur_pg = cur_pg + 2
        elem = driver.find_element_by_xpath("//a[@data-target='"+str(cur_pg)+"']")
        elem.click()
        time.sleep(2)


if __name__ == '__main__':
    driver = webdriver.Firefox()
    main_crype(driver)
    driver.quit()
