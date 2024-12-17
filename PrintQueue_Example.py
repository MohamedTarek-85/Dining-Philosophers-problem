# استيراد المكتبات
import threading  # عشان نستخدم مفهوم الثريدنج ونحقق التزامن
import time  # عشان نتحكم في الوقت

# تعريف كلاس الطابعة
class Printer:
    def __init__(self, id):
        self.id = id + 1  # رقم تعريف الطابعة
        self.lock = threading.Lock()  # قفل للتحكم في استخدام الطابعة

# تعريف كلاس الموظف
class Employee(threading.Thread):
    def __init__(self, id, left_printer, right_printer, priority_lock, stop_flag):
        threading.Thread.__init__(self)
        self.id = id + 1  # رقم الموظف
        self.left_printer = left_printer  # الطابعة اللي على الشمال
        self.right_printer = right_printer  # الطابعة اللي على اليمين
        self.priority_lock = priority_lock  # قفل لتحديد الأولوية
        self.stop_flag = stop_flag  # علامة الإنهاء

    # دالة تشغيل الموظف
    def run(self):
        while not self.stop_flag.is_set():  # يشتغل طالما علامة الإنهاء مش مفعّلة
            print(f"Employee {self.id} is preparing the file for printing.")  # تجهيز الملف
            time.sleep(1)  # استراحة تمثل وقت تجهيز الملف

            # محاولة حجز الطابعات
            print(f"Employee {self.id} needs to acquire both printers for printing.")
            with self.priority_lock:  # طلب إذن من الأولوية
                with self.left_printer.lock:  # حجز الطابعة الشمال
                    print(f"Employee {self.id} acquired the left printer {self.left_printer.id}.")
                    with self.right_printer.lock:  # حجز الطابعة اليمين
                        print(f"Employee {self.id} acquired the right printer {self.right_printer.id}.")
                        
                        # الطباعة
                        print(f"Employee {self.id} is printing now.")
                        time.sleep(2)  # استراحة تمثل وقت الطباعة

            # الموظف خلص الطباعة
            print(f"Employee {self.id} has finished printing and released both printers.")

        print(f"Employee {self.id} has exited the simulation.")  # رسالة عند إنهاء الموظف

# دالة تشغيل المحاكاة
def office_simulation(num_employees, duration):
    printers = [Printer(i) for i in range(num_employees)]  # إنشاء الطابعات
    priority_lock = threading.Lock()  # قفل لتحديد الأولويات (مفتاح مشترك لكل الموظفين)
    stop_flag = threading.Event()  # علامة مشتركة للتحكم في إنهاء الخيوط

    # إنشاء الموظفين
    employees = [
        Employee(i, printers[i], printers[(i + 1) % num_employees], priority_lock, stop_flag)
        for i in range(num_employees)
    ]  
    # هنا يتم ربط كل موظف بطابعتين (اليسرى واليمنى) مع مراعاة التدوير
    # الطابعة اليمنى للموظف الأخير تكون الطابعة الأولى بسبب [(i + 1) % num_employees]

    # بدء تشغيل كل الموظفين
    for employee in employees:
        employee.start()

    # تشغيل المحاكاة لفترة محددة
    time.sleep(duration)  # تشغيل المحاكاة لمدة زمنية محددة
    stop_flag.set()  # تفعيل علامة الإنهاء بعد انتهاء الوقت

    # انتظار انتهاء جميع الموظفين
    for employee in employees:
        employee.join()  # ينتظر انتهاء جميع الموظفين (الخيوط)

    print("The simulation has ended.")  # رسالة إنهاء المحاكاة

# تشغيل البرنامج
office_simulation(5, 20)  # 5 موظفين ومدة المحاكاة 20 ثانية
