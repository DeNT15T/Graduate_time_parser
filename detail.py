import mechanicalsoup

# data用來紀錄學生姓名、L串列紀錄各畢業時間的入學年與口試日期
data={}
L1, L2, L2_3, L3_4, L4_beyond = ([],[],[],[],[])


def show(Name, Student, Y1, Y2, Y2_3, Y3_4, Y4_beyond):
    print("--------------Detail searching...-------------")

    # 開啟url
    url = 'https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    browser.select_form('form[name="main"]')

    # 填入資料並開始搜尋
    browser["qs0"] = Name
    browser["dcf"] = "ad"
    browser.submit_selected()
    
    # 紀錄網址中的ccd項
    ccd = browser.get_url()
    ccd = ccd[52:58:]

    # 根據畢業年遞減排序
    browser.select_form('form[name="main"]')
    browser["sortby"] = "-yr"
    browser["SubmitChangePage"] = "1"

    # 進入第一筆資料，並取得資料網址
    enter = "/cgi-bin/gs32/gsweb.cgi/ccd=" + ccd + "/record"
    browser.follow_link(enter.strip())
    now = browser.get_url()
    
    # 迴圈控制變數宣告
    i = 0

    # 利用迴圈依序進入每一筆資料
    while  i < Student:
        i += 1
        now = now[:69] + str(i)
        browser.open(now.strip())
        access = browser.get_current_page()

        # 取得學生名字，若學生名字存在data字典中，嘗試取得口試日期
        student_name = access.body.form.div.table.tbody.tr.td.table.find("th",text="研究生:").find_next_sibling().get_text()
        if student_name in data:
            try:
                oral_defense = access.body.form.div.table.tbody.tr.td.table.find("th",text="口試日期:").find_next_sibling().get_text()
                # 於data的對應key中加入口試日期，並將入學年以西元年表示，轉成string
                data[student_name].append(oral_defense)
                data[student_name][0] += 1911
                data[student_name][0] = str(data[student_name][0])+"年"

                # 依照value中的畢業時間資訊分類至對應的L串列中
                if data[student_name][1] == "1":
                    L1.append([data[student_name][0],data[student_name][2]])
                elif data[student_name][1] == "2":
                    L2.append([data[student_name][0],data[student_name][2]])
                elif data[student_name][1] == "2_3":
                    L2_3.append([data[student_name][0],data[student_name][2]])
                elif data[student_name][1] == "3_4":
                    L3_4.append([data[student_name][0],data[student_name][2]])
                elif data[student_name][1] == "4_beyond":
                    L4_beyond.append([data[student_name][0],data[student_name][2]])

            # 若口試日期取得失敗，繼續迴圈
            except AttributeError:
                continue



    # 輸出結果
    print("天才一年畢業的", Y1, "位學生中：")
    if(L1 != []):
        for time in L1:
            print("1位學生於", time[0], "入學，於", time[1], "進行口試")
    else:
        print("無資料")

    print("準時兩年畢業的", Y2, "位學生中：")
    if(L2 != []):
        for time in L2:
            print("1位學生於", time[0], "入學，於", time[1], "進行口試")
    else:
        print("無資料")
    print("兩到三年畢業的", Y2_3, "位學生中：")
    if(L2_3 != []):
        for time in L2_3:
            print("1位學生於", time[0], "入學，於", time[1], "進行口試")
    else:
        print("無資料")
    print("三到四年畢業的", Y3_4, "位學生中：")
    if(L3_4 != []):
        for time in L3_4:
            print("1位學生於", time[0], "入學，於", time[1], "進行口試")
    else:
        print("無資料")
    print("四年以上畢業的", Y4_beyond, "位學生中：")
    if(L4_beyond != []):
        for time in L4_beyond:
            print("1位學生於", time[0], "入學，於", time[1], "進行口試")
    else:
        print("無資料")
