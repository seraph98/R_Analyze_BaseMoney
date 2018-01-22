from selenium import webdriver
from bs4 import BeautifulSoup


# 底层设计, 不参与接口的暴露
def crype_value(url, count=500):
    # count 记录统计的个数, 默认500个
    driver = webdriver.Firefox()
    driver.get(url)
    sp = BeautifulSoup(driver.page_source, 'lxml')
    pg_num = 1
    elem = driver.find_element_by_xpath("//a[@data-target='"+str(pg_num)+"']")
    elem.click()
    val = []
    total_count = 0
    while True:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tbody = 0
        if total_count >= count:
            break
        for td in soup.find_all('tbody'):
            tbody = td
        for tr in tbody.find_all('tr'):
            cnt = 0
            for td in tr.find_all('td'):
                if cnt == 0:
                    dt = td.string.replace('-','')
                if cnt == 1:
                    value = float(td.string)
                    break
                cnt = cnt + 1
            val.extend((dt, value))
            total_count += 1
        print('已经爬完'+str(pg_num)+'号页面')
        try:
            elem = driver.find_element_by_xpath("//a[@class='down-page']")
            elem.click()
            pg_num = pg_num + 1
        except Exception as e:
            print(e)
            break
    driver.quit()
    return val