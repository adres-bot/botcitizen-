from flask import Flask, request, render_template_string
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ إنشاء قاعدة البيانات
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

init_db()

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    resp = MessagingResponse()
    msg = resp.message()

    def save_report(msg_text):
        conn = sqlite3.connect('reports.db')
        c = conn.cursor()
        c.execute('INSERT INTO reports (phone, message, timestamp) VALUES (?, ?, ?)', (sender, msg_text, timestamp))
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

# ✅ صفحة عرض البلاغات
@app.route("/بلاغات")
def show_reports():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute("SELECT phone, message, timestamp FROM reports ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>قائمة البلاغات</title>
    </head>
    <body>
        <h2>📋 قائمة البلاغات المستلمة</h2>
        <table border="1" cellpadding="5" style="direction: rtl;">
            <tr>
                <th>📱 الرقم</th>
                <th>💬 البلاغ</th>
                <th>🕒 الوقت</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, rows=rows)

if __name__ == "__main__":
  from flask import render_template_string
import sqlite3

@app.route("/بلاغات")
def show_reports():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute("SELECT phone, message, timestamp FROM reports ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    html = '''
    <html>
    <head><title>قائمة البلاغات</title></head>
    <body>
        <h2>📋 قائمة البلاغات المستلمة</h2>
        <table border="1" style="direction: rtl;">
            <tr>
                <th>📱 الرقم</th>
                <th>💬 البلاغ</th>
                <th>🕒 الوقت</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, rows=rows)
   app.run()
