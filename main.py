import mechanicalsoup
import requests

Name = input('教授名稱：')
Student = int(input('參考的最近研究生數量：'))
print('您要找的是', Name, '參考的研究生為最近的', Student, '個')

years = [Student]

url = 'http://etd.lib.nctu.edu.tw/cgi-bin/gs32/tugsweb.cgi?o=dwebmge'
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)
browser.select_form('form[name="main"]')
browser["qs0"] = Name
browser["dcf"] = "ad"
browser.submit_selected()   # 開始查詢

# 紀錄網址中的ccd項
temp = browser.get_url()
code = temp[56:62:]

# descent sort by graduate year && show newest 100 datas
browser.select_form('form[name="main"]')
browser["jpsize"] = "100"
browser["sortby"] = "-yr"
browser["SubmitChangePage"] = "1"
browser.submit_selected()


# 進入第一項
enter = "cgi-bin/gs32/tugsweb.cgi/ccd=" + code + "/r"
browser.follow_link(enter.strip())
now = browser.get_url()


# 遞迴找出下一項
for i in range(1,Student+1):
    now = now[:73] + str(i)
    print(now)
    browser.open(now.strip())
    # Next：想辦法取出學號、畢業年份資訊並計算
    access = browser.get_current_page()
    print(i)
    print(access.body.form.div.table.tbody.tr.td.table.find("th",text="學號:").find_next_sibling().get_text())
    print(access.body.form.div.table.tbody.tr.td.table.find("th",text="畢業學年度:").find_next_sibling().get_text())
