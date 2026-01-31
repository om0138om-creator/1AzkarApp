import flet as ft
import sqlite3
import os
import json
from datetime import datetime

# ==================== قاعدة البيانات ====================

def get_db_path():
    """الحصول على مسار قاعدة البيانات"""
    return "hisn_almuslim.db"

def init_database():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # جدول الفئات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT NOT NULL,
            color TEXT NOT NULL,
            order_num INTEGER DEFAULT 0
        )
    ''')
    
    # جدول الأذكار
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adhkar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            current_count INTEGER DEFAULT 0,
            benefit TEXT,
            hadith TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # جدول التسبيح
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasbih (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            target INTEGER DEFAULT 33,
            last_updated TEXT
        )
    ''')
    
    # جدول الإعدادات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # إدخال البيانات الافتراضية
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        insert_default_data(cursor)
    
    conn.commit()
    conn.close()

def insert_default_data(cursor):
    """إدخال البيانات الافتراضية"""
    
    # الفئات
    categories = [
        ("أذكار الصباح", "wb_sunny", "#10b981", 1),
        ("أذكار المساء", "nights_stay", "#6366f1", 2),
        ("أذكار الصلاة", "mosque", "#f59e0b", 3),
        ("أذكار النوم", "bedtime", "#8b5cf6", 4),
        ("أذكار القرآن", "menu_book", "#ec4899", 5),
        ("أذكار السفر", "flight", "#06b6d4", 6),
        ("أذكار الطعام", "restaurant", "#84cc16", 7),
        ("أذكار متنوعة", "star", "#f97316", 8),
    ]
    
    cursor.executemany(
        "INSERT INTO categories (name, icon, color, order_num) VALUES (?, ?, ?, ?)",
        categories
    )
    
    # أذكار الصباح
    morning_adhkar = [
        (1, "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 1, 0, "من أذكار الصباح المباركة", "رواه أبو داود"),
        (1, "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ", 1, 0, "التوكل على الله في بداية اليوم", "رواه الترمذي"),
        (1, "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَىٰ عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ", 1, 0, "سيد الاستغفار", "رواه البخاري"),
        (1, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "أفضل الكلام بعد القرآن", "رواه مسلم"),
        (1, "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 10, 0, "كانت له عدل عشر رقاب", "متفق عليه"),
        (1, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "حماية من كل شر", "رواه مسلم"),
        (1, "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", 3, 0, "لم يضره شيء", "رواه أبو داود والترمذي"),
        (1, "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ", 3, 0, "سؤال العافية", "رواه ابن ماجه"),
    ]
    
    # أذكار المساء
    evening_adhkar = [
        (2, "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", 1, 0, "من أذكار المساء", "رواه أبو داود"),
        (2, "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ", 1, 0, "التوكل على الله", "رواه الترمذي"),
        (2, "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ", 3, 0, "حماية من الشر", "رواه مسلم"),
        (2, "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ", 1, 0, "الاستعاذة من الهم", "رواه البخاري"),
        (2, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", 100, 0, "حُطت خطاياه وإن كانت مثل زبد البحر", "متفق عليه"),
        (2, "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", 100, 0, "الاستغفار", "متفق عليه"),
    ]
    
    # أذكار الصلاة
    prayer_adhkar = [
        (3, "أَسْتَغْفِرُ اللَّهَ، أَسْتَغْفِرُ اللَّهَ، أَسْتَغْفِرُ اللَّهَ", 3, 0, "بعد السلام من الصلاة", "رواه مسلم"),
        (3, "اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ، تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ", 1, 0, "بعد الصلاة", "رواه مسلم"),
        (3, "سُبْحَانَ اللَّهِ", 33, 0, "التسبيح بعد الصلاة", "رواه مسلم"),
        (3, "الْحَمْدُ لِلَّهِ", 33, 0, "التحميد بعد الصلاة", "رواه مسلم"),
        (3, "اللَّهُ أَكْبَرُ", 33, 0, "التكبير بعد الصلاة", "رواه مسلم"),
        (3, "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", 1, 0, "تمام المائة", "رواه مسلم"),
        (3, "آيَةُ الْكُرْسِيِّ", 1, 0, "قراءة آية الكرسي بعد كل صلاة", "رواه النسائي"),
    ]
    
    # أذكار النوم
    sleep_adhkar = [
        (4, "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", 1, 0, "عند النوم", "رواه البخاري"),
        (4, "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ", 1, 0, "عند النوم", "رواه أبو داود"),
        (4, "سُبْحَانَ اللَّهِ", 33, 0, "قبل النوم", "متفق عليه"),
        (4, "الْحَمْدُ لِلَّهِ", 33, 0, "قبل النوم", "متفق عليه"),
        (4, "اللَّهُ أَكْبَرُ", 34, 0, "قبل النوم", "متفق عليه"),
        (4, "اللَّهُمَّ أَسْلَمْتُ نَفْسِي إِلَيْكَ، وَوَجَّهْتُ وَجْهِي إِلَيْكَ، وَفَوَّضْتُ أَمْرِي إِلَيْكَ", 1, 0, "التوكل على الله عند النوم", "متفق عليه"),
    ]
    
    # أذكار القرآن
    quran_adhkar = [
        (5, "أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ", 1, 0, "قبل القراءة", ""),
        (5, "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", 1, 0, "البسملة", ""),
        (5, "صَدَقَ اللَّهُ الْعَظِيمُ", 1, 0, "بعد الانتهاء من القراءة", ""),
    ]
    
    # أذكار السفر
    travel_adhkar = [
        (6, "اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَٰذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ، وَإِنَّا إِلَىٰ رَبِّنَا لَمُنْقَلِبُونَ", 1, 0, "دعاء السفر", "رواه مسلم"),
        (6, "اللَّهُمَّ إِنَّا نَسْأَلُكَ فِي سَفَرِنَا هَٰذَا الْبِرَّ وَالتَّقْوَىٰ، وَمِنَ الْعَمَلِ مَا تَرْضَىٰ", 1, 0, "دعاء السفر", "رواه مسلم"),
        (6, "اللَّهُمَّ هَوِّنْ عَلَيْنَا سَفَرَنَا هَٰذَا وَاطْوِ عَنَّا بُعْدَهُ", 1, 0, "تسهيل السفر", "رواه مسلم"),
        (6, "آيِبُونَ تَائِبُونَ عَابِدُونَ لِرَبِّنَا حَامِدُونَ", 1, 0, "عند العودة من السفر", "رواه مسلم"),
    ]
    
    # أذكار الطعام
    food_adhkar = [
        (7, "بِسْمِ اللَّهِ", 1, 0, "قبل الأكل", "رواه أبو داود"),
        (7, "بِسْمِ اللَّهِ أَوَّلَهُ وَآخِرَهُ", 1, 0, "إذا نسي التسمية في أوله", "رواه أبو داود"),
        (7, "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَٰذَا، وَرَزَقَنِيهِ، مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ", 1, 0, "بعد الأكل", "رواه أبو داود والترمذي"),
        (7, "الْحَمْدُ لِلَّهِ حَمْدًا كَثِيرًا طَيِّبًا مُبَارَكًا فِيهِ", 1, 0, "بعد الأكل", "رواه البخاري"),
    ]
    
    # أذكار متنوعة
    misc_adhkar = [
        (8, "لَا إِلَٰهَ إِلَّا اللَّهُ", 100, 0, "أفضل الذكر", "رواه الترمذي"),
        (8, "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَٰهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ", 100, 0, "الباقيات الصالحات", "رواه مسلم"),
        (8, "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", 100, 0, "كنز من كنوز الجنة", "متفق عليه"),
        (8, "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ", 100, 0, "كلمتان حبيبتان إلى الرحمن", "متفق عليه"),
        (8, "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَىٰ نَبِيِّنَا مُحَمَّدٍ", 100, 0, "الصلاة على النبي", "رواه مسلم"),
    ]
    
    # إدخال جميع الأذكار
    all_adhkar = morning_adhkar + evening_adhkar + prayer_adhkar + sleep_adhkar + quran_adhkar + travel_adhkar + food_adhkar + misc_adhkar
    
    cursor.executemany(
        "INSERT INTO adhkar (category_id, text, count, current_count, benefit, hadith) VALUES (?, ?, ?, ?, ?, ?)",
        all_adhkar
    )
    
    # إدخال التسبيحات الافتراضية
    tasbihat = [
        ("سُبْحَانَ اللَّهِ", 0, 33, datetime.now().isoformat()),
        ("الْحَمْدُ لِلَّهِ", 0, 33, datetime.now().isoformat()),
        ("اللَّهُ أَكْبَرُ", 0, 34, datetime.now().isoformat()),
        ("لَا إِلَٰهَ إِلَّا اللَّهُ", 0, 100, datetime.now().isoformat()),
        ("أَسْتَغْفِرُ اللَّهَ", 0, 100, datetime.now().isoformat()),
        ("الصَّلَاةُ عَلَى النَّبِيِّ", 0, 100, datetime.now().isoformat()),
    ]
    
    cursor.executemany(
        "INSERT INTO tasbih (name, count, target, last_updated) VALUES (?, ?, ?, ?)",
        tasbihat
    )
    
    # إعدادات افتراضية
    settings = [
        ("dark_mode", "false"),
        ("font_size", "18"),
    ]
    
    cursor.executemany(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        settings
    )

# ==================== وظائف قاعدة البيانات ====================

def get_categories():
    """الحصول على جميع الفئات"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories ORDER BY order_num")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_adhkar_by_category(category_id):
    """الحصول على الأذكار حسب الفئة"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM adhkar WHERE category_id = ?", (category_id,))
    adhkar = cursor.fetchall()
    conn.close()
    return adhkar

def update_adhkar_count(adhkar_id, new_count):
    """تحديث عداد الذكر"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("UPDATE adhkar SET current_count = ? WHERE id = ?", (new_count, adhkar_id))
    conn.commit()
    conn.close()

def reset_adhkar_counts(category_id):
    """إعادة تعيين جميع العدادات لفئة معينة"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("UPDATE adhkar SET current_count = 0 WHERE category_id = ?", (category_id,))
    conn.commit()
    conn.close()

def get_tasbihat():
    """الحصول على جميع التسبيحات"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasbih")
    tasbihat = cursor.fetchall()
    conn.close()
    return tasbihat

def update_tasbih_count(tasbih_id, new_count):
    """تحديث عداد التسبيح"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasbih SET count = ?, last_updated = ? WHERE id = ?",
        (new_count, datetime.now().isoformat(), tasbih_id)
    )
    conn.commit()
    conn.close()

def reset_tasbih_count(tasbih_id):
    """إعادة تعيين عداد التسبيح"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasbih SET count = 0, last_updated = ? WHERE id = ?",
        (datetime.now().isoformat(), tasbih_id)
    )
    conn.commit()
    conn.close()

def get_setting(key):
    """الحصول على إعداد معين"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_setting(key, value):
    """حفظ إعداد"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

# ==================== التطبيق الرئيسي ====================

def main(page: ft.Page):
    """الدالة الرئيسية للتطبيق"""
    
    # تهيئة قاعدة البيانات
    init_database()
    
    # إعدادات الصفحة الأساسية
    page.title = "حصن المسلم"
    page.rtl = True
    page.padding = 0
    page.spacing = 0
    page.scroll = "adaptive"
    
    # الألوان الأساسية
    PRIMARY_COLOR = "#10b981"
    PRIMARY_DARK = "#059669"
    SECONDARY_COLOR = "#6366f1"
    
    # تحميل الإعدادات
    dark_mode = get_setting("dark_mode") == "true"
    font_size = int(get_setting("font_size") or "18")
    
    # تطبيق الوضع
    page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
    
    # تحميل الخط المخصص
    page.fonts = {
        "MyFont": "myfont.otf"
    }
    
    # السمة المخصصة
    page.theme = ft.Theme(
        font_family="MyFont",
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            secondary=SECONDARY_COLOR,
        ),
    )
    
    page.dark_theme = ft.Theme(
        font_family="MyFont",
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            secondary=SECONDARY_COLOR,
        ),
    )
    
    # ==================== المتغيرات ====================
    
    current_category_id = None
    current_tasbih_id = None
    current_tasbih_count = 0
    current_tasbih_target = 33
    
    # ==================== المكونات ====================
    
    def get_text_color():
        """الحصول على لون النص حسب الوضع"""
        return ft.colors.WHITE if dark_mode else ft.colors.BLACK
    
    def get_bg_color():
        """الحصول على لون الخلفية حسب الوضع"""
        return "#1a1a2e" if dark_mode else "#f8fafc"
    
    def get_card_color():
        """الحصول على لون البطاقة حسب الوضع"""
        return "#252542" if dark_mode else ft.colors.WHITE
    
    def create_header(title, show_back=False, show_settings=True):
        """إنشاء شريط العنوان"""
        
        def go_back(e):
            show_home_page()
        
        def go_settings(e):
            show_settings_page()
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    # زر الرجوع
                    ft.IconButton(
                        icon="arrow_forward",
                        icon_color=ft.colors.WHITE,
                        icon_size=24,
                        on_click=go_back,
                        visible=show_back,
                    ) if show_back else ft.Container(width=48),
                    
                    # العنوان
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                        expand=True,
                    ),
                    
                    # زر الإعدادات
                    ft.IconButton(
                        icon="settings",
                        icon_color=ft.colors.WHITE,
                        icon_size=24,
                        on_click=go_settings,
                        visible=show_settings,
                    ) if show_settings else ft.Container(width=48),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[PRIMARY_COLOR, PRIMARY_DARK],
            ),
        )
    
    def create_category_card(category):
        """إنشاء بطاقة الفئة"""
        cat_id, name, icon, color, order = category
        
        def on_click(e):
            nonlocal current_category_id
            current_category_id = cat_id
            show_adhkar_page(cat_id, name)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icon,
                            size=40,
                            color=ft.colors.WHITE,
                        ),
                        width=70,
                        height=70,
                        border_radius=35,
                        bgcolor=color,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        name,
                        size=font_size,
                        weight=ft.FontWeight.W_600,
                        color=get_text_color(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=16,
            bgcolor=get_card_color(),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            on_click=on_click,
            ink=True,
        )
    
    def create_adhkar_card(dhikr, category_color):
        """إنشاء بطاقة الذكر"""
        dhikr_id, cat_id, text, count, current_count, benefit, hadith = dhikr
        remaining = count - current_count
        is_completed = remaining <= 0
        
        count_text = ft.Text(
            str(max(0, remaining)),
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
        )
        
        count_button = ft.Container(
            content=count_text,
            width=60,
            height=60,
            border_radius=30,
            bgcolor=ft.colors.GREEN if is_completed else category_color,
            alignment=ft.alignment.center,
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        def on_count_click(e):
            nonlocal remaining, is_completed
            if remaining > 0:
                new_count = current_count + 1
                update_adhkar_count(dhikr_id, new_count)
                remaining = count - new_count
                is_completed = remaining <= 0
                count_text.value = str(max(0, remaining))
                if is_completed:
                    count_button.bgcolor = ft.colors.GREEN
                    count_button.content = ft.Icon("check", color=ft.colors.WHITE, size=30)
                page.update()
        
        count_button.on_click = on_count_click
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # نص الذكر
                    ft.Container(
                        content=ft.Text(
                            text,
                            size=font_size + 2,
                            weight=ft.FontWeight.W_500,
                            color=get_text_color(),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.all(16),
                    ),
                    
                    # الخط الفاصل
                    ft.Divider(height=1, color=ft.colors.with_opacity(0.2, get_text_color())),
                    
                    # زر العداد والعدد الكلي
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                count_button,
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            f"العدد: {count}",
                                            size=font_size - 2,
                                            color=ft.colors.with_opacity(0.7, get_text_color()),
                                        ),
                                        ft.Text(
                                            "✓ اكتمل" if is_completed else f"متبقي: {remaining}",
                                            size=font_size - 4,
                                            color=ft.colors.GREEN if is_completed else category_color,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        padding=ft.padding.symmetric(vertical=12),
                    ),
                    
                    # الفائدة والحديث
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    benefit or "",
                                    size=font_size - 4,
                                    color=ft.colors.with_opacity(0.6, get_text_color()),
                                    text_align=ft.TextAlign.CENTER,
                                ) if benefit else ft.Container(),
                                ft.Text(
                                    hadith or "",
                                    size=font_size - 4,
                                    color=ft.colors.with_opacity(0.5, get_text_color()),
                                    italic=True,
                                    text_align=ft.TextAlign.CENTER,
                                ) if hadith else ft.Container(),
                            ],
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(bottom=12, left=16, right=16),
                        visible=bool(benefit or hadith),
                    ),
                ],
                spacing=0,
            ),
            margin=ft.margin.only(bottom=16, left=16, right=16),
            border_radius=16,
            bgcolor=get_card_color(),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, category_color)),
        )
    
    def create_tasbih_button(tasbih):
        """إنشاء زر التسبيح"""
        tasbih_id, name, count, target, last_updated = tasbih
        
        def on_click(e):
            show_tasbih_counter_page(tasbih_id, name, count, target)
        
        progress = min(count / target, 1.0) if target > 0 else 0
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    width=50,
                                    height=50,
                                    border_radius=25,
                                    bgcolor=ft.colors.with_opacity(0.2, PRIMARY_COLOR),
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        str(count),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=PRIMARY_COLOR,
                                    ),
                                    width=50,
                                    height=50,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                        ),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                name,
                                size=font_size,
                                weight=ft.FontWeight.W_600,
                                color=get_text_color(),
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Container(
                                            width=150 * progress,
                                            height=4,
                                            bgcolor=PRIMARY_COLOR,
                                            border_radius=2,
                                        ),
                                        width=150,
                                        height=4,
                                        bgcolor=ft.colors.with_opacity(0.2, PRIMARY_COLOR),
                                        border_radius=2,
                                    ),
                                    ft.Text(
                                        f"{count}/{target}",
                                        size=12,
                                        color=ft.colors.with_opacity(0.6, get_text_color()),
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=8,
                        expand=True,
                    ),
                    ft.Icon(
                        "chevron_left",
                        color=ft.colors.with_opacity(0.5, get_text_color()),
                        size=24,
                    ),
                ],
                spacing=16,
            ),
            padding=16,
            margin=ft.margin.only(bottom=12, left=16, right=16),
            border_radius=12,
            bgcolor=get_card_color(),
            on_click=on_click,
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    # ==================== صفحات التطبيق ====================
    
    def show_home_page():
        """عرض الصفحة الرئيسية"""
        categories = get_categories()
        tasbihat = get_tasbihat()
        
        # شبكة الفئات
        categories_grid = ft.GridView(
            controls=[create_category_card(cat) for cat in categories],
            runs_count=2,
            max_extent=180,
            child_aspect_ratio=1.0,
            spacing=16,
            run_spacing=16,
            padding=16,
        )
        
        # قائمة التسبيحات
        tasbih_list = ft.Column(
            controls=[create_tasbih_button(t) for t in tasbihat],
            spacing=0,
        )
        
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        create_header("حصن المسلم", show_back=False, show_settings=True),
                        
                        # البطاقة الترحيبية
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon("auto_awesome", color=ft.colors.AMBER, size=30),
                                    ft.Text(
                                        "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                                        size=font_size + 4,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                        "أذكار من الكتاب والسنة",
                                        size=font_size - 2,
                                        color=ft.colors.with_opacity(0.9, ft.colors.WHITE),
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                            ),
                            padding=24,
                            margin=ft.margin.all(16),
                            border_radius=16,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[PRIMARY_COLOR, SECONDARY_COLOR],
                            ),
                        ),
                        
                        # عنوان الأقسام
                        ft.Container(
                            content=ft.Text(
                                "📚 أقسام الأذكار",
                                size=font_size + 2,
                                weight=ft.FontWeight.BOLD,
                                color=get_text_color(),
                            ),
                            padding=ft.padding.only(right=16, top=8, bottom=8),
                        ),
                        
                        # شبكة الفئات
                        categories_grid,
                        
                        # عنوان التسبيح
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon("touch_app", color=PRIMARY_COLOR, size=24),
                                    ft.Text(
                                        "التسبيح الإلكتروني",
                                        size=font_size + 2,
                                        weight=ft.FontWeight.BOLD,
                                        color=get_text_color(),
                                    ),
                                ],
                                spacing=8,
                            ),
                            padding=ft.padding.only(right=16, top=16, bottom=8),
                        ),
                        
                        # قائمة التسبيحات
                        tasbih_list,
                        
                        ft.Container(height=20),
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=0,
                ),
                bgcolor=get_bg_color(),
                expand=True,
            )
        )
        page.update()
    
    def show_adhkar_page(category_id, category_name):
        """عرض صفحة الأذكار"""
        adhkar = get_adhkar_by_category(category_id)
        categories = get_categories()
        category_color = "#10b981"
        
        for cat in categories:
            if cat[0] == category_id:
                category_color = cat[3]
                break
        
        def reset_all(e):
            reset_adhkar_counts(category_id)
            show_adhkar_page(category_id, category_name)
        
        adhkar_cards = [create_adhkar_card(d, category_color) for d in adhkar]
        
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        create_header(category_name, show_back=True, show_settings=False),
                        
                        # زر إعادة التعيين
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        text="إعادة تعيين الكل",
                                        icon="refresh",
                                        on_click=reset_all,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.with_opacity(0.1, category_color),
                                            color=category_color,
                                        ),
                                    ),
                                    ft.Text(
                                        f"{len(adhkar)} ذكر",
                                        size=font_size - 2,
                                        color=ft.colors.with_opacity(0.6, get_text_color()),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        ),
                        
                        # قائمة الأذكار
                        ft.Column(
                            controls=adhkar_cards,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            spacing=0,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
                bgcolor=get_bg_color(),
                expand=True,
            )
        )
        page.update()
    
    def show_tasbih_counter_page(tasbih_id, name, count, target):
        """عرض صفحة عداد التسبيح"""
        nonlocal current_tasbih_count, current_tasbih_target
        current_tasbih_count = count
        current_tasbih_target = target
        
        count_text = ft.Text(
            str(current_tasbih_count),
            size=72,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR,
        )
        
        target_text = ft.Text(
            f"الهدف: {target}",
            size=font_size,
            color=ft.colors.with_opacity(0.6, get_text_color()),
        )
        
        progress_ring = ft.ProgressRing(
            value=min(current_tasbih_count / target, 1.0) if target > 0 else 0,
            width=220,
            height=220,
            stroke_width=12,
            color=PRIMARY_COLOR,
            bgcolor=ft.colors.with_opacity(0.2, PRIMARY_COLOR),
        )
        
        def increment(e):
            nonlocal current_tasbih_count
            current_tasbih_count += 1
            count_text.value = str(current_tasbih_count)
            progress_ring.value = min(current_tasbih_count / target, 1.0) if target > 0 else 0
            update_tasbih_count(tasbih_id, current_tasbih_count)
            page.update()
        
        def reset(e):
            nonlocal current_tasbih_count
            current_tasbih_count = 0
            count_text.value = "0"
            progress_ring.value = 0
            reset_tasbih_count(tasbih_id)
            page.update()
        
        counter_button = ft.Container(
            content=ft.Stack(
                controls=[
                    progress_ring,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                count_text,
                                target_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                        ),
                        width=220,
                        height=220,
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
            on_click=increment,
            ink=True,
            border_radius=110,
        )
        
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        create_header("التسبيح الإلكتروني", show_back=True, show_settings=False),
                        
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # اسم التسبيح
                                    ft.Container(
                                        content=ft.Text(
                                            name,
                                            size=font_size + 8,
                                            weight=ft.FontWeight.BOLD,
                                            color=get_text_color(),
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        padding=ft.padding.symmetric(vertical=24),
                                    ),
                                    
                                    # العداد الدائري
                                    ft.Container(
                                        content=counter_button,
                                        alignment=ft.alignment.center,
                                        padding=ft.padding.symmetric(vertical=32),
                                    ),
                                    
                                    # التعليمات
                                    ft.Text(
                                        "اضغط على الدائرة للتسبيح",
                                        size=font_size - 2,
                                        color=ft.colors.with_opacity(0.5, get_text_color()),
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    
                                    ft.Container(height=32),
                                    
                                    # زر إعادة التعيين
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            text="إعادة تعيين",
                                            icon="refresh",
                                            on_click=reset,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.colors.RED_400,
                                                color=ft.colors.WHITE,
                                                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                                            ),
                                        ),
                                        alignment=ft.alignment.center,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                            expand=True,
                            padding=16,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
                bgcolor=get_bg_color(),
                expand=True,
            )
        )
        page.update()
    
    def show_settings_page():
        """عرض صفحة الإعدادات"""
        nonlocal dark_mode, font_size
        
        def toggle_dark_mode(e):
            nonlocal dark_mode
            dark_mode = e.control.value
            save_setting("dark_mode", "true" if dark_mode else "false")
            page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
            show_settings_page()
        
        def change_font_size(e):
            nonlocal font_size
            font_size = int(e.control.value)
            save_setting("font_size", str(font_size))
            font_preview.value = f"حجم الخط: {font_size}"
            font_preview.size = font_size
            page.update()
        
        font_preview = ft.Text(
            f"حجم الخط: {font_size}",
            size=font_size,
            color=get_text_color(),
        )
        
        dark_mode_switch = ft.Switch(
            value=dark_mode,
            active_color=PRIMARY_COLOR,
            on_change=toggle_dark_mode,
        )
        
        font_slider = ft.Slider(
            min=14,
            max=28,
            value=font_size,
            divisions=14,
            active_color=PRIMARY_COLOR,
            on_change=change_font_size,
        )
        
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        create_header("الإعدادات", show_back=True, show_settings=False),
                        
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # الوضع الداكن
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Icon(
                                                            "dark_mode" if dark_mode else "light_mode",
                                                            color=PRIMARY_COLOR,
                                                            size=28,
                                                        ),
                                                        ft.Text(
                                                            "الوضع الداكن",
                                                            size=font_size,
                                                            weight=ft.FontWeight.W_500,
                                                            color=get_text_color(),
                                                        ),
                                                    ],
                                                    spacing=16,
                                                ),
                                                dark_mode_switch,
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        padding=20,
                                        border_radius=12,
                                        bgcolor=get_card_color(),
                                    ),
                                    
                                    ft.Container(height=16),
                                    
                                    # حجم الخط
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Icon(
                                                            "text_fields",
                                                            color=PRIMARY_COLOR,
                                                            size=28,
                                                        ),
                                                        ft.Text(
                                                            "حجم الخط",
                                                            size=font_size,
                                                            weight=ft.FontWeight.W_500,
                                                            color=get_text_color(),
                                                        ),
                                                    ],
                                                    spacing=16,
                                                ),
                                                ft.Container(height=12),
                                                font_slider,
                                                ft.Container(height=8),
                                                font_preview,
                                            ],
                                        ),
                                        padding=20,
                                        border_radius=12,
                                        bgcolor=get_card_color(),
                                    ),
                                    
                                    ft.Container(height=32),
                                    
                                    # معلومات التطبيق
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Icon("info_outline", color=PRIMARY_COLOR, size=40),
                                                ft.Text(
                                                    "حصن المسلم",
                                                    size=font_size + 4,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=get_text_color(),
                                                ),
                                                ft.Text(
                                                    "الإصدار 1.0.0",
                                                    size=font_size - 2,
                                                    color=ft.colors.with_opacity(0.6, get_text_color()),
                                                ),
                                                ft.Container(height=8),
                                                ft.Text(
                                                    "أذكار من الكتاب والسنة",
                                                    size=font_size - 2,
                                                    color=ft.colors.with_opacity(0.6, get_text_color()),
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=4,
                                        ),
                                        padding=32,
                                        border_radius=12,
                                        bgcolor=get_card_color(),
                                        alignment=ft.alignment.center,
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=16,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                bgcolor=get_bg_color(),
                expand=True,
            )
        )
        page.update()
    
    # عرض الصفحة الرئيسية
    show_home_page()

# تشغيل التطبيق
if __name__ == "__main__":
    ft.app(target=main)