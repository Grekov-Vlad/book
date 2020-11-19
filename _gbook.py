import json
from datetime import datetime
from http import cookies
import time


class Gbook:
    LOGIN = "admin"
    PASSWORD = "pass@word1"
    TMP_LOGFORM = "logform.tmp"
    TMP_FORM = "form.tmp"
    TMP_CONTENT = "content.tmp"
    TMP_MESSAGE = "message.tmp"
    DB = "messages.json"
    def __init__(self):
        self.messages = ""
        self.form = ""
        self.content = ""
        self.logform = ""
        
        with open(self.TMP_FORM,"r", encoding="utf-8") as f:
            self.form = f.read()
        with open(self.TMP_CONTENT,"r", encoding="utf-8") as f:
            self.content = f.read()
        with open(self.TMP_LOGFORM,"r", encoding="utf-8") as f:
            self.logform = f.read()
        try:
            with open(self.DB,"r", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            with open(self.DB,"w", encoding="utf-8") as f:
                json.dump({},f)
            
    def read_msgs(self,admin):
        with open(self.DB, "r", encoding="utf-8") as f:
            m = json.load(f)
        if not m:
            self.messages = "Записей нет!"
            return
        with open(self.TMP_MESSAGE, "r", encoding="utf-8") as f:
            pattern = f.read()
        for id in sorted(m.keys(), reverse=True):
            date = datetime.fromtimestamp(int(id)).strftime('%d-%m-%Y %H:%M')
            self.messages += pattern.format(msg=m[id]["msg"], datetime=date,name=m[id]["name"],email=m[id]["email"])
            if admin:
                self.messages += "<p><a href='index.py?del={}'>Удалить</a></p>".format(id)
            
    def save_msgs(self,name,email,msg):
        ts = int(time.time())
        with open(self.DB,"r", encoding="utf-8") as f:
            m = json.load(f)
        m[ts] = {"name":name,"email":email,"msg":msg}
        with open(self.DB,"w", encoding="utf-8") as f:
            json.dump(m,f)

    def delete_msg(self,id):
        with open(self.DB, "r", encoding="utf-8") as f:
            m = json.load(f)
        del m[id]
        with open(self.DB, "w", encoding="utf-8") as f:
            json.dump(m,f)

    def login(self,login,password):
        if login == self.LOGIN and password == self.PASSWORD:
            cookie = cookies.SimpleCookie()
            cookie["admin"] = "1"
            cookie["admin"]["httponly"] = 1
            print(cookie.output())
            return True
        return False

    def logout(self):
            cookie = cookies.SimpleCookie()
            cookie["admin"] = "0"
            cookie["admin"]["httponly"] = 1
            exp = time.gmtime(time.time() - 3600)
            exp = time.strftime("%a, %d, %b %Y %T GMT", exp)
            cookie["admin"]["expires"] = exp
            print(cookie.output())
