from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time


#创建csv文件表头信息
def new_csv_key(id,value):
    with open('jijin/'+id+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['data', id])
        date = 1
        for i in value:
            writer.writerow([date, i])
            date = date + 1


#创建csv文件内容
def add_csv_value():
    pass

#爬取内容
def main_crype(driver):
    driver.get('http://fund.jd.com/')
    elem = driver.find_element_by_xpath("//div[@class='sort-btn one-month'][@data-sortid='3,4'][@data-sorttype='3']")
    elem.click()
    time.sleep(2)

    cur_pg = 1
    # go_to_page(driver, 187)

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


def crype_value(url):
    driver = webdriver.Firefox()
    url = 'http:'+url
    driver.get(url)
    sp = BeautifulSoup(driver.page_source, 'lxml')
    pg_num = 0
    for a in sp.find_all('a'):
        try:
            temp_page = a.attrs.get('data-target')
            if temp_page is None:
                temp_page = 0
            else:
                temp_page = int(temp_page)
        except Exception as e:
            temp_page = 0
        if temp_page > pg_num:
            pg_num = temp_page
    elem = driver.find_element_by_xpath("//a[@data-target='"+str(pg_num)+"']")
    elem.click()
    val = []
    while True:
        temp_val = []
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tbody = 0
        for td in soup.find_all('tbody'):
            tbody = td
        for tr in tbody.find_all('tr'):
            cnt = 0
            for td in tr.find_all('td'):
                if cnt == 1:
                    temp_val.append(td.string)
                    break
                cnt = cnt + 1
        print('已经爬完'+str(pg_num)+'号页面')
        temp_val.reverse()
        val.extend(temp_val)
        try:
            elem = driver.find_element_by_xpath("//a[@class='up-page']")
            elem.click()
            pg_num = pg_num - 1
        except Exception as e:
            print(e)
            break
    driver.quit()
    return val


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
