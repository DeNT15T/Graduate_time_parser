import mechanicalsoup

import Detail
from Student_id import NumberCalculator


# 初始宣告, 檢驗值合不合理
school = int(input('欲查詢學校[0.交大 1.中央 2.清大 3.陽明]，輸入數字：'))
professor_name = input('教授名稱：')
num_of_students = int(input('參考最近碩士畢業生的數量：'))
if professor_name is '' or school < 0 or school >= 4:
    raise ValueError

# 系所過濾
input_str = input('欲過濾的系所數量（選填）：')
filter_count = 0 if input_str is '' else int(input_str)
del input_str

Filter = []
for i in range(filter_count):
    Filter.append(input('過濾系所：'))

# 開始搜尋
print("-----------------Searching...-----------------")

# 開啟url
url = 'http://etd.lib.nctu.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)
browser.select_form('form[name="main"]')

# 填入資料並開始搜尋
browser["qs0"] = professor_name
browser["dcf"] = "ad"
browser["limitdb"] = school
browser.submit_selected()

# 根據畢業年遞減排序
browser.select_form('form[name="main"]')
browser["sortby"] = "-yr"
browser["SubmitChangePage"] = "1"
browser.submit_selected()

# 紀錄網址中的ccd項
ccd = browser.get_url()[54:60:]

# 進入第一筆資料，並取得資料網址
enter = "/cgi-bin/gs32/gsweb.cgi/ccd=" + ccd + "/record"
browser.follow_link(enter.strip())
current_url = browser.get_url()
previous_number, i = 0, 0
lookup_table = {'Y1'       : 0,
                'Y2'       : 0,
                'Y2_3'     : 0,
                'Y3_4'     : 0,
                'Y4_beyond': 0}

# 檢查無窮迴圈用的變數
diff_odd, diff_even, check = (0, 0, 0)

# 利用迴圈依序進入每一筆資料
Student = num_of_students

while i < Student:
    i += 1
    current_url = current_url[:71] + str(i)
    browser.open(current_url.strip())
    access = browser.get_current_page()

    # 避免過度過濾導致無窮迴圈
    if i % 2 is 1:
        diff_odd = Student - i
    else:
        diff_even = Student - i

    if diff_odd is diff_even:
        check += 1
    else:
        check = 0

    if check is 30:
        i -= 30
        break

    # 過濾博士生資料
    degree = access.body.form.div.table.tbody.tr.td.table.find("th", text="學位類別:").find_next_sibling().get_text()
    if degree is "博士":
        Student += 1
        continue

    # 過濾系所
    Department = access.body.form.div.table.tbody.tr.td.table.find("th", text="系所名稱:").find_next_sibling().get_text()
    if Department in Filter:
        Student += 1
        continue

    # 取得學號，並偵測第 i 筆資料是否已超過教授收過的學生量
    number = access.body.form.div.table.tbody.tr.td.table.find("th", text="學號:").find_next_sibling().get_text()
    if previous_number is number:
        break
    else:
        previous_number = number

    # 取得畢業學年度
    grad_year = access.body.form.div.table.tbody.tr.td.table.find("th", text="畢業學年度:").find_next_sibling().get_text()

    # 過濾出學號中的入學年資訊
    admission_year = NumberCalculator(school).get_number(number)

    # 畢業生名字
    try:
        student_name = access.body.form.div.table.tbody.tr.td.table.find("th",
                text="作者:").find_next_sibling().get_text()
    except AttributeError:
        student_name = access.body.form.div.table.tbody.tr.td.table.find("th",
                text="作者(中文):").find_next_sibling().get_text()

    # 畢業年 - 入學年
    calculate = int(grad_year) - int(admission_year)
    calculate_to_year = {0: 'Y1', 1: 'Y2', 2: 'Y2_3', 3: 'Y3_4'}

    # 下面這一行用 .get 代表說如果查找失敗回傳回'Y4_beyond'，就是原本code裡面的'else'部分。
    lookup_table[calculate_to_year.get(calculate, "Y4_beyond")] += 1
    new = {student_name: [int(admission_year), calculate_to_year.get(calculate, "Y4_beyond")[1:]]}

    # dict(data) = { key(學生名字):value[入學年, 畢業時間] }
    Detail.data.update(new)

print("最近", num_of_students, "筆碩士畢業生紀錄中")
print(lookup_table['Y1'], "位天才一年畢業")
print(lookup_table['Y2'], "位準時兩年畢業")
print(lookup_table['Y2_3'], "位兩到三年畢業")
print(lookup_table['Y3_4'], "位三到四年畢業")
print(lookup_table['Y4_beyond'], "位四年以上畢業")

# 顯示口試時間詳情（將i代替Student傳入，藉此減少多餘搜尋的工作量）
Detail.show(professor_name, i, **lookup_table)
