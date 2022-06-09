import tkinter as tk
import BMI_Calculate
import SQL
from tkinter import messagebox
from tkinter import ttk

class BMI(tk.Tk):
    def __init__(self):
        super().__init__()

        # --視窗建立及初始設置 START--
        self.title('BMI測量')
        self.geometry('400x220+500+300')  #視窗寬400px 高200px 左上頂點座標設置在(500px,300px)
        self.resizable(0, 0)   #視窗不可調整大小
        # --視窗建立及初始設置 END --

        # --主框架設定 START--
        self.mainframe1 = tk.Frame(self)
        self.mainframe2 = tk.Frame(self)
        self.mainframe3 = tk.Frame(self)
        # --主框架設定 END--

        # --可變內容設定 START--
        self.BMI = tk.StringVar()
        self.Name = tk.StringVar()
        self.memberAccount = ()
        # --可變內容設定 END---

        # --登入狀態欄設置 START--
        self.titleFrame = tk.Frame(self.mainframe1)
        self.titleLabel = tk.Label(self.titleFrame, textvariable=self.Name, font=('arial', 14))
        self.Name.set('訪客您好，歡迎測試使用')
        self.titleLabel.pack()
        self.titleFrame.pack(side=tk.TOP)
        # --登入狀態欄設置 END---

        # --BMI資料輸入區設置 START--
        self.EnterFrame = tk.Frame(self.mainframe1)
        self.WeightLabel = tk.Label(self.EnterFrame, text='請輸入您的體重(公斤) :')
        self.HeightLabel = tk.Label(self.EnterFrame, text='請輸入您的身高(公分) :')
        self.WeightEntry = tk.Entry(self.EnterFrame, width=10, justify='center')
        self.HeightEntry = tk.Entry(self.EnterFrame, width=10, justify='center')
        self.WeightLabel.grid(row=0, column=0, padx=10, pady=5)
        self.HeightLabel.grid(row=1, column=0, padx=10, pady=5)
        self.WeightEntry.grid(row=0, column=1, padx=10, pady=5)
        self.HeightEntry.grid(row=1, column=1, padx=10, pady=5)
        self.EnterFrame.pack(side=tk.LEFT, padx=5, pady=5)
        # --BMI資料輸入區設置 END---

        # --BMI顯示區設置 START--
        self.ShowFrame = tk.Frame(self.mainframe1)
        self.ShowLabel1 = tk.Label(self.ShowFrame, text='您目前的BMI為', font=('Helvetica', 12), fg='blue')
        self.ShowLabel2 = tk.Label(self.ShowFrame, textvariable=self.BMI, bg='lightblue', width=10, font=('arial', 12))
        self.ShowLabel1.pack(side=tk.TOP, pady=5)
        self.ShowLabel2.pack(side=tk.TOP, pady=5)
        self.ShowFrame.pack(side=tk.TOP)
        # --BMI顯示區設置 END--

        # --輸入法提醒文字 START--
        self.NoteFrame = tk.Frame(self.mainframe2)
        self.NoteLabel = tk.Label(self.NoteFrame, text='◎ 需切換成英文輸入法，才能輸入小數點', font=('arial', 10), fg='red')
        self.NoteLabel.pack()
        self.NoteFrame.pack()
        # --輸入法提醒文字 END--

        # --按鈕設置區 START--
        self.CalButton = tk.Button(self.mainframe3, text='計算', command=self.BMICal)
        self.CalButton.grid(row=0, column=0, ipadx=5)

        self.ClearButton = tk.Button(self.mainframe3, text='清除', command=self.Clear)
        self.ClearButton.grid(row=0, column=1, ipadx=5)

        self.SighInButton = tk.Button(self.mainframe3, text='登入', command=self.SignInCheck)
        self.SighInButton.grid(row=0, column=2, ipadx=5)

        self.SighOutButton = tk.Button(self.mainframe3, text='登出', state='disabled', command=self.SignOutCheck)
        self.SighOutButton.grid(row=0, column=3, ipadx=5)

        self.RegisterButton = tk.Button(self.mainframe3, text='註冊', command=self.Regist)
        self.RegisterButton.grid(row=1, column=0, ipadx=5)

        self.WriteButton = tk.Button(self.mainframe3, text='寫入', state='disabled', command=self.WriteToDB)
        self.WriteButton.grid(row=1, column=1, ipadx=5)

        self.SearchButton = tk.Button(self.mainframe3, text='查詢', state='disabled', command=self.Search)
        self.SearchButton.grid(row=1, column=2, ipadx=5)
        # --按鈕設置區 END---

        # --主框架定位 START--
        self.mainframe1.pack(side=tk.TOP, padx=5, pady=5)
        self.mainframe2.pack(side=tk.TOP, padx=5, pady=5)
        self.mainframe3.pack(side=tk.TOP, padx=5, pady=5)
        # --主框架定位 END--

        # --資料庫建立 START --
        SQL.Database()
        # --資料庫建立 END --

    # --函式區 START--
    def BMICal(self):  # BMI計算以及彈跳視窗顯示結果
        try:
            weight = float(self.WeightEntry.get())
            height = float(self.HeightEntry.get())
            MyBMI = BMI_Calculate.BMICalculate(weight, height)
            self.BMI.set(MyBMI)
            if float(self.BMI.get()) < 18.5:
                messagebox.showinfo('計算結果', f'您有點過輕囉! 要注意營養!, 建議要增重{(18.5 * (height / 100) ** 2 - weight):2f}公斤')
            elif 18.5 <= float(self.BMI.get()) <= 24.0:
                messagebox.showinfo('計算結果', '標準體重! 請繼續保持!')
            else:
                messagebox.showinfo('計算結果', f'有點過重，建議要減重{(weight - 24.0 * (height / 100) ** 2):.2f}公斤')
        except:
            messagebox.showwarning('輸入錯誤', '請檢查身高及體重是否正確輸入數字')

    def Clear(self):  # 清除按鈕功能
        self.WeightEntry.delete(0, 'end')
        self.HeightEntry.delete(0, 'end')
        self.BMI.set('')

    def SignInCheck(self):  # 登入按鈕功能
        def check():
            if SQL.MemberCheck(AccountEntry.get()) == 0:
                messagebox.showwarning('檢查結果', '該帳號不存在')
            else:
                self.memberAccount += (SQL.MemberData(AccountEntry.get())[1],)
                if SQL.MemberData(AccountEntry.get())[1] == AccountEntry.get() and \
                        SQL.MemberData(AccountEntry.get())[2] == PasswordEntry.get():
                    self.Name.set(f'{SQL.MemberData(AccountEntry.get())[0]}，歡迎您再度回來')
                    self.titleLabel.config(fg='green')
                    self.SighInButton.config(state='disabled')
                    self.WriteButton.config(state='normal')
                    self.SighOutButton.config(state='normal')
                    self.SearchButton.config(state='normal')
                    self.RegisterButton.config(state='disabled')
                    Toplevel1.destroy()
                else:
                    messagebox.showwarning('檢查結果', '密碼輸入錯誤')

        def Cancel():
            Toplevel1.destroy()

        # --登入彈跳視窗 START--
        Toplevel1 = tk.Toplevel()
        Toplevel1.geometry('250x120+500+300')
        Toplevel1.resizable(0, 0)
        Toplevel1.title('登入作業')
        Toplevel1.transient(self)

        # --登入視窗UI START--
        AccountLabel = tk.Label(Toplevel1, text='請輸入您的帳號:')
        PasswordLabel = tk.Label(Toplevel1, text='請輸入您的密碼:')
        AccountEntry = tk.Entry(Toplevel1, width=10, justify='center')
        PasswordEntry = tk.Entry(Toplevel1, show='*', width=10, justify='center')
        AccountLabel.grid(row=0, column=0, padx=10, pady=5)
        PasswordLabel.grid(row=1, column=0, padx=10, pady=5)
        AccountEntry.grid(row=0, column=1, padx=10, pady=5)
        PasswordEntry.grid(row=1, column=1, padx=10, pady=5)
        YesButton = tk.Button(Toplevel1, text='確定', width=10, command=check)
        CancelButton = tk.Button(Toplevel1, text='取消', width=10, command=Cancel)
        YesButton.grid(row=2, column=0)
        CancelButton.grid(row=2, column=1)
        # --登入視窗UI END--
        # --登入彈跳視窗 END--

    def SignOutCheck(self):  # 登出按鈕功能
        self.Name.set('訪客您好，歡迎測試使用')
        self.titleLabel.config(fg='black')
        self.SighInButton.config(state='normal')
        self.WriteButton.config(state='disabled')
        self.SighOutButton.config(state='disabled')
        self.SearchButton.config(state='disabled')
        self.RegisterButton.config(state='normal')
        del self.memberAccount   #消除登入資訊
        self.memberAccount = ()  #重新建立登入資訊紀錄元組

    def Regist(self):  # 註冊按鈕功能
        import time

        # --註冊資訊輸入檢查 START--
        def Sure():
            if accountEntry.get() == '':
                messagebox.showwarning('', '請輸入帳號')
            elif passwordEntry.get() == '':
                messagebox.showwarning('', '請輸入密碼')
            elif passwordcheckEntry.get() == '':
                messagebox.showwarning('', '請再次輸入密碼')
            elif passwordEntry.get() != passwordcheckEntry.get():
                messagebox.showwarning('', '請確認密碼輸入一致')
            elif (accountEntry.get() != '') and (passwordEntry.get() != '') and (passwordEntry.get() == passwordcheckEntry.get()):
                if (SQL.AccountExit(accountEntry.get())) == 0:
                    time.sleep(2)  # 防止讀寫同時進行  造成data is locked
                    SQL.AccountCheck(nameEntry.get(), accountEntry.get(), passwordEntry.get())
                    messagebox.showinfo('註冊結果', '註冊完成，感謝您!')
                    MemberRegist.destroy()
                else:
                    messagebox.showinfo('註冊結果', '該帳號已存在!')
        # --註冊資訊輸入檢查 END--

        def Cancel():  # 取消註冊
            MemberRegist.destroy()

        # --註冊彈出視窗 START--
        MemberRegist = tk.Toplevel()
        MemberRegist.title('會員註冊')
        MemberRegist.geometry('350x400+800+150')
        MemberRegist.transient(self)

        # --註冊視窗UI START--
        memberlabel0 = tk.Label(MemberRegist, text='會員註冊資訊設定')
        memberlabel0.grid(row=0, column=0, pady=5)
        memberlabel1 = tk.Label(MemberRegist, text='1. 請輸入您的姓名或暱稱 (選填)', justify='left')
        memberlabel1.grid(row=1, column=0, pady=5)
        nameEntry = tk.Entry(MemberRegist, width=20, justify='center')
        nameEntry.grid(row=2, column=0, pady=5)
        memberlabel2 = tk.Label(MemberRegist, text='2. 請輸入帳號', justify='left')
        memberlabel2.grid(row=3, column=0, pady=5)
        memberlabel3 = tk.Label(MemberRegist, text='(*必填)', fg='red')
        memberlabel3.grid(row=3, column=1, pady=5)
        accountEntry = tk.Entry(MemberRegist, width=20, justify='center')
        accountEntry.grid(row=4, column=0, pady=5)
        memberlabel4 = tk.Label(MemberRegist)
        memberlabel4.grid(row=4, column=1, pady=5)
        memberlabel5 = tk.Label(MemberRegist, text='3. 請輸入密碼')
        memberlabel5.grid(row=5, column=0, pady=5)
        memberlabel6 = tk.Label(MemberRegist, text='(*必填)', fg='red')
        memberlabel6.grid(row=5, column=1, pady=5)
        passwordEntry = tk.Entry(MemberRegist, width=20, show='*', justify='center')
        passwordEntry.grid(row=6, column=0, pady=5)
        memberlabel7 = tk.Label(MemberRegist)
        memberlabel7.grid(row=6, column=1, pady=5)
        memberlabel8 = tk.Label(MemberRegist, text='4. 請再次確認密碼')
        memberlabel8.grid(row=7, column=0, pady=5)
        memberlabel9 = tk.Label(MemberRegist, text='(*必填)', fg='red')
        memberlabel9.grid(row=7, column=1, pady=5)
        passwordcheckEntry = tk.Entry(MemberRegist, width=20, show='*', justify='center')
        passwordcheckEntry.grid(row=8, column=0, pady=5)
        memberlabel10 = tk.Label(MemberRegist)
        memberlabel10.grid(row=8, column=1, pady=5)
        SureButton = tk.Button(MemberRegist, text='確定註冊', width=10, command=Sure)
        SureButton.grid(row=9, column=0, padx=5)
        CancelButton = tk.Button(MemberRegist, text='取消註冊', width=10, command=Cancel)
        CancelButton.grid(row=9, column=1, padx=5)
        # --註冊視窗UI END--
        # --註冊彈出視窗 END--

    def WriteToDB(self):  #BMI計算結果寫入資料庫
        if self.WeightEntry.get() != '' and self.HeightEntry.get() != '' and self.BMI.get() != '':
            SQL.WriteToDB(self.WeightEntry.get(), self.HeightEntry.get(), self.BMI.get(), self.memberAccount[0])
        else:
            messagebox.showwarning('寫入結果', '請確認數值是否輸入完成或是否計算完成')

    def Search(self):  # 查詢按鈕功能

        # 查詢功能變數設置
        value = tk.StringVar()
        # 最多可以查詢15筆BMI資料
        choice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        def SearchGo():  #確定查詢
            if len(SQL.SearchGo(int(NumberChoice.get()), self.memberAccount[0])) == 0:
                messagebox.showinfo('查詢結果', '查無資料')
            elif len(SQL.SearchGo(int(NumberChoice.get()), self.memberAccount[0])) < int(NumberChoice.get()):
                messagebox.showinfo('查詢結果', f'目前只有{len(SQL.SearchGo(int(NumberChoice.get()), self.memberAccount[0]))}\
筆資料，為{SQL.SearchGo(int(NumberChoice.get()), self.memberAccount[0])}')
            else:
                messagebox.showinfo('查詢結果', f'{SQL.SearchGo(int(NumberChoice.get()), self.memberAccount[0])}')

        def No():  #取消查詢
            Toplevel2.destroy()

        # --BMI歷史查詢彈掉視窗 START--
        Toplevel2 = tk.Toplevel()
        Toplevel2.title('個人BMI查詢')
        Toplevel2.geometry('250x100+500+300')
        Toplevel2.transient(self)
        frame1 = tk.Frame(Toplevel2)
        label1 = tk.Label(frame1, text='請選擇要查詢的近幾筆BMI資料筆數')
        label1.grid(row=0, column=0)
        NumberChoice = ttk.Combobox(frame1, textvariable=value, value=choice, width=6, justify='center')
        NumberChoice.current(choice[0])
        NumberChoice.grid(row=1, column=0)
        frame1.pack(padx=5, pady=5)
        frame2 = tk.Frame(Toplevel2)
        YesButton = tk.Button(frame2, text='確定', width=7, command=SearchGo)
        YesButton.grid(row=0, column=0, padx=5)
        NoButton = tk.Button(frame2, text='取消', width=7, command=No)
        NoButton.grid(row=0, column=1)
        frame2.pack(padx=5, pady=5)
        # --BMI歷史查詢彈掉視窗 END--

if __name__ == '__main__':
    bmi = BMI()
    bmi.mainloop()