from flask import Flask, request, render_template_string
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT,
                    message TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ✅ استقبال الرسائل من واتساب
@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    phone = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    # ✅ تخزين الرسالة مباشرة بدون شروط
    conn = sqlite3.connect('reports.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (phone, message, timestamp) VALUES (?, ?, ?)",
              (phone, incoming_msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    # الكلمات المفتاحية والردود
    if "ماء" in incoming_msg:
        msg.body("🚰 هل هناك انقطاع في الماء؟ يرجى توضيح المكان وسنقوم بالمتابعة.")
    elif "كهرباء" in incoming_msg or "كهربا" in incoming_msg:
        msg.body("💡 يرجى تحديد موقع المشكلة المتعلقة بالكهرباء وسنقوم بإبلاغ الجهات المختصة.")
    elif "صحة" in incoming_msg or "صحه" in incoming_msg or "مركز صحي" in incoming_msg:
        msg.body("🏥 يرجى تحديد اسم المركز الصحي والمشكلة التي تواجهها، وسنتابعها مع الجهات المختصة.")
    elif "مدرسة" in incoming_msg or "مدرسه" in incoming_msg or "تعليم" in incoming_msg:
        msg.body("📚 يرجى تحديد اسم المدرسة والمشكلة التي لاحظتها (نقص أدوات، غياب معلم، إلخ).")
    elif "بلاغ" in incoming_msg or "بلّغ" in incoming_msg or "تبليغ" in incoming_msg:
        msg.body("📢 أرسل تفاصيل البلاغ (مثلاً: أين؟ متى؟ ماذا حدث؟). سيتم توثيقه وإحالته للجهات المختصة.")
    elif "تطعيم" in incoming_msg or "لقاح" in incoming_msg or "تطعيمه" in incoming_msg:
        msg.body("💉 حملة تطعيم الأطفال ستقام يوم السبت القادم في بلدية عرفات – لا تنسوا المشاركة.")
    elif "استبيان" in incoming_msg or "استبانة" in incoming_msg:
        msg.body("📝 هل ترغب بالمشاركة في تقييم جودة الخدمات؟ أرسل 'نعم' وسنرسل لك الأسئلة.")
    elif "حفر" in incoming_msg or "حفرة" in incoming_msg or "حفره" in incoming_msg or "شارع" in incoming_msg:
        msg.body("🚧 هل هناك حفرة أو ضرر في الطريق؟ يرجى تحديد الموقع وسنقوم بإبلاغ الجهة المسؤولة.")
    elif "إنارة" in incoming_msg or "ضوء" in incoming_msg or "شارع مظلم" in incoming_msg or "اضاءة" in incoming_msg:
        msg.body("💡 شكرًا للتبليغ. يرجى تحديد اسم الشارع الذي يحتاج إصلاح الإنارة.")
    elif "نفايات" in incoming_msg or "فايات" in incoming_msg or "قمامة" in incoming_msg or "نظافة" in incoming_msg or "زبالة" in incoming_msg:
        msg.body("🗑️ شكرًا على الإبلاغ. سيتم إرسال ملاحظة إلى فرق النظافة في منطقتك.")
    elif "شكوى" in incoming_msg or "تظلم" in incoming_msg or "شكاية" in incoming_msg:
        msg.body("📝 يرجى كتابة تفاصيل الشكوى وسنتابعها بالطرق الرسمية.")
    elif "قائمة" in incoming_msg or "مساعدة" in incoming_msg or "help" in incoming_msg:
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
    <html>
    <head>
        <title>قائمة البلاغات</title>
        <meta charset="utf-8">
    </head>
    <body style="direction: rtl; font-family: Arial;">
        <h2>📋 قائمة البلاغات</h2>
        <table border="1" cellpadding="8" cellspacing="0">
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

# ✅ تشغيل التطبيق
if __name__ == "__main__":
    app.run()


# ✅ تشغيل التطبيق
if __name__ == "__main__":
    app.run()

