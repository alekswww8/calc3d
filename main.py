import os, glob
from google.colab import files

%cd /content/calc3d

# 1. Записываем именно ВАШ рабочий код калькулятора
with open('main.py', 'w', encoding='utf-8') as f:
    f.write('''import os
import struct
import math
import sqlite3
import urllib.parse
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooserListView
from kivy.core.clipboard import Clipboard
from kivy.graphics import Mesh, Color
from kivy.graphics.opengl import GL_TRIANGLES

LANGUAGES = {
    "UA": {
        "title": "3D КАЛЬКУЛЯТОР", "btn_file": "📁 ОБРАТИ STL", "btn_view3d": "👁️ 3D ПЕРЕГЛЯД",
        "no_file": "Файл не обрано", "loading": "Триває розрахунок...", "history": "📋 Історія",
        "vase_on": "🏺 Режим вази: УВІМК", "vase_off": "🏺 Режим вази: ВИМК",
        "walls": "Стінки (периметри):", "infill": "Заповнення (%):", "spool": "Котушка 1 кг (грн):",
        "hour": "Верстат + світло (грн/год):", "markup": "Маржа / Націнка (x):", "speed": "Швидкість (см³/год):",
        "weight": "Вага деталі (г):", "time": "Час друку (год):", "nozzle": "Сопло",
        "initial_result": "Оберіть деталь — розрахунок з'явиться тут", "btn_share": "📤 ВІДПРАВИТИ ЧЕК",
        "btn_save": "💾 ЗБЕРЕГТИ В БАЗУ", "share_title": "Відправка чека",
        "share_hint": "Чек скопійовано в буфер! Оберіть додаток:", "btn_tg": "✈️ Telegram",
        "btn_viber": "🟣 Viber", "btn_wa": "🟢 WhatsApp", "btn_copy": "📋 Тільки скопіювати",
        "saved_msg": "Замовлення успішно збережено!", "copied_msg": "Чек скопійовано в буфер обміну!",
        "history_title": "ІСТОРІЯ ЗАМОВЛЕНЬ", "history_empty": "Історія порожня", "btn_clear": "🗑 Очистити",
        "btn_close": "Закрити", "vol": "Об'єм", "area": "Площа", "receipt_header": "🧾 Розрахунок вартості 3D-друку",
        "receipt_file": "Файл", "receipt_mat": "Матеріал", "receipt_weight": "Вага", "receipt_time": "Час",
        "receipt_total": "Разом до сплати", "viewer_title": "3D Перегляд моделі", "viewer_hint": "Свайп: Обертання | Два пальці: Зум"
    },
    "RU": {
        "title": "3D КАЛЬКУЛЯТОР", "btn_file": "📁 ВЫБРАТЬ STL", "btn_view3d": "👁️ 3D ПРОСМОТР",
        "no_file": "Файл не выбран", "loading": "Идет расчет...", "history": "📋 История",
        "vase_on": "🏺 Режим вазы: ВКЛ", "vase_off": "🏺 Режим вазы: ВЫКЛ",
        "walls": "Стенки (периметры):", "infill": "Заполнение (%):", "spool": "Катушка 1 кг (грн):",
        "hour": "Станок + свет (грн/ч):", "markup": "Маржа / Наценка (x):", "speed": "Скорость (см³/ч):",
        "weight": "Вес детали (г):", "time": "Время печати (ч):", "nozzle": "Сопло",
        "initial_result": "Выберите деталь — расчет появится здесь", "btn_share": "📤 ОТПРАВИТЬ ЧЕК",
        "btn_save": "💾 СОХРАНИТЬ В БАЗУ", "share_title": "Отправка чека",
        "share_hint": "Чек скопирован в буфер! Выберите мессенджер:", "btn_tg": "✈️ Telegram",
        "btn_viber": "🟣 Viber", "btn_wa": "🟢 WhatsApp", "btn_copy": "📋 Только скопировать",
        "saved_msg": "Заказ успешно сохранен!", "copied_msg": "Чек скопирован в буфер обмена!",
        "history_title": "ИСТОРИЯ ЗАКАЗОВ", "history_empty": "История пуста", "btn_clear": "🗑 Очистить",
        "btn_close": "Закрыть", "vol": "Объем", "area": "Площадь", "receipt_header": "🧾 Расчет стоимости 3D-печати",
        "receipt_file": "Файл", "receipt_mat": "Материал", "receipt_weight": "Вес", "receipt_time": "Время",
        "receipt_total": "Итого к оплате", "viewer_title": "3D Просмотр модели", "viewer_hint": "Свайп: Вращение | Два пальца: Зум"
    },
    "EN": {
        "title": "3D PRINT CALC", "btn_file": "📁 CHOOSE STL", "btn_view3d": "👁️ 3D VIEW",
        "no_file": "No file chosen", "loading": "Calculating...", "history": "📋 History",
        "vase_on": "🏺 Vase mode: ON", "vase_off": "🏺 Vase mode: OFF",
        "walls": "Perimeters (walls):", "infill": "Infill (%):", "spool": "Spool 1 kg (uah):",
        "hour": "Printer + power (uah/h):", "markup": "Markup / Margin (x):", "speed": "Speed (cm³/h):",
        "weight": "Part weight (g):", "time": "Print time (h):", "nozzle": "Nozzle",
        "initial_result": "Select part — quote will appear here", "btn_share": "📤 SHARE QUOTE",
        "btn_save": "💾 SAVE TO DB", "share_title": "Share Quote",
        "share_hint": "Quote copied to clipboard! Select app:", "btn_tg": "✈️ Telegram",
        "btn_viber": "🟣 Viber", "btn_wa": "🟢 WhatsApp", "btn_copy": "📋 Copy only",
        "saved_msg": "Order saved successfully!", "copied_msg": "Quote copied to clipboard!",
        "history_title": "ORDER HISTORY", "history_empty": "History is empty", "btn_clear": "🗑 Clear",
        "btn_close": "Close", "vol": "Volume", "area": "Area", "receipt_header": "🧾 3D Print Quote",
        "receipt_file": "File", "receipt_mat": "Material", "receipt_weight": "Weight", "receipt_time": "Time",
        "receipt_total": "Total Amount", "viewer_title": "3D Model Viewer", "viewer_hint": "Swipe: Rotate | Pinch: Zoom"
    }
}

DENSITIES = {"PLA": 1.24, "CoPET": 1.27, "PETG": 1.27, "ABS": 1.04, "TPU": 1.21}
DEFAULT_PRICES = {"PLA": "800", "CoPET": "700", "PETG": "700", "ABS": "650", "TPU": "1100"}
NOZZLE_SPEEDS = {0.2: "8", 0.4: "18", 0.6: "28", 0.8: "38"}

KV = """
<StyledTextInput@TextInput>:
    multiline: False
    background_color: 0.08, 0.09, 0.12, 1
    foreground_color: 1, 1, 1, 1
    cursor_color: 0.23, 0.51, 0.96, 1
    size_hint_y: None
    height: '36dp'
    font_size: '14sp'
    padding: ['8dp', '8dp']

<TagButton@Button>:
    background_normal: ''
    background_color: 0.12, 0.14, 0.19, 1
    color: 0.8, 0.85, 0.9, 1
    font_size: '12sp'
    bold: True
    size_hint_y: None
    height: '34dp'

ScrollView:
    do_scroll_x: False
    BoxLayout:
        id: main_layout
        orientation: 'vertical'
        padding: '12dp'
        spacing: '8dp'
        size_hint_y: None
        height: self.minimum_height

        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: '6dp'
            Label:
                id: lbl_title
                text: "3D КАЛЬКУЛЯТОР"
                font_size: '16sp'
                bold: True
                color: 0.38, 0.65, 0.98, 1
                halign: 'left'
                valign: 'middle'
                text_size: self.size
            TagButton:
                id: btn_lang_ua
                text: "UA"
                size_hint_x: None
                width: '36dp'
                on_release: app.set_lang('UA')
            TagButton:
                id: btn_lang_ru
                text: "RU"
                size_hint_x: None
                width: '36dp'
                on_release: app.set_lang('RU')
            TagButton:
                id: btn_lang_en
                text: "EN"
                size_hint_x: None
                width: '36dp'
                on_release: app.set_lang('EN')
            Button:
                id: btn_history
                text: "📋"
                size_hint_x: None
                width: '42dp'
                background_normal: ''
                background_color: 0.16, 0.19, 0.25, 1
                on_release: app.open_history()

        BoxLayout:
            size_hint_y: None
            height: '42dp'
            spacing: '6dp'
            Button:
                id: btn_file
                text: "📁 ОБРАТИ STL"
                bold: True
                font_size: '13sp'
                background_normal: ''
                background_color: 0.15, 0.39, 0.92, 1
                on_release: app.open_file_picker()
            Button:
                id: btn_view3d
                text: "👁️ 3D"
                size_hint_x: None
                width: '75dp'
                bold: True
                font_size: '13sp'
                disabled: True
                background_normal: ''
                background_color: 0.01, 0.52, 0.78, 1
                on_release: app.open_3d_viewer()

        Label:
            id: lbl_file_info
            text: "Файл не обрано"
            font_size: '12sp'
            color: 0.8, 0.84, 0.9, 1
            size_hint_y: None
            height: '24dp'

        BoxLayout:
            id: mat_box
            size_hint_y: None
            height: '34dp'
            spacing: '4dp'

        BoxLayout:
            id: nz_box
            size_hint_y: None
            height: '34dp'
            spacing: '4dp'

        Button:
            id: btn_vase
            text: "🏺 Режим вази: ВИМК"
            size_hint_y: None
            height: '36dp'
            font_size: '13sp'
            bold: True
            background_normal: ''
            background_color: 0.16, 0.19, 0.25, 1
            on_release: app.toggle_vase()

        GridLayout:
            id: grid_inputs
            cols: 2
            size_hint_y: None
            height: self.minimum_height
            spacing: '6dp'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '75dp'
            padding: '8dp'
            canvas.before:
                Color:
                    rgba: 0.07, 0.11, 0.08, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8]
            Label:
                id: lbl_cost
                text: "0.00 грн"
                font_size: '22sp'
                bold: True
                color: 0.2, 0.83, 0.6, 1
            Label:
                id: lbl_detail
                text: "Оберіть деталь"
                font_size: '11sp'
                color: 0.75, 0.8, 0.85, 1

        BoxLayout:
            size_hint_y: None
            height: '42dp'
            spacing: '8dp'
            Button:
                id: btn_share
                text: "📤 ВІДПРАВИТИ"
                bold: True
                font_size: '13sp'
                background_normal: ''
                background_color: 0.31, 0.27, 0.9, 1
                on_release: app.open_share_dialog()
            Button:
                id: btn_save
                text: "💾 ЗБЕРЕГТИ"
                bold: True
                font_size: '13sp'
                background_normal: ''
                background_color: 0.02, 0.59, 0.41, 1
                on_release: app.save_order()
"""

def parse_stl_data(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 84:
        return 0.0, 0.0, []
    size = os.path.getsize(file_path)
    triangles = []
    try:
        with open(file_path, 'rb') as f:
            f.seek(80)
            raw_cnt = f.read(4)
            if len(raw_cnt) == 4:
                num = struct.unpack('<I', raw_cnt)[0]
                if abs(size - (84 + num * 50)) <= 2:
                    total_vol, total_area = 0.0, 0.0
                    batch = 5000 * 50
                    step = max(1, num // 30000)
                    idx = 0
                    while True:
                        raw = f.read(batch)
                        if not raw:
                            break
                        n = len(raw) // 50
                        for i in range(n):
                            v = struct.unpack_from('<9f', raw, i * 50 + 12)
                            ax, ay, az = v[0], v[1], v[2]
                            bx, by, bz = v[3], v[4], v[5]
                            cx, cy, cz = v[6], v[7], v[8]
                            total_vol += (1.0 / 6.0) * (-cx*by*az + bx*cy*az + cx*ay*bz - ax*cy*bz - bx*ay*cz + ax*by*cz)
                            abx, handy_y = bx - ax, by - ay
                            abz = bz - az
                            acx, acy, acz = cx - ax, cy - ay, cz - az
                            cr_x = handy_y * acz - abz * acy
                            cr_y = handy_y * acx - abx * acz
                            cr_z = abx * acy - handy_y * acx
                            mag = math.sqrt(cr_x**2 + cr_y**2 + cr_z**2)
                            total_area += 0.5 * mag
                            if idx % step == 0:
                                triangles.extend([ax, ay, az, bx, by, bz, cx, cy, cz])
                            idx += 1
                    return abs(total_vol) / 1000.0, total_area / 100.0, triangles
    except:
        pass
    return 0.0, 0.0, []

class Mobile3DView(Widget):
    def __init__(self, raw_points, **kwargs):
        super().__init__(**kwargs)
        self.raw_points = raw_points
        self.rot_x = 25.0
        self.rot_y = -35.0
        self.zoom = 1.0
        self.touch_start = None
        self.normalize_model()
        self.bind(size=self.draw_scene, pos=self.draw_scene)

    def normalize_model(self):
        if not self.raw_points:
            self.coords = []
            return
        xs = self.raw_points[0::3]
        ys = self.raw_points[1::3]
        zs = self.raw_points[2::3]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        cx, cy, cz = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0, (min_z + max_z) / 2.0
        max_dim = max(max_x - min_x, max_y - min_y, max_z - min_z, 1.0)
        self.scale_factor = 220.0 / max_dim

        self.coords = []
        for i in range(0, len(self.raw_points), 3):
            self.coords.append((self.raw_points[i] - cx) * self.scale_factor)
            self.coords.append((self.raw_points[i+1] - cy) * self.scale_factor)
            self.coords.append((self.raw_points[i+2] - cz) * self.scale_factor)

    def project(self, x, y, z):
        rad_x = math.radians(self.rot_x)
        rad_y = math.radians(self.rot_y)
        x1 = x * math.cos(rad_y) + z * math.sin(rad_y)
        z1 = -x * math.sin(rad_y) + z * math.cos(rad_y)
        y2 = y * math.cos(rad_x) - z1 * math.sin(rad_x)
        return self.center_x + x1 * self.zoom, self.center_y + y2 * self.zoom

    def draw_scene(self, *args):
        self.canvas.clear()
        if not hasattr(self, 'coords') or not self.coords:
            return
        with self.canvas:
            Color(0.95, 0.48, 0.15, 1)
            v_list, idx_list, count = [], [], 0
            for i in range(0, len(self.coords), 9):
                px1, py1 = self.project(self.coords[i], self.coords[i+1], self.coords[i+2])
                px2, py2 = self.project(self.coords[i+3], self.coords[i+4], self.coords[i+5])
                px3, py3 = self.project(self.coords[i+6], self.coords[i+7], self.coords[i+8])
                v_list.extend([px1, py1, 0, 0, px2, py2, 0, 0, px3, py3, 0, 0])
                idx_list.extend([count, count+1, count+2])
                count += 3
            Mesh(vertices=v_list, indices=idx_list, mode='triangles')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_start = touch.pos
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_start:
            dx, dy = touch.pos[0] - self.touch_start[0], touch.pos[1] - self.touch_start[1]
            self.rot_y += dx * 0.4
            self.rot_x -= dy * 0.4
            self.touch_start = touch.pos
            self.draw_scene()
            return True
        return super().on_touch_move(touch)

class StudioCalcMobileApp(App):
    def build(self):
        self.cur_lang = "UA"
        self.material = "CoPET"
        self.nozzle = 0.4
        self.vase_mode = False
        self.vol_cm3 = 0.0
        self.area_cm2 = 0.0
        self.cur_file = "Деталь"
        self.total_cost = 0.0
        self.mesh_points = []
        self.db_path = os.path.join(self.user_data_dir, "orders.db")
        self.init_db()
        self.root = Builder.load_string(KV)
        self.init_interface()
        self.apply_language()
        return self.root

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dt TEXT, filename TEXT, material TEXT, weight REAL, hours REAL, cost REAL
            )
        """)
        conn.commit()
        conn.close()

    def tr(self, key):
        return LANGUAGES[self.cur_lang].get(key, key)

    def init_interface(self):
        mb = self.root.ids.mat_box
        self.mat_btns = {}
        for m in ["PLA", "CoPET", "PETG", "ABS", "TPU"]:
            b = Button(text=m, font_size='11sp', bold=True, background_normal='', background_color=(0.12, 0.14, 0.19, 1))
            b.bind(on_release=lambda btn, name=m: self.set_mat(name))
            self.mat_btns[m] = b
            mb.addWidget(b)

        nb = self.root.ids.nz_box
        self.nz_btns = {}
        for nz in [0.2, 0.4, 0.6, 0.8]:
            b = Button(text=f"Ø {nz}", font_size='11sp', bold=True, background_normal='', background_color=(0.12, 0.14, 0.19, 1))
            b.bind(on_release=lambda btn, size=nz: self.set_nozzle(size))
            self.nz_btns[nz] = b
            nb.addWidget(b)

        gi = self.root.ids.grid_inputs
        self.inputs, self.labels = {}, {}
        fields = [
            ("walls", "3"), ("infill", "20"), ("spool", "700"), ("hour", "15"),
            ("markup", "1.2"), ("speed", "18"), ("weight", "0.0"), ("time", "0.0")
        ]
        from kivy.uix.textinput import TextInput
        for k, val in fields:
            lbl = Label(text=self.tr(k), font_size='12sp', color=(0.85, 0.88, 0.92, 1), size_hint_y=None, height='36dp', halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            inp = TextInput(text=val, multiline=False, size_hint_y=None, height='36dp', font_size='13sp',
                            background_color=(0.08, 0.09, 0.12, 1), foreground_color=(1, 1, 1, 1))
            inp.bind(text=self.recalc)
            self.labels[k] = lbl
            self.inputs[k] = inp
            gi.addWidget(lbl)
            gi.addWidget(inp)
        self.update_selector_styles()

    def set_lang(self, code):
        self.cur_lang = code
        self.apply_language()

    def apply_language(self):
        ids = self.root.ids
        ids.lbl_title.text = self.tr("title")
        ids.btn_file.text = self.tr("btn_file")
        ids.btn_view3d.text = self.tr("btn_view3d")
        ids.btn_vase.text = self.tr("vase_on") if self.vase_mode else self.tr("vase_off")
        ids.btn_share.text = self.tr("btn_share")
        ids.btn_save.text = self.tr("btn_save")
        for k, lbl in self.labels.items():
            lbl.text = self.tr(k)
        for c in ["UA", "RU", "EN"]:
            ids[f"btn_lang_{c.lower()}"].background_color = (0.23, 0.51, 0.96, 1) if c == self.cur_lang else (0.12, 0.14, 0.19, 1)
        if self.vol_cm3 <= 0:
            ids.lbl_file_info.text = self.tr("no_file")
            ids.lbl_detail.text = self.tr("initial_result")
        else:
            ids.lbl_file_info.text = f"{self.cur_file} | {self.tr('vol')}: {self.vol_cm3:.2f} cm³"
        self.recalc()

    def set_mat(self, m):
        self.material = m
        if m in DEFAULT_PRICES:
            self.inputs["spool"].text = DEFAULT_PRICES[m]
        self.update_selector_styles()
        self.recalc()

    def set_nozzle(self, nz):
        self.nozzle = nz
        self.inputs["speed"].text = NOZZLE_SPEEDS.get(nz, "18")
        self.update_selector_styles()
        self.recalc()

    def toggle_vase(self):
        self.vase_mode = not self.vase_mode
        self.root.ids.btn_vase.text = self.tr("vase_on") if self.vase_mode else self.tr("vase_off")
        self.root.ids.btn_vase.background_color = (0.85, 0.45, 0.05, 1) if self.vase_mode else (0.16, 0.19, 0.25, 1)
        self.recalc()

    def update_selector_styles(self):
        for k, b in self.mat_btns.items():
            b.background_color = (0.15, 0.39, 0.92, 1) if k == self.material else (0.12, 0.14, 0.19, 1)
        for k, b in self.nz_btns.items():
            b.background_color = (0.85, 0.45, 0.05, 1) if k == self.nozzle else (0.12, 0.14, 0.19, 1)

    def open_file_picker(self):
        content = BoxLayout(orientation='vertical', spacing='6dp', padding='6dp')
        start_dir = "/sdcard/Download" if os.path.exists("/sdcard/Download") else os.path.expanduser("~")
        fc = FileChooserListView(path=start_dir, filters=['*.stl', '*.STL'])
        content.addWidget(fc)
        btn_box = BoxLayout(size_hint_y=None, height='40dp', spacing='8dp')
        btn_ok = Button(text="OK", bold=True, background_normal='', background_color=(0.15, 0.39, 0.92, 1))
        btn_cn = Button(text=self.tr("btn_close"), bold=True, background_normal='', background_color=(0.2, 0.24, 0.32, 1))
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cn)
        content.addWidget(btn_box)

        pop = Popup(title=self.tr("btn_file"), content=content, size_hint=(0.95, 0.95))
        def on_ok(b):
            if fc.selection:
                self.on_file_selected(fc.selection)
            pop.dismiss()
        btn_ok.bind(on_release=on_ok)
        btn_cn.bind(on_release=pop.dismiss)
        pop.open()

    def on_file_selected(self, selection):
        if selection and selection[0].lower().endswith(".stl"):
            path = selection[0]
            self.cur_file = os.path.basename(path)
            self.root.ids.lbl_file_info.text = self.tr("loading")
            vol, area, points = parse_stl_data(path)
            self.vol_cm3, self.area_cm2, self.mesh_points = vol, area, points
            self.root.ids.lbl_file_info.text = f"{self.cur_file} | {self.tr('vol')}: {vol:.2f} cm³"
            self.root.ids.btn_view3d.disabled = (len(points) == 0)
            self.recalc()

    def open_3d_viewer(self):
        if not self.mesh_points:
            return
        box = BoxLayout(orientation='vertical', padding='8dp', spacing='6dp')
        box.addWidget(Mobile3DView(self.mesh_points))
        box.addWidget(Label(text=self.tr("viewer_hint"), font_size='12sp', color=(0.6, 0.65, 0.7, 1), size_hint_y=None, height='24dp'))
        btn_c = Button(text=self.tr("btn_close"), size_hint_y=None, height='38dp', bold=True, background_normal='', background_color=(0.18, 0.22, 0.28, 1))
        box.addWidget(btn_c)
        pop = Popup(title=f"{self.tr('viewer_title')} — {self.cur_file}", content=box, size_hint=(0.95, 0.9))
        btn_c.bind(on_release=pop.dismiss)
        pop.open()

    def recalc(self, *args):
        if self.vol_cm3 <= 0:
            return
        try:
            walls = float(self.inputs["walls"].text or 3)
            infill = float(self.inputs["infill"].text or 20) / 100.0
            spd = max(1.0, float(self.inputs["speed"].text or 18))
            dens = DENSITIES.get(self.material, 1.27)
            if self.vase_mode:
                u_vol = self.area_cm2 * ((self.nozzle * 1.1) / 10.0)
            else:
                s_vol = self.area_cm2 * ((walls * self.nozzle) / 10.0)
                u_vol = self.vol_cm3 if s_vol >= self.vol_cm3 or infill >= 0.99 else s_vol + (self.vol_cm3 - s_vol) * infill
            calc_w = u_vol * dens
            calc_t = u_vol / spd
            self.inputs["weight"].text = f"{calc_w:.1f}"
            self.inputs["time"].text = f"{calc_t:.2f}"
            spool_c = float(self.inputs["spool"].text or 700)
            hour_r = float(self.inputs["hour"].text or 15)
            markup = float(self.inputs["markup"].text or 1.2)
            self.total_cost = ((spool_c / 1000.0) * calc_w + hour_r * calc_t) * markup
            sym = "грн" if self.cur_lang != "EN" else "uah"
            self.root.ids.lbl_cost.text = f"{self.total_cost:.2f} {sym}"
            self.root.ids.lbl_detail.text = f"{self.material} ({calc_w:.1f} g) | {calc_t:.2f} h | Ø{self.nozzle} mm"
        except:
            pass

    def get_receipt_text(self):
        sym = "грн" if self.cur_lang != "EN" else "uah"
        return (
            f"{self.tr('receipt_header')}\\n"
            f"• {self.tr('receipt_file')}: {self.cur_file}\\n"
            f"• {self.tr('receipt_mat')}: {self.material}\\n"
            f"• {self.tr('nozzle')}: Ø{self.nozzle} mm\\n"
            f"• {self.tr('receipt_weight')}: {self.inputs['weight'].text} g | {self.tr('receipt_time')}: {self.inputs['time'].text} h\\n"
            f"────────────────────────\\n"
            f"{self.tr('receipt_total')}: {self.total_cost:.2f} {sym}"
        )

    def open_share_dialog(self):
        if self.total_cost <= 0:
            return
        Clipboard.copy(self.get_receipt_text())
        enc = urllib.parse.quote(self.get_receipt_text())
        box = BoxLayout(orientation='vertical', spacing='8dp', padding='10dp')
        box.addWidget(Label(text=self.tr("share_hint"), font_size='13sp', color=(0.38, 0.65, 0.98, 1)))
        from webbrowser import open as open_url
        def share_to(uri):
            open_url(uri)
            pop.dismiss()
        for name, uri, col in [
            (self.tr("btn_tg"), f"tg://msg_url?text={enc}", (0.13, 0.62, 0.85, 1)),
            (self.tr("btn_viber"), f"viber://forward?text={enc}", (0.45, 0.38, 0.95, 1)),
            (self.tr("btn_wa"), f"whatsapp://send?text={enc}", (0.15, 0.83, 0.4, 1)),
        ]:
            b = Button(text=name, background_normal='', background_color=col, size_hint_y=None, height='38dp', bold=True)
            b.bind(on_release=lambda x, u=uri: share_to(u))
            box.addWidget(b)
        pop = Popup(title=self.tr("share_title"), content=box, size_hint=(0.85, 0.55))
        pop.open()

    def save_order(self):
        if self.total_cost <= 0:
            return
        conn = sqlite3.connect(self.db_path)
        conn.cursor().execute("INSERT INTO orders (dt, filename, material, weight, hours, cost) VALUES (?, ?, ?, ?, ?, ?)",
                    (datetime.now().strftime("%d.%m %H:%M"), self.cur_file, self.material,
                     float(self.inputs["weight"].text or 0), float(self.inputs["time"].text or 0), round(self.total_cost, 2)))
        conn.commit()
        conn.close()
        box = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        box.addWidget(Label(text=self.tr("saved_msg")))
        btn = Button(text="OK", size_hint_y=None, height='36dp')
        box.addWidget(btn)
        p = Popup(title="", content=box, size_hint=(0.75, 0.3))
        btn.bind(on_release=p.dismiss)
        p.open()

    def open_history(self):
        conn = sqlite3.connect(self.db_path)
        rows = conn.cursor().execute("SELECT dt, filename, material, weight, cost FROM orders ORDER BY id DESC").fetchall()
        conn.close()
        box = BoxLayout(orientation='vertical', padding='8dp', spacing='6dp')
        scroll = ScrollView()
        c_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing='4dp')
        c_box.bind(minimum_height=c_box.setter('height'))
        sym = "грн" if self.cur_lang != "EN" else "uah"
        if not rows:
            c_box.addWidget(Label(text=self.tr("history_empty"), size_hint_y=None, height='40dp', color=(0.6, 0.65, 0.7, 1)))
        else:
            for r in rows:
                row_l = BoxLayout(size_hint_y=None, height='38dp', padding='4dp')
                row_l.addWidget(Label(text=f"{r[0]} | {r[1]}", font_size='11sp', halign='left', size_hint_x=0.5))
                row_l.addWidget(Label(text=f"{r[2]} ({r[3]}g)", font_size='11sp', size_hint_x=0.25))
                row_l.addWidget(Label(text=f"{r[4]:.2f} {sym}", font_size='12sp', bold=True, color=(0.2, 0.83, 0.6, 1), size_hint_x=0.25))
                c_box.addWidget(row_l)
        scroll.addWidget(c_box)
        box.addWidget(scroll)
        btn_box = BoxLayout(size_hint_y=None, height='38dp', spacing='8dp')
        btn_clr = Button(text=self.tr("btn_clear"), background_normal='', background_color=(0.86, 0.15, 0.15, 1), bold=True)
        def clr(b):
            conn = sqlite3.connect(self.db_path)
            conn.cursor().execute("DELETE FROM orders")
            conn.commit()
            conn.close()
            p.dismiss()
        btn_clr.bind(on_release=clr)
        btn_box.addWidget(btn_clr)
        btn_cls = Button(text=self.tr("btn_close"), background_normal='', background_color=(0.2, 0.24, 0.32, 1), bold=True)
        btn_cls.bind(on_release=lambda b: p.dismiss())
        btn_box.addWidget(btn_cls)
        box.addWidget(btn_box)
        p = Popup(title=self.tr("history_title"), content=box, size_hint=(0.9, 0.8))
        p.open()

if __name__ == '__main__':
    StudioCalcMobileApp().run()''')

print("Файл main.py с вашим кодом успешно создан!")

# 2. Настраиваем buildozer.spec
!git checkout -- buildozer.spec
!sed -i 's/^requirements = .*/requirements = python3,kivy/' buildozer.spec
!sed -i 's/^#android.permissions = .*/android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET/' buildozer.spec

# 3. Собираем APK
!rm -rf bin/*.apk
!buildozer -v -y android debug

# 4. Скачивание
apks = glob.glob('bin/*.apk')
if apks:
    print("Готово! Скачивается:", apks[0])
    files.download(apks[0])
else:
    print("Сборка не удалась.")
