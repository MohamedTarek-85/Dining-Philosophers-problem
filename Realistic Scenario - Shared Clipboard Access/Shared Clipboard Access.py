import threading  # استيراد مكتبة الـ threading لاستخدام الخيوط
import time  # استيراد مكتبة الوقت لاستخدام التأخيرات العشوائية
import random  # استيراد مكتبة العشوائيات لاختيار العمليات عشوائيًا

# تعريف فئة الـ Clipboard (الحافظة) التي تمثل المورد المشترك
class Clipboard:
    def __init__(self):
        self.content = "Initial Content"  # تعيين المحتوى الابتدائي للحافظة
        self.lock = threading.Lock()  # إنشاء قفل لضمان الوصول المتسلسل للحافظة

    # دالة لقراءة المحتوى من الحافظة
    def read(self, program_id):
        print(f"Program {program_id} is reading the clipboard: '{self.content}'")  # طباعة المحتوى الحالي للحافظة

    # دالة لكتابة محتوى جديد في الحافظة
    def write(self, program_id):
        new_content = f"Content from Program {program_id} at {time.ctime()}"  # إنشاء محتوى جديد مع الوقت الحالي
        print(f"Program {program_id} is writing to the clipboard: '{new_content}'")  # طباعة المحتوى الجديد المكتوب
        self.content = new_content  # تحديث الحافظة بالمحتوى الجديد

# تعريف فئة الـ Program التي تمثل كل برنامج (خيط) يحاول الوصول إلى الحافظة
class Program(threading.Thread):
    def __init__(self, program_id, clipboard):
        threading.Thread.__init__(self)  # تهيئة الخيط
        self.program_id = program_id  # تعيين معرف البرنامج
        self.clipboard = clipboard  # تخزين مرجع الحافظة

    # دالة لتشغيل الخيط (برنامج) وبدء العمليات
    def run(self):
        while True:
            action = random.choice(["read", "write"])  # اختيار عملية عشوائية (قراءة أو كتابة)
            time.sleep(random.uniform(1, 3))  # انتظار عشوائي لمدة قصيرة لمحاكاة تأخير

            with self.clipboard.lock:  # استخدام القفل لضمان الوصول المتسلسل للحافظة
                if action == "read":  # إذا كانت العملية هي القراءة
                    self.clipboard.read(self.program_id)  # استدعاء دالة القراءة
                elif action == "write":  # إذا كانت العملية هي الكتابة
                    self.clipboard.write(self.program_id)  # استدعاء دالة الكتابة

# تهيئة الحافظة وإنشاء 5 برامج (خيوط) مع بدء الترقيم من 1
clipboard = Clipboard()  # إنشاء كائن الحافظة
programs = [Program(i+1, clipboard) for i in range(5)]  # إنشاء 5 برامج (خيوط) تمثل المستخدمين مع بدء الترقيم من 1

# بدء جميع البرامج (الخيوط)
for program in programs:
    program.start()  # بدء الخيط