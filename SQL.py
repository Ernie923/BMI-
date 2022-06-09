import sqlite3

def Database():
    # 檢查資料庫是否存在，若不存在則建立
    try:
        conn = sqlite3.connect('BMIDB.db')
        cur = conn.cursor()
        cur.execute(f"create table 'BMI明細'('編號'INTEGER,'帳號'TEXT NOT NULL,'BMI'REAL,PRIMARY KEY('編號'AUTOINCREMENT))")
        conn.commit()
        conn.close()
        conn = sqlite3.connect('BMIDB.db')
        cur = conn.cursor()
        cur.execute(f"create table '會員明細'('會員名稱'TEXT,'帳號'TEXT NOT NULL,'密碼'TEXT NOT NULL,'體重'REAL,'BMI'REAL,\
        PRIMARY KEY('帳號'))")
        conn.commit()
        conn.close()
    except:
        pass

def AccountExit(accountEntry):   #檢查帳號受否已被註冊
    # 從UI傳入帳號
    conn = sqlite3.connect('BMIDB.db')
    cur = conn.cursor()
    cur.execute(f"select * from 會員明細 where 帳號='{accountEntry}'")
    if cur.fetchone() is None:
        return 0
    conn.close()

def AccountCheck(nameEntry, accountEntry, passwordEntry):   #將註冊資訊寫入資料庫
    # 從UI傳入會員名稱，帳號，密碼
    conn = sqlite3.connect('BMIDB.db')
    cur = conn.cursor()
    # values = (nameEntry, accountEntry, passwordEntry)
    cur.execute(f"insert into 會員明細 (會員名稱,帳號,密碼) values ('{nameEntry}','{accountEntry}','{passwordEntry}')")
    conn.commit()
    conn.close()

def WriteToDB(weight, height, BMI, account):   #寫入按鈕功能
    # 從UI傳入體重、身高、BMI數值及帳號
    if weight != '' and height != '' and BMI != '':
        conn = sqlite3.connect('BMIDB.db')
        cur = conn.cursor()
        # cur.execute('update 會員明細 set 體重=%d,BMI=%d where 帳號=%s', (WeightEntry.get(), BMI.get(), memberAccount[0]))
        cur.execute(f"insert into BMI明細 (帳號,BMI) values ('{account}',{BMI})")
        conn.commit()
        conn.close()

def SearchGo(number, account):
    # 從UI查詢介面，傳入所選的筆數及帳號
    conn = sqlite3.connect('BMIDB.db')
    cur = conn.cursor()
    cur.execute(f"select * from BMI明細 where 帳號='{account}' order by 編號 desc LIMIT {number}")
    datalist = []  # 儲存讀取出來的各筆BMI值
    for i in cur.fetchall():
        datalist.append(round(i[2], 2))
    conn.close()
    return datalist

def MemberCheck(accountEntry):
    # 從登入UI，傳輸入的帳號
    # return 0 代表帳號不存在
    conn = sqlite3.connect('BMIDB.db')
    cur = conn.cursor()
    cur.execute(f"select * from 會員明細 where 帳號='{accountEntry}'")
    if cur.fetchone() is None:
        conn.close()
        return 0
    else:
        conn.close()

def MemberData(accountEntry):
    # 從登入UI，傳輸入的帳號
    # 傳回 name 用以改變UI介面
    conn = sqlite3.connect('BMIDB.db')
    cur = conn.cursor()
    cur.execute(f"select 會員名稱,帳號,密碼 from 會員明細 where 帳號='{accountEntry}'")
    name = cur.fetchone()
    conn.close()
    return name