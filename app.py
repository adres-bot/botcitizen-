from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "ماء" in incoming_msg:
        msg.body("🚰 هل هناك انقطاع في الماء؟ يرجى توضيح المكان وسنقوم بالمتابعة.")
    elif "كهرباء" in incoming_msg:
        msg.body("💡 يرجى تحديد موقع المشكلة المتعلقة بالكهرباء وسنقوم بإبلاغ الجهات المختصة.")
    elif "صحة" in incoming_msg or "مركز صحي" in incoming_msg:
        msg.body("🏥 يرجى تحديد اسم المركز الصحي والمشكلة التي تواجهها، وسنتابعها مع الجهات المختصة.")
    elif "مدرسة" in incoming_msg or "تعليم" in incoming_msg:
        msg.body("📚 يرجى تحديد اسم المدرسة والمشكلة التي لاحظتها (نقص أدوات، غياب معلم، إلخ).")
    elif "بلاغ" in incoming_msg or "بلّغ" in incoming_msg:
        msg.body("📢 أرسل تفاصيل البلاغ (مثلاً: أين؟ متى؟ ماذا حدث؟). سيتم توثيقه وإحالته للجهات المختصة.")
    elif "تطعيم" in incoming_msg or "لقاح" in incoming_msg:
        msg.body("💉 حملة تطعيم الأطفال ستقام يوم السبت القادم في بلدية عرفات – لا تنسوا المشاركة.")
    elif "استبيان" in incoming_msg:
        msg.body("📝 هل ترغب بالمشاركة في تقييم جودة الخدمات؟ أرسل 'نعم' وسنرسل لك الأسئلة.")
    elif "حفر" in incoming_msg or "حفرة" in incoming_msg or "شارع" in incoming_msg:
        msg.body("🚧 هل هناك حفرة أو ضرر في الطريق؟ يرجى تحديد الموقع وسنقوم بإبلاغ الجهة المسؤولة.")
    elif "إنارة" in incoming_msg or "ضوء" in incoming_msg or "شارع مظلم" in incoming_msg:
        msg.body("💡 شكرًا للتبليغ. يرجى تحديد اسم الشارع الذي يحتاج إصلاح الإنارة.")
    elif "نفايات" in incoming_msg or "قمامة" in incoming_msg or "نظافة" in incoming_msg:
        msg.body("🗑️ شكرًا على الإبلاغ. سيتم إرسال ملاحظة إلى فرق النظافة في منطقتك.")
    elif "شكوى" in incoming_msg or "تظلم" in incoming_msg:
        msg.body("📝 يرجى كتابة تفاصيل الشكوى وسنتابعها بالطرق الرسمية.")
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
