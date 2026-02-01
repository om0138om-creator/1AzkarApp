import flet as ft
import sqlite3
import os
import datetime

# ==================== قاعدة البيانات الآمنة ====================

def get_db_path():
    """الحصول على مسار قاعدة البيانات بشكل آمن للأندرويد"""
    try:
        # في أندرويد، نستخدم متغير البيئة المخصص للملفات
        if "ANDROID_FILES" in os.environ:
            return os.path.join(os.environ["ANDROID_FILES"], "hisn_almuslim.db")
        # حل بديل إذا لم نجد المتغير
        if os.path.exists("/data/data"): 
             # هذا المسار عام للأندرويد ولكنه يحتاج التأكد من اسم الحزمة، لذا نفضل الحل الأول
             pass
    except Exception:
        pass
    
    # العودة للوضع العادي (للحاسوب)
    return "hisn_almuslim.db"

def init_database():
    """تهيئة قاعدة البيانات"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # إنشاء الجداول (نفس الجداول السابقة)
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, icon TEXT, color TEXT, order_num INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adhkar 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, text TEXT, count INTEGER, 
                      current_count INTEGER DEFAULT 0, benefit TEXT, hadith TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasbih 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, count INTEGER, target INTEGER, last_updated TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # التأكد من وجود بيانات
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        # إدخال بيانات تجريبية سريعة للتأكد من العمل
        cursor.execute("INSERT INTO categories (name, icon, color, order_num) VALUES (?, ?, ?, ?)", 
                       ("أذكار الصباح", "wb_sunny", "#10b981", 1))
        cursor.execute("INSERT INTO adhkar (category_id, text, count) VALUES (?, ?, ?)",
                       (1, "سبحان الله وبحمده", 100))
    
    conn.commit()
    conn.close()

# ==================== التطبيق الرئيسي ====================

def main(page: ft.Page):
    # وضع حماية شامل (Try/Except) لمنع الشاشة البيضاء
    try:
        page.title = "حصن المسلم"
        page.rtl = True
        page.scroll = "adaptive"
        page.padding = 10
        page.theme_mode = ft.ThemeMode.LIGHT # تثبيت الوضع الفاتح للتجربة

        # 1. تهيئة قاعدة البيانات
        init_database()

        # 2. بناء الواجهة (بدون خطوط مخصصة مؤقتاً)
        page.appbar = ft.AppBar(
            title=ft.Text("حصن المسلم", color=ft.colors.WHITE),
            center_title=True,
            bgcolor="#10b981",
        )

        # دالة لجلب الأذكار وعرضها
        def load_ui():
            db_path = get_db_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            cats = cursor.fetchall()
            conn.close()

            # عرض الفئات
            for cat in cats:
                page.add(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(cat[2], color=ft.colors.WHITE),
                            ft.Text(cat[1], size=18, color=ft.colors.WHITE, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=cat[3],
                        padding=20,
                        border_radius=10,
                        margin=5
                    )
                )
            
            page.add(ft.Text("تم التشغيل بنجاح ✅", color="green", size=20))

        load_ui()

    except Exception as e:
        # في حالة حدوث خطأ، اطبعه على الشاشة بدلاً من الشاشة البيضاء
        page.add(
            ft.Column([
                ft.Icon(ft.icons.ERROR, color="red", size=50),
                ft.Text("حدث خطأ أثناء التشغيل:", size=20, color="red", weight="bold"),
                ft.Text(str(e), size=16, color="red"),
                ft.Text("يرجى تصوير هذه الشاشة وإرسالها", size=14)
            ])
        )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
