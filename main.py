import mechanicalsoup
import id_converter
import detail

class LabCensusSystem:
    def __init__(self):
        # handle user input
        self.school = input('欲查詢學校[1.交大 2.中央 3.清大 4.陽明]，輸入數字：')
        self.name = input('教授名稱：')
        self.sample_count = int(input('參考最近碩士畢業生的數量：'))

        # set filter
        cnt = input('欲過濾的系所數量（選填）：')
        self.filter = []
        cnt = 0 if(cnt=='') else int(cnt)
        while cnt:
            self.filter.append(input('過濾系所：'))
            cnt -= 1

        self.result = [0,0,0,0,0]

    def Search(self):
        print("-----------------Searching...-----------------")

        # 開啟url
        url = 'http://etd.lib.nctu.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)
        browser.select_form('form[name="main"]')

        # 填入資料並開始搜尋
        browser["qs0"] = self.name
        browser["dcf"] = "ad"
        browser["limitdb"] = int(self.school)-1
        browser.submit_selected()

        # 紀錄網址中的ccd項
        ccd = browser.get_url()
        ccd = ccd[54:60:]

        # 根據畢業年遞減排序
        browser.select_form('form[name="main"]')
        browser["sortby"] = "-yr"
        # browser["SubmitChangePage"] = "1"

        # 進入第一筆資料，並取得資料網址
        enter = f"/cgi-bin/gs32/gsweb.cgi/ccd={ccd}/record"
        browser.follow_link(enter.strip())
        now = browser.get_url()

        # Y2：兩年畢業、Y2_3：兩年以上三年以下畢業，以此類推；previous_number用來紀錄前一筆的學號
        previous_number, i = 0, 0

        # 檢查無窮迴圈用的變數
        diff_odd, diff_even, check = (0, 0, 0)

        # 迴圈依序進入每一筆資料
        cnt = self.sample_count
        while i < cnt:
            i += 1
            now = now[:71] + str(i)
            browser.open(now.strip())
            access = browser.get_current_page()

            # 避免過度過濾導致無窮迴圈

            if(i%2==1):
                diff_odd = cnt - i
            else:
                diff_even = cnt - i
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
                cnt += 1
                continue

            # 過濾系所
            Department = access.body.form.div.table.tbody.tr.td.table.find("th",text="系所名稱:").find_next_sibling().get_text()
            if(Department in self.filter):
                cnt += 1
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
            if(self.school == "1"):
                enter_year = id_converter.NCTU(number)
            elif(self.school == "2"):
                enter_year = id_converter.NCU(number)
            elif(self.school == "3"):
                enter_year = id_converter.NTHU(number)
            elif(self.school == "4"):
                enter_year = id_converter.NYMU(number)

            # 畢業生名字
            try:
                student_name = access.body.form.div.table.tbody.tr.td.table.find("th",text="作者:").find_next_sibling().get_text()
            except AttributeError:
                student_name = access.body.form.div.table.tbody.tr.td.table.find("th",text="作者(中文):").find_next_sibling().get_text()
            # 畢業年 - 入學年
            calculate = int(grad_year) - int(enter_year)
            if calculate == 0:
                self.result[0] += 1
                new = {student_name:[int(enter_year),"1"]}
            elif calculate == 1:
                self.result[1] += 1
                new = {student_name:[int(enter_year),"2"]}
            elif calculate == 2:
                self.result[2] += 1
                new = {student_name:[int(enter_year),"2_3"]}
            elif calculate == 3:
                self.result[3] += 1
                new = {student_name:[int(enter_year),"3_4"]}
            else:
                self.result[4] += 1
                new = {student_name:[int(enter_year),"4_beyond"]}

            # dict(data) = { key(學生名字):value[入學年, 畢業時間] }
            detail.data.update(new)

    def Show(self):
        print(f"最近 {str(self.sample_count)} 筆碩士畢業生紀錄中")
        print(f"{self.result[0]}\t位第一年畢業")
        print(f"{self.result[1]}\t位第二年畢業")
        print(f"{self.result[2]}\t位第三年畢業")
        print(f"{self.result[3]}\t位第四年畢業")
        print(f"{self.result[4]}\t位第五年以上畢業")

if __name__=="__main__":
    LCS = LabCensusSystem()
    LCS.Search()
    LCS.Show()
    # 顯示口試時間詳情（將i代替Student傳入，藉此減少多餘搜尋的工作量）
    detail.show(LCS.name, LCS.sample_count, LCS.result)
