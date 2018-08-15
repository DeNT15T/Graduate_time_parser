import mechanicalsoup
import requests

# 初始宣告
Name = input('教授名稱：')
Input_Student = int(input('參考最近碩士畢業生的數量：'))
Student = Input_Student
url = 'http://etd.lib.nctu.edu.tw/cgi-bin/gs32/tugsweb.cgi?o=dwebmge'

browser = mechanicalsoup.StatefulBrowser()
browser.open(url)
browser.select_form('form[name="main"]')
# 填入資料並開始搜尋
browser["qs0"] = Name
browser["dcf"] = "ad"
browser.submit_selected()

# 紀錄網址中的ccd項
ccd = browser.get_url()
ccd = ccd[56:62:]

# 根據畢業年遞減排序
browser.select_form('form[name="main"]')
browser["sortby"] = "-yr"
browser["SubmitChangePage"] = "1"
browser.submit_selected()

# 進入第一筆資料，並取得資料網址
enter = "cgi-bin/gs32/tugsweb.cgi/ccd=" + ccd + "/r"
browser.follow_link(enter.strip())
now = browser.get_url()

# Y2：兩年畢業、Y2_3：兩年以上三年以下畢業，以此類推；previous_number用來紀錄前一筆的學號
Y2, Y2_3, Y3_4, Y4_beyond, previous_number, i = (0, 0, 0, 0, 0, 0)

# 利用迴圈依序進入每一筆資料
#for i in range(1,Student+1):
while i < Student:
    i += 1
    now = now[:73] + str(i)
    browser.open(now.strip())
    access = browser.get_current_page()

    # 去除掉博士生資料
    degree = access.body.form.div.table.tbody.tr.td.table.find("th",text="學位類別:").find_next_sibling().get_text()
    if (degree == "博士"):
        Student += 1
        continue

    # 取得學號，並偵測第 i 筆資料是否已超過教授收過的學生量
    number = access.body.form.div.table.tbody.tr.td.table.find("th",text="學號:").find_next_sibling().get_text()
    if(previous_number == number):
        break
    else:
        previous_number = number

    # 取得畢業學年度
    grad_year = access.body.form.div.table.tbody.tr.td.table.find("th",text="畢業學年度:").find_next_sibling().get_text()

    # 過濾出學號中的入學年資訊
    number = number[0:2]
    if(number[0]=="0"):
        number = "1" + number

    # 畢業年 - 入學年
    calculate = int(grad_year) - int(number)
    if calculate == 1:
        Y2 += 1
    elif calculate == 2:
        Y2_3 += 1
    elif calculate == 3:
        Y3_4 += 1
    else:
        Y4_beyond += 1

print("最近", Input_Student, "筆碩士畢業生紀錄中")
print(Y2, "位準時兩年畢業")
print(Y2_3, "位兩到三年畢業")
print(Y3_4, "位三到四年畢業")
print(Y4_beyond, "位四年以上畢業")
