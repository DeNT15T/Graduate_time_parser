import mechanicalsoup
import student_id
import detail

# 初始宣告
School = input('欲查詢學校[1.交大 2.中央 3.清大 4.陽明]，輸入數字：')
Name = input('教授名稱：')
Input_Student = int(input('參考最近碩士畢業生的數量：'))
Student = Input_Student

# 系所過濾
Filter_Count = input('欲過濾的系所數量（選填）：')
Filter = []
if(Filter_Count == ''):
    Filter_Count = 0
else:
    Filter_Count = int(Filter_Count)
while Filter_Count:
    Filter.append(input('過濾系所：'))
    Filter_Count -= 1

print("-----------------Searching...-----------------")

# 開啟url
url = 'http://etd.lib.nctu.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)
browser.select_form('form[name="main"]')

# 填入資料並開始搜尋
browser["qs0"] = Name
browser["dcf"] = "ad"
browser["limitdb"] = int(School)-1
browser.submit_selected()

# 紀錄網址中的ccd項
ccd = browser.get_url()
ccd = ccd[54:60:]

# 根據畢業年遞減排序
browser.select_form('form[name="main"]')
browser["sortby"] = "-yr"
browser["SubmitChangePage"] = "1"
browser.submit_selected()

# 進入第一筆資料，並取得資料網址
enter = "/cgi-bin/gs32/gsweb.cgi/ccd=" + ccd + "/record"
browser.follow_link(enter.strip())
now = browser.get_url()

# Y2：兩年畢業、Y2_3：兩年以上三年以下畢業，以此類推；previous_number用來紀錄前一筆的學號
Y1, Y2, Y2_3, Y3_4, Y4_beyond, previous_number, i = (0, 0, 0, 0, 0, 0, 0)

# 檢查無窮迴圈用的變數
diff_odd, diff_even, check = (0, 0, 0)

# 利用迴圈依序進入每一筆資料
while i < Student:
    i += 1
    now = now[:71] + str(i)
    browser.open(now.strip())
    access = browser.get_current_page()

    # 避免過度過濾導致無窮迴圈
    if(i%2==1):
        diff_odd = Student - i
    else:
        diff_even = Student - i
    if(diff_odd == diff_even):
        check += 1
    else:
        check = 0
    if(check == 30):
        i -= 30
        break

    # 過濾博士生資料
    degree = access.body.form.div.table.tbody.tr.td.table.find("th",text="學位類別:").find_next_sibling().get_text()
    if (degree == "博士"):
        Student += 1
        continue

    # 過濾系所
    Department = access.body.form.div.table.tbody.tr.td.table.find("th",text="系所名稱:").find_next_sibling().get_text()
    if(Department in Filter):
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
    if(School == "1"):
        enter_year = student_id.NCTU(number)
    elif(School == "2"):
        enter_year = student_id.NCU(number)
    elif(School == "3"):
        enter_year = student_id.NTHU(number)
    elif(School == "4"):
        enter_year = student_id.NYMU(number)

    # 畢業生名字
    try:
        student_name = access.body.form.div.table.tbody.tr.td.table.find("th",text="作者:").find_next_sibling().get_text()
    except AttributeError:
        student_name = access.body.form.div.table.tbody.tr.td.table.find("th",text="作者(中文):").find_next_sibling().get_text()
    # 畢業年 - 入學年
    calculate = int(grad_year) - int(enter_year)
    if calculate == 0:
        Y1 += 1
        new = {student_name:[int(enter_year),"1"]}
    elif calculate == 1:
        Y2 += 1
        new = {student_name:[int(enter_year),"2"]}
    elif calculate == 2:
        Y2_3 += 1
        new = {student_name:[int(enter_year),"2_3"]}
    elif calculate == 3:
        Y3_4 += 1
        new = {student_name:[int(enter_year),"3_4"]}
    else:
        Y4_beyond += 1
        new = {student_name:[int(enter_year),"4_beyond"]}

    # dict(data) = { key(學生名字):value[入學年, 畢業時間] }
    detail.data.update(new)

print("最近", Input_Student, "筆碩士畢業生紀錄中")
print(Y1, "位天才一年畢業")
print(Y2, "位準時兩年畢業")
print(Y2_3, "位兩到三年畢業")
print(Y3_4, "位三到四年畢業")
print(Y4_beyond, "位四年以上畢業")

# 顯示口試時間詳情（將i代替Student傳入，藉此減少多餘搜尋的工作量）
detail.show(Name, i, Y1, Y2, Y2_3, Y3_4, Y4_beyond)
