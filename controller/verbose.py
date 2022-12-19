import mechanicalsoup


class VerboseBooster:
    def __init__(self, name, sample_count, res, verbose_input):
        # data用來紀錄學生姓名、L串列紀錄各畢業時間的入學年與口試日期
        self.name = name
        self.sample_count = sample_count
        self.res = res
        self.students = verbose_input
        self.L1, self.L2, self.L3, self.L4, self.L5 = ([],[],[],[],[])

    def show(self):
        print("--------------Detail searching...-------------")

        # 開啟url
        url = 'https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)
        browser.select_form('form[name="main"]')

        # 填入資料並開始搜尋
        browser["qs0"] = self.name
        browser["dcf"] = "ad"
        browser.submit_selected()
        
        # 紀錄網址中的ccd項
        ccd = browser.get_url()
        ccd = ccd[52:58:]

        # 根據畢業年遞減排序
        try:
            browser.select_form('form[name="main"]')
        except LinkNotFoundError:
            print("系統過載，請稍後再試")
        browser["sortby"] = "-yr"
        browser["SubmitChangePage"] = "1"

        # 進入第一筆資料，並取得資料網址
        enter = f"/cgi-bin/gs32/gsweb.cgi/ccd={ccd}/record"
        browser.follow_link(enter.strip())
        now = browser.get_url()
        
        # 迴圈控制變數宣告
        i = 0

        # 利用迴圈依序進入每一筆資料
        while  i < self.sample_count:
            i += 1
            now = now[:69] + str(i)
            browser.open(now.strip())
            access = browser.get_current_page()

            # 取得學生名字，若學生名字存在data字典中，嘗試取得口試日期
            student_name = access.body.form.div.table.tbody.tr.td.table.find("th", text="研究生:").find_next_sibling().get_text()
            if student_name in self.students:
                try:
                    oral_defense = access.body.form.div.table.tbody.tr.td.table.find("th", text="口試日期:").find_next_sibling().get_text()
    #                oral_defense = ''.join(c for c in oral_defense if c.isdigit())
                    # 於data的對應key中加入口試日期，並將入學年以西元年表示，轉成string
                    self.students[student_name].append(oral_defense)
                    self.students[student_name][0] = f"{str(int(self.students[student_name][0])+1911)} 年"

                    # 依照value中的畢業時間資訊分類至對應的L串列中
                    if self.students[student_name][1] == "1":
                        self.L1.append([self.students[student_name][0], self.students[student_name][2]])
                    elif self.students[student_name][1] == "2":
                        self.L2.append([self.students[student_name][0], self.students[student_name][2]])
                    elif self.students[student_name][1] == "2_3":
                        self.L3.append([self.students[student_name][0], self.students[student_name][2]])
                    elif self.students[student_name][1] == "3_4":
                        self.L4.append([self.students[student_name][0], self.students[student_name][2]])
                    elif self.students[student_name][1] == "4_beyond":
                        self.L5.append([self.students[student_name][0], self.students[student_name][2]])

                # 若口試日期取得失敗，繼續迴圈
                except AttributeError:
                    continue



        # 輸出結果
        print(f"第一年畢業的 {self.res[0]} 位學生中：")
        if(self.L1 != []):
            for time in self.L1:
                print(f"曾有人於 {time[0]} 入學，於 {time[1]} 進行口試")
        else:
            print("無資料")

        print(f"第二年畢業的 {self.res[1]} 位學生中：")
        if(self.L2 != []):
            for time in self.L2:
                print(f"曾有人於 {time[0]} 入學，於 {time[1]} 進行口試")
        else:
            print("無資料")
        print(f"第三年畢業的 {self.res[2]} 位學生中：")
        if(self.L3 != []):
            for time in self.L3:
                print(f"曾有人於 {time[0]} 入學，於 {time[1]} 進行口試")
        else:
            print("無資料")
        print(f"第四年畢業的 {self.res[3]} 位學生中：")
        if(self.L4 != []):
            for time in self.L4:
                print(f"曾有人於 {time[0]} 入學，於 {time[1]} 進行口試")
        else:
            print("無資料")
        print(f"第五年以上畢業的 {self.res[4]} 位學生中：")
        if(self.L5 != []):
            for time in self.L5:
                print(f"曾有人於 {time[0]} 入學，於 {time[1]} 進行口試")
        else:
            print("無資料")
