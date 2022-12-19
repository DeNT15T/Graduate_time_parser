from controller import lab_census_system
from controller import verbose

if __name__=="__main__":
    # handle user input
    school = input('欲查詢學校[1.交大 2.中央 3.清大 4.陽明]，輸入數字：')
    name = input('教授名稱：')
    sample_count = int(input('參考最近碩士畢業生的數量：'))
    filter_cnt = input('欲過濾的系所數量（選填）：')

    LCS = lab_census_system.LabCensusSystem(school, name, sample_count, filter_cnt)
    verbose_input = LCS.Search()
    res = LCS.Show()
    print(f"最近 {str(sample_count)} 筆碩士畢業生紀錄中")
    print(f"{res[0]}\t位第一年畢業")
    print(f"{res[1]}\t位第二年畢業")
    print(f"{res[2]}\t位第三年畢業")
    print(f"{res[3]}\t位第四年畢業")
    print(f"{res[4]}\t位第五年以上畢業")
    # 顯示口試時間詳情（將i代替Student傳入，藉此減少多餘搜尋的工作量）
#    verbose.show(LCS.name, LCS.sample_count, LCS.result)
    V = verbose.VerboseBooster(name, sample_count, res, verbose_input)
    V.show()
