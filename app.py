from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ إنشاء قاعدة البيانات إذا لم تكن موجودة
def init_db():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # تشغيل الدالة عند تشغيل البوت

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')  # رقم المرسل
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    resp = MessagingResponse()
    msg = resp.message()

    # ✅ حفظ كل بلاغ في قاعدة البيانات
    def save_report(msg):
        conn = sqlite3.connect('reports.db')
        c = conn.cursor()
        c.execute('INSERT INTO reports (phone, message, timestamp) VALUES (?, ?, ?)', (sender, msg, timestamp))
        conn.commit()
        conn.close()

    if "بلاغ" in incoming_msg or "بلّغ" in incoming_msg:
        msg.body("📢 أرسل تفاصيل البلاغ (مثلاً: أين؟ متى؟ ماذا حدث؟). سيتم توثيقه وإحالته للجهات المختصة.")
    elif any(word in incoming_msg for word in ["ماء", "كهرباء", "صحة", "مدرسة", "تطعيم", "استبيان", "حفر", "إنارة", "نفايات", "شكوى"]):
        save_report(incoming_msg)
        msg.body("✅ تم استلام بلاغك. شكرًا لمساهمتك!")
    elif "قائمة" in incoming_msg or "مساعدة" in incoming_msg:
        msg.body(
            "👋 أهلاً بك في بوت المواطن:\n"
            "اكتب أي من الكلمات التالية:\n"
            "• ماء – كهرباء – صحة – مدرسة – بلاغ – تطعيم\n"
            "• استبيان – حفر – إنارة – نفايات – شكوى"
        )
    else:
        msg.body("❗ لم أفهم رسالتك.\nاكتب 'قائمة' لعرض الكلمات المدعومة.")

    return str(resp)

if __name__ == "__main__":
    app.run()


    return html

if __name__ == "__main__":
    app.run()
