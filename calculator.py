"""
Trading Position Calculator
Калькулятор расчета позиции по зонам
"""

import customtkinter as ctk
from tkinter import messagebox
import re


class TradingCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Trading Position Calculator")
        self.geometry("500x750")
        self.resizable(False, False)
        
        # Цвета
        self.colors = {
            "bg_dark": "#0d1117",
            "bg_card": "#161b22",
            "accent": "#58a6ff",
            "green": "#3fb950",
            "red": "#f85149",
            "yellow": "#d29922",
            "text": "#e6edf3",
            "text_dim": "#8b949e",
            "border": "#30363d"
        }
        
        # Параметры по таймфреймам
        self.tf_params = {
            "1h": {"entry_pct": 25, "stop_pct": 6},
            "2h": {"entry_pct": 22, "stop_pct": 15},
            "4h": {"entry_pct": 22, "stop_pct": 6}
        }
        self.rr_ratio = 1.8
        
        self.configure(fg_color=self.colors["bg_dark"])
        self._create_ui()
        
    def _create_ui(self):
        main = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Заголовок с кнопкой настроек
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame, text="POSITION CALCULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame, text="Расчёт позиции по зонам",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w")
        
        # Кнопка настроек
        ctk.CTkButton(
            header, text="⚙️", width=36, height=36,
            font=ctk.CTkFont(size=16),
            fg_color=self.colors["bg_card"],
            hover_color=self.colors["border"],
            corner_radius=8,
            command=self.open_settings
        ).pack(side="right", anchor="n")
        
        # === ВХОДНЫЕ ДАННЫЕ ===
        input_card = ctk.CTkFrame(main, fg_color=self.colors["bg_card"], corner_radius=12)
        input_card.pack(fill="x", pady=(0, 10))
        
        inp = ctk.CTkFrame(input_card, fg_color="transparent")
        inp.pack(fill="x", padx=15, pady=15)
        
        # Зона: верхняя и нижняя граница
        zone_row = ctk.CTkFrame(inp, fg_color="transparent")
        zone_row.pack(fill="x", pady=(0, 10))
        zone_row.grid_columnconfigure((0, 1), weight=1)
        
        self.entry_zone_high = self._input(zone_row, "Верхняя граница зоны", "100", 0, 0)
        self.entry_zone_low = self._input(zone_row, "Нижняя граница зоны", "95", 0, 1)
        
        # Направление: Long / Short
        dir_frame = ctk.CTkFrame(inp, fg_color="transparent")
        dir_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            dir_frame, text="Направление",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.dir_var = ctk.StringVar(value="LONG")
        dir_seg = ctk.CTkSegmentedButton(
            dir_frame, values=["LONG", "SHORT"],
            variable=self.dir_var,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#0d1117",
            selected_color=self.colors["green"],
            selected_hover_color="#2d8a3e",
            unselected_color="#0d1117",
            unselected_hover_color="#1a2332",
            command=self._on_direction_change
        )
        dir_seg.pack(fill="x")
        self.dir_seg = dir_seg
        
        # Таймфрейм
        tf_frame = ctk.CTkFrame(inp, fg_color="transparent")
        tf_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            tf_frame, text="Таймфрейм",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.tf_var = ctk.StringVar(value="1h")
        tf_seg = ctk.CTkSegmentedButton(
            tf_frame, values=["1h", "2h", "4h"],
            variable=self.tf_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#0d1117",
            selected_color=self.colors["accent"],
            selected_hover_color="#4090e0",
            unselected_color="#0d1117",
            unselected_hover_color="#1a2332"
        )
        tf_seg.pack(fill="x")
        
        # Депозит и Риск
        dep_row = ctk.CTkFrame(inp, fg_color="transparent")
        dep_row.pack(fill="x")
        dep_row.grid_columnconfigure((0, 1), weight=1)
        
        self.entry_deposit = self._input(dep_row, "Депозит ($)", "1000", 0, 0)
        self.entry_risk = self._input(dep_row, "Риск (%)", "1", 0, 1)
        
        # Кнопки
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            btn_frame, text="📋 ПАРСИТЬ",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45, corner_radius=10,
            fg_color=self.colors["border"],
            hover_color="#3d444d",
            command=self.parse_from_clipboard
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ctk.CTkButton(
            btn_frame, text="РАССЧИТАТЬ",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45, corner_radius=10,
            fg_color=self.colors["accent"],
            hover_color="#4090e0",
            command=self.calculate
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # === РЕЗУЛЬТАТЫ ===
        res_card = ctk.CTkFrame(main, fg_color=self.colors["bg_card"], corner_radius=12)
        res_card.pack(fill="x")
        
        res = ctk.CTkFrame(res_card, fg_color="transparent")
        res.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            res, text="РЕЗУЛЬТАТЫ",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Размер позиции
        pos_box = ctk.CTkFrame(res, fg_color="#1a2332", corner_radius=10)
        pos_box.pack(fill="x", pady=(0, 10))
        pos_in = ctk.CTkFrame(pos_box, fg_color="transparent")
        pos_in.pack(fill="x", padx=12, pady=12)
        
        ctk.CTkLabel(
            pos_in, text="Размер позиции",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w")
        
        self.lbl_position = ctk.CTkLabel(
            pos_in, text="—",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.lbl_position.pack(anchor="w")
        
        self.lbl_position_usd = ctk.CTkLabel(
            pos_in, text="Введите данные и нажмите Рассчитать",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        )
        self.lbl_position_usd.pack(anchor="w")
        
        # Точки: Вход, Стоп, Тейк
        prices_grid = ctk.CTkFrame(res, fg_color="transparent")
        prices_grid.pack(fill="x", pady=(0, 8))
        prices_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.lbl_entry = self._result_cell(prices_grid, "Вход", "—", self.colors["accent"], 0, 0)
        self.lbl_stop = self._result_cell(prices_grid, "Стоп", "—", self.colors["red"], 0, 1)
        self.lbl_take = self._result_cell(prices_grid, "Тейк", "—", self.colors["green"], 0, 2)
        
        # Риск $, Прибыль $, R:R
        money_grid = ctk.CTkFrame(res, fg_color="transparent")
        money_grid.pack(fill="x")
        money_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.lbl_risk_usd = self._result_cell(money_grid, "Риск $", "—", self.colors["red"], 0, 0)
        self.lbl_profit_usd = self._result_cell(money_grid, "Прибыль $", "—", self.colors["green"], 0, 1)
        self.lbl_rr = self._result_cell(money_grid, "R:R", "1:1.8", self.colors["yellow"], 0, 2)

    def _input(self, parent, label, default, row, col):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, padx=4, sticky="ew")
        
        # Заголовок
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 3))
        
        ctk.CTkLabel(
            header, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(side="left")
        
        # Поле ввода
        entry = ctk.CTkEntry(
            frame, height=36, corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#0d1117",
            border_color=self.colors["border"],
            border_width=1,
            text_color=self.colors["text"]
        )
        entry.pack(fill="x")
        entry.insert(0, default)
        
        # Маленькая кнопка вставки (V)
        paste_btn = ctk.CTkButton(
            header, text="V", width=20, height=16,
            font=ctk.CTkFont(size=9),
            fg_color=self.colors["border"],
            hover_color=self.colors["accent"],
            text_color=self.colors["text_dim"],
            corner_radius=4,
            command=lambda: self._do_paste(entry)
        )
        paste_btn.pack(side="right")
        
        # Привязка Ctrl+V к внутреннему виджету (англ + русс раскладка)
        try:
            inner = entry._entry
            inner.bind("<Control-v>", lambda e: self._do_paste(entry))
            inner.bind("<Control-V>", lambda e: self._do_paste(entry))
            # Русская раскладка: V = М
            inner.bind("<Control-igrave>", lambda e: self._do_paste(entry))  # м
            inner.bind("<Control-Igrave>", lambda e: self._do_paste(entry))  # М
            # Универсальный обработчик
            inner.bind("<Control-Key>", lambda e: self._handle_ctrl_key(e, entry))
        except:
            pass
        
        return entry
    
    def _handle_ctrl_key(self, event, entry):
        """Обработка Ctrl+клавиша (любая раскладка)"""
        # V на английской, М на русской (keycode 86)
        if event.keycode == 86:  # Физическая клавиша V
            self._do_paste(entry)
            return "break"
    
    def _do_paste(self, entry):
        """Вставка из буфера обмена"""
        try:
            clipboard = self.clipboard_get()
            cleaned = clipboard.strip()
            if cleaned:
                entry.delete(0, "end")
                entry.insert(0, cleaned)
        except:
            pass
        return "break"
    
    def _result_cell(self, parent, title, value, color, row, col):
        frame = ctk.CTkFrame(parent, fg_color="#1a2332", corner_radius=8, height=60)
        frame.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        frame.grid_propagate(False)
        
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            inner, text=title,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=self.colors["text_dim"]
        ).pack()
        
        lbl = ctk.CTkLabel(
            inner, text=value,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=color
        )
        lbl.pack()
        return lbl
    
    def _on_direction_change(self, value):
        """Меняем цвет кнопки в зависимости от направления"""
        if value == "LONG":
            self.dir_seg.configure(selected_color=self.colors["green"], selected_hover_color="#2d8a3e")
        else:
            self.dir_seg.configure(selected_color=self.colors["red"], selected_hover_color="#c73e3e")
    
    def open_settings(self):
        """Открыть окно настроек"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Настройки параметров")
        settings_window.geometry("420x550")
        settings_window.resizable(False, False)
        settings_window.configure(fg_color=self.colors["bg_dark"])
        
        # Делаем окно модальным
        settings_window.transient(self)
        settings_window.grab_set()
        
        # Прокручиваемый контейнер
        main = ctk.CTkScrollableFrame(
            settings_window, 
            fg_color="transparent",
            scrollbar_button_color=self.colors["border"]
        )
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main, text="НАСТРОЙКИ ПАРАМЕТРОВ",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.colors["text"]
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            main, text="Проценты рассчитываются от размера зоны",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(pady=(0, 15))
        
        # Словарь для хранения полей ввода
        self.settings_entries = {}
        
        for tf in ["1h", "2h", "4h"]:
            # Карточка для таймфрейма
            card = ctk.CTkFrame(main, fg_color=self.colors["bg_card"], corner_radius=10)
            card.pack(fill="x", pady=(0, 10))
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)
            
            # Заголовок таймфрейма
            ctk.CTkLabel(
                inner, text=tf.upper(),
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=self.colors["accent"]
            ).pack(anchor="w")
            
            # Поля ввода
            fields_frame = ctk.CTkFrame(inner, fg_color="transparent")
            fields_frame.pack(fill="x", pady=(8, 0))
            fields_frame.grid_columnconfigure((0, 1), weight=1)
            
            # Вход %
            entry_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
            entry_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            
            ctk.CTkLabel(
                entry_frame, text="Вход от верха зоны %",
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_dim"]
            ).pack(anchor="w")
            
            entry_pct = ctk.CTkEntry(
                entry_frame, height=32, corner_radius=6,
                fg_color="#0d1117", border_color=self.colors["border"],
                text_color=self.colors["text"]
            )
            entry_pct.pack(fill="x")
            entry_pct.insert(0, str(self.tf_params[tf]["entry_pct"]))
            
            # Стоп %
            stop_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
            stop_frame.grid(row=0, column=1, sticky="ew")
            
            ctk.CTkLabel(
                stop_frame, text="Стоп от края зоны %",
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_dim"]
            ).pack(anchor="w")
            
            stop_pct = ctk.CTkEntry(
                stop_frame, height=32, corner_radius=6,
                fg_color="#0d1117", border_color=self.colors["border"],
                text_color=self.colors["text"]
            )
            stop_pct.pack(fill="x")
            stop_pct.insert(0, str(self.tf_params[tf]["stop_pct"]))
            
            self.settings_entries[tf] = {"entry": entry_pct, "stop": stop_pct}
        
        # R:R настройка
        rr_card = ctk.CTkFrame(main, fg_color=self.colors["bg_card"], corner_radius=10)
        rr_card.pack(fill="x", pady=(0, 15))
        
        rr_inner = ctk.CTkFrame(rr_card, fg_color="transparent")
        rr_inner.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            rr_inner, text="Risk/Reward (R:R)",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["yellow"]
        ).pack(anchor="w")
        
        rr_frame = ctk.CTkFrame(rr_inner, fg_color="transparent")
        rr_frame.pack(fill="x", pady=(8, 0))
        
        ctk.CTkLabel(
            rr_frame, text="1 :",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        ).pack(side="left")
        
        self.rr_entry = ctk.CTkEntry(
            rr_frame, width=80, height=32, corner_radius=6,
            fg_color="#0d1117", border_color=self.colors["border"],
            text_color=self.colors["text"]
        )
        self.rr_entry.pack(side="left", padx=(5, 0))
        self.rr_entry.insert(0, str(self.rr_ratio))
        
        # Кнопки
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(5, 0))
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            btn_frame, text="↺ ПО УМОЛЧАНИЮ",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40, corner_radius=10,
            fg_color=self.colors["border"],
            hover_color="#3d444d",
            command=self.reset_to_defaults
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ctk.CTkButton(
            btn_frame, text="СОХРАНИТЬ",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40, corner_radius=10,
            fg_color=self.colors["green"],
            hover_color="#2d8a3e",
            command=lambda: self.save_settings(settings_window)
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")
    
    def reset_to_defaults(self):
        """Сбросить настройки по умолчанию"""
        defaults = {
            "1h": {"entry_pct": 25, "stop_pct": 6},
            "2h": {"entry_pct": 22, "stop_pct": 15},
            "4h": {"entry_pct": 22, "stop_pct": 6}
        }
        default_rr = 1.8
        
        # Обновляем поля в окне настроек
        for tf in ["1h", "2h", "4h"]:
            self.settings_entries[tf]["entry"].delete(0, "end")
            self.settings_entries[tf]["entry"].insert(0, str(defaults[tf]["entry_pct"]))
            
            self.settings_entries[tf]["stop"].delete(0, "end")
            self.settings_entries[tf]["stop"].insert(0, str(defaults[tf]["stop_pct"]))
        
        self.rr_entry.delete(0, "end")
        self.rr_entry.insert(0, str(default_rr))
    
    def save_settings(self, window):
        """Сохранить настройки"""
        try:
            for tf in ["1h", "2h", "4h"]:
                entry_val = float(self.settings_entries[tf]["entry"].get().replace(",", "."))
                stop_val = float(self.settings_entries[tf]["stop"].get().replace(",", "."))
                
                if entry_val <= 0 or stop_val <= 0:
                    raise ValueError("Значения должны быть > 0")
                
                self.tf_params[tf]["entry_pct"] = entry_val
                self.tf_params[tf]["stop_pct"] = stop_val
            
            rr_val = float(self.rr_entry.get().replace(",", "."))
            if rr_val <= 0:
                raise ValueError("R:R должен быть > 0")
            self.rr_ratio = rr_val
            
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте данные:\n{e}")
    
    def parse_from_clipboard(self):
        """Парсинг данных из буфера обмена"""
        try:
            text = self.clipboard_get()
        except:
            messagebox.showerror("Ошибка", "Буфер обмена пуст")
            return
        
        # Ищем таймфрейм (1h, 2h, 4h)
        tf_match = re.search(r'\b(1h|2h|4h)\b', text, re.IGNORECASE)
        if tf_match:
            tf = tf_match.group(1).lower()
            self.tf_var.set(tf)
        
        # Ищем направление (LONG/SHORT)
        if 'LONG' in text.upper():
            self.dir_var.set("LONG")
            self._on_direction_change("LONG")
        elif 'SHORT' in text.upper():
            self.dir_var.set("SHORT")
            self._on_direction_change("SHORT")
        
        # Ищем зону входа: $XX.XXXX - $XX.XXXX
        zone_match = re.search(r'\$?([\d.]+)\s*[-–]\s*\$?([\d.]+)', text)
        if zone_match:
            price1 = float(zone_match.group(1))
            price2 = float(zone_match.group(2))
            
            # Определяем какая цена выше
            zone_low = min(price1, price2)
            zone_high = max(price1, price2)
            
            # Заполняем поля
            self.entry_zone_high.delete(0, "end")
            self.entry_zone_high.insert(0, str(zone_high))
            
            self.entry_zone_low.delete(0, "end")
            self.entry_zone_low.insert(0, str(zone_low))
        
        if not zone_match:
            messagebox.showwarning("Внимание", "Не удалось найти зону входа в тексте")
        
    def _get_decimals(self, value_str):
        """Определить количество знаков после запятой"""
        value_str = value_str.replace(",", ".").strip()
        if "." in value_str:
            return len(value_str.split(".")[-1])
        return 0
    
    def calculate(self):
        try:
            zone_high_str = self.entry_zone_high.get().replace(",", ".").strip()
            zone_low_str = self.entry_zone_low.get().replace(",", ".").strip()
            
            zone_high = float(zone_high_str)
            zone_low = float(zone_low_str)
            deposit = float(self.entry_deposit.get().replace(",", ".").strip())
            risk_pct = float(self.entry_risk.get().replace(",", ".").strip())
            
            # Определяем количество знаков после запятой
            decimals = max(self._get_decimals(zone_high_str), self._get_decimals(zone_low_str), 2)
            
            if zone_high <= zone_low:
                raise ValueError("Верхняя граница должна быть выше нижней")
            if deposit <= 0 or risk_pct <= 0:
                raise ValueError("Депозит и риск должны быть > 0")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте данные:\n{e}")
            return
        
        # Получаем параметры по таймфрейму
        tf = self.tf_var.get()
        params = self.tf_params[tf]
        is_long = self.dir_var.get() == "LONG"
        
        # Размер зоны = 100%
        zone_size = zone_high - zone_low
        
        if is_long:
            # LONG: входим ниже верхней границы, стоп ниже нижней, тейк вверх
            entry_price = zone_high - (zone_size * params["entry_pct"] / 100)
            stop_price = zone_low - (zone_size * params["stop_pct"] / 100)
            stop_distance = entry_price - stop_price
            take_distance = stop_distance * self.rr_ratio
            take_price = entry_price + take_distance
        else:
            # SHORT: входим выше нижней границы, стоп выше верхней, тейк вниз
            entry_price = zone_low + (zone_size * params["entry_pct"] / 100)
            stop_price = zone_high + (zone_size * params["stop_pct"] / 100)
            stop_distance = stop_price - entry_price
            take_distance = stop_distance * self.rr_ratio
            take_price = entry_price - take_distance
        
        # Размер позиции
        risk_usd = deposit * (risk_pct / 100)
        position_size = risk_usd / stop_distance
        position_usd = position_size * entry_price
        
        # Потенциальная прибыль
        profit_usd = position_size * take_distance
        
        # Обновляем UI
        self.lbl_position.configure(text=f"{position_size:,.4f} ед.")
        self.lbl_position_usd.configure(text=f"= ${position_usd:,.2f} на позицию")
        
        self.lbl_entry.configure(text=f"{entry_price:,.{decimals}f}")
        self.lbl_stop.configure(text=f"{stop_price:,.{decimals}f}")
        self.lbl_take.configure(text=f"{take_price:,.{decimals}f}")
        
        self.lbl_risk_usd.configure(text=f"${risk_usd:,.2f}")
        self.lbl_profit_usd.configure(text=f"${profit_usd:,.2f}")
        self.lbl_rr.configure(text=f"1:{self.rr_ratio}")


if __name__ == "__main__":
    app = TradingCalculator()
    app.mainloop()
