from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from datetime import datetime

# إعدادات Airtable
AIRTABLE_API_KEY = "ضع التوكن هنا"
BASE_ID = "appsksbCyBcVUaKN0"
TABLE_NAME = "Table 1"

app = Flask(__name__)

# إرسال البيانات إلى Airtable
def save_to_airtable(phone, message):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "رقم الهاتف": phone,
            "محتوى البلاغ": message,
            "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.status_code == 200 or response.status_code == 201

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip().lower()
    phone = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()

    # الردود الذكية
    if "ماء" in incoming_msg:
        msg.body("🚰 هل هناك انقطاع في الماء؟ يرجى توضيح المكان وسنقوم بالمتابعة.")
    elif "كهرباء" in incoming_msg or "كهربا" in incoming_msg:
        msg.body("💡 يرجى تحديد موقع المشكلة المتعلقة بالكهرباء وسنقوم بإبلاغ الجهات المختصة.")
    elif "نفايات" in incoming_msg or "قمامة" in incoming_msg:
        msg.body("🗑️ شكرًا على الإبلاغ. سيتم إرسال ملاحظة إلى فرق النظافة في منطقتك.")
    elif "قائمة" in incoming_msg or "مساعدة" in incoming_msg:
        msg.body("📝 اكتب بلاغك أو اختر من الكلمات: ماء - كهرباء - نفايات - شكوى - تطعيم - إنارة - استبيان.")
    else:
        msg.body("❗ لم أفهم رسالتك.\nاكتب 'قائمة' لعرض الكلمات المدعومة.")

    # حفظ البلاغ
    if len(incoming_msg) > 2:
        save_to_airtable(phone, incoming_msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
