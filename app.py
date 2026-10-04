import os, sqlite3, secrets, string
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
DB = os.environ.get("DATABASE_PATH", "data.db")
PREFIX = "ABDOUUU-HUSENG-VPS-"
ADMIN_PATH = "abdouuu-vps-cod"

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con=db()
    con.execute("""CREATE TABLE IF NOT EXISTS codes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        max_users INTEGER NOT NULL,
        used_users INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1
    )""")
    con.commit(); con.close()

def make_code():
    alphabet=string.ascii_uppercase+string.digits
    return PREFIX + "-".join("".join(secrets.choice(alphabet) for _ in range(5)) for _ in range(3))

def valid_code(code):
    con=db()
    row=con.execute("SELECT * FROM codes WHERE code=? AND active=1",(code.strip(),)).fetchone()
    if not row:
        con.close(); return False, "الكود غير موجود أو تم تعطيله"
    if datetime.fromisoformat(row["expires_at"]) <= datetime.now(timezone.utc):
        con.close(); return False, "انتهت مدة الكود"
    if row["used_users"] >= row["max_users"]:
        con.close(); return False, "وصل الكود إلى الحد الأقصى للمستخدمين"
    con.close(); return True, "الكود صالح"

@app.route("/")
def index(): return render_template("index.html", name="𝔸𝔹𝔻𝕆𝕌𝕌𝕌 ℍ𝕌𝕊𝔼ℕ𝔾 𝕍ℙ𝕊")

@app.post("/api/verify")
def verify():
    data=request.get_json(silent=True) or {}
    code=str(data.get("code","")).strip()
    ok,msg=valid_code(code)
    if ok:
        con=db()
        con.execute("UPDATE codes SET used_users=used_users+1 WHERE code=?",(code,))
        con.commit(); con.close()
        session["licensed"]=True
        return jsonify(ok=True, message="تم التحقق من الكود بنجاح")
    return jsonify(ok=False, message=msg), 400

@app.route("/dashboard")
def dashboard():
    if not session.get("licensed"): return redirect(url_for("index"))
    return render_template("dashboard.html", name="𝔸𝔹𝔻𝕆𝕌𝕌𝕌 ℍ𝕌𝕊𝔼ℕ𝔾 𝕍ℙ𝕊")

@app.route("/"+ADMIN_PATH)
def admin():
    con=db(); rows=con.execute("SELECT * FROM codes ORDER BY id DESC").fetchall(); con.close()
    return render_template("admin.html", name="𝔸𝔹𝔻𝕆𝕌𝕌𝕌 ℍ𝕌𝕊𝔼ℕ𝔾 𝕍ℙ𝕊", codes=rows, admin_path=ADMIN_PATH)

@app.post("/"+ADMIN_PATH+"/create")
def create_code():
    data=request.get_json(silent=True) or {}
    try:
        days=max(1,min(int(data.get("days",1)),3650))
        users=max(1,min(int(data.get("users",1)),100000))
    except:
        return jsonify(ok=False,message="المدة وعدد المستخدمين يجب أن يكونا أرقاماً"),400
    code=make_code()
    now=datetime.now(timezone.utc)
    expires=now+timedelta(days=days)
    con=db()
    con.execute("INSERT INTO codes(code,expires_at,max_users,created_at) VALUES(?,?,?,?)",
                (code,expires.isoformat(),users,now.isoformat()))
    con.commit(); con.close()
    return jsonify(ok=True,code=code,expires_at=expires.isoformat(),max_users=users)

@app.post("/"+ADMIN_PATH+"/toggle")
def toggle_code():
    data=request.get_json(silent=True) or {}
    con=db()
    con.execute("UPDATE codes SET active=CASE active WHEN 1 THEN 0 ELSE 1 END WHERE id=?",(int(data.get("id",0)),))
    con.commit(); con.close()
    return jsonify(ok=True)

@app.post("/"+ADMIN_PATH+"/delete")
def delete_code():
    data=request.get_json(silent=True) or {}
    con=db(); con.execute("DELETE FROM codes WHERE id=?",(int(data.get("id",0)),)); con.commit(); con.close()
    return jsonify(ok=True)

@app.get("/health")
def health(): return jsonify(status="ok")

init_db()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
