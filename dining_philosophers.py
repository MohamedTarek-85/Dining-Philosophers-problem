# استيراد المكتبات المطلوبة
import threading  # استخدام threading لإدارة الخيوط
import time  # استخدام time للتحكم في الزمن وحساب الوقت

# تعريف كلاس العصاية
class Chopstick:
    def __init__(self, id):
        self.id = id + 1  # رقم تعريف العصاية (يبدأ من 1 بدلاً من 0)
        self.lock = threading.Lock()  # قفل للتحكم في استخدام العصاية من قبل أكثر من فيلسوف

# تعريف كلاس مراقبة حالات الجوع
class StarvationMonitor:
    def __init__(self, philosophers, timeout=10):
        self.philosophers = philosophers  # قائمة بالفلاسفة
        self.timeout = timeout  # الفترة الزمنية القصوى دون أكل
        self.last_meal_times = {philosopher.id: time.time() for philosopher in philosophers}  # تسجيل وقت آخر وجبة لكل فيلسوف
        self.monitor_thread = threading.Thread(target=self.monitor)  # خيط منفصل لمراقبة الجوع
        self.running = True  # حالة المراقبة (تعمل أو تتوقف)

    def update_meal_time(self, philosopher_id):
        # تحديث وقت آخر وجبة عند الانتهاء من الأكل
        self.last_meal_times[philosopher_id] = time.time()

    def monitor(self):
        # حلقة لمراقبة حالات الجوع بشكل دوري
        while self.running:
            current_time = time.time()  # الوقت الحالي
            for philosopher_id, last_meal_time in self.last_meal_times.items():
                if current_time - last_meal_time > self.timeout:  # التحقق من تجاوز الوقت المحدد
                    print(f"WARNING: Philosopher {philosopher_id} is starving! (No food for {self.timeout} seconds)")
            time.sleep(5)  # الانتظار 5 ثوانٍ قبل الفحص التالي

    def stop(self):
        # إيقاف مراقبة حالات الجوع
        self.running = False

# تعريف كلاس الفيلسوف
class Philosopher(threading.Thread):
    def __init__(self, id, left_chopstick, right_chopstick, priority_lock, starvation_monitor):
        threading.Thread.__init__(self)
        self.id = id + 1  # رقم الفيلسوف (يبدأ من 1 بدلاً من 0)
        self.left_chopstick = left_chopstick  # العصا على اليسار
        self.right_chopstick = right_chopstick  # العصا على اليمين
        self.priority_lock = priority_lock  # قفل لتحديد الأولويات
        self.starvation_monitor = starvation_monitor  # مراقب الجوع المرتبط بالفيلسوف

    def run(self):
        while True:  # حلقة مستمرة (التفكير - الجوع - الأكل - التفكير)
            print(f"Philosopher {self.id} is thinking.")  # طباعة حالة التفكير
            time.sleep(1)  # استراحة تمثل وقت التفكير

            # محاولة الأكل
            print(f"Philosopher {self.id} is hungry and requesting priority.")
            with self.priority_lock:  # استخدام قفل الأولوية لتجنب التداخل
                with self.left_chopstick.lock:  # محاولة الإمساك بالعصا اليسرى
                    print(f"Philosopher {self.id} picked up left chopstick {self.left_chopstick.id}.")
                    with self.right_chopstick.lock:  # محاولة الإمساك بالعصا اليمنى
                        print(f"Philosopher {self.id} picked up right chopstick {self.right_chopstick.id}.")
                        
                        # الأكل
                        print(f"Philosopher {self.id} is eating now.")
                        self.starvation_monitor.update_meal_time(self.id)  # تحديث وقت آخر وجبة
                        time.sleep(2)  # استراحة تمثل وقت الأكل
                        print(f"Philosopher {self.id} finished eating and is thinking again.")

# تشغيل المحاكاة
def dining_philosophers(num_philosophers):
    chopsticks = [Chopstick(i) for i in range(num_philosophers)]  # إنشاء العصايات
    priority_lock = threading.Lock()  # قفل للأولوية لضمان الترتيب

    # إنشاء الفلاسفة
    philosophers = [
        Philosopher(i, chopsticks[i], chopsticks[(i + 1) % num_philosophers], priority_lock, None)
        for i in range(num_philosophers)
    ]

    # إنشاء مراقب الجوع
    starvation_monitor = StarvationMonitor(philosophers)
    for philosopher in philosophers:
        philosopher.starvation_monitor = starvation_monitor  # ربط مراقب الجوع بكل فيلسوف

    # بدء تشغيل مراقبة الجوع
    starvation_monitor.monitor_thread.start()

    # بدء تشغيل الفلاسفة
    for philosopher in philosophers:
        philosopher.start()

    # إبقاء البرنامج يعمل
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        starvation_monitor.stop()  # إيقاف مراقبة الجوع
        starvation_monitor.monitor_thread.join()  # انتظار إنهاء خيط المراقبة

# تشغيل البرنامج
if __name__ == "__main__":
    dining_philosophers(5)  # تشغيل المحاكاة لـ 5 فلاسفة
