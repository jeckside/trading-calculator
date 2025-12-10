"""
Trading Position Calculator
Калькулятор расчета позиции по зонам
"""

import customtkinter as ctk
from tkinter import messagebox


class TradingCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Trading Position Calculator")
        self.geometry("500x680")
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
        
        # Заголовок
        ctk.CTkLabel(
            main, text="POSITION CALCULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors["text"]
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            main, text="Расчёт позиции по зонам",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors["text_dim"]
        ).pack(pady=(0, 15))
        
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
        
        # Кнопка
        ctk.CTkButton(
            main, text="РАССЧИТАТЬ",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            height=45, corner_radius=10,
            fg_color=self.colors["accent"],
            hover_color="#4090e0",
            command=self.calculate
        ).pack(fill="x", pady=15)
        
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
        
        ctk.CTkLabel(
            frame, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 3))
        
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
        return entry
    
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
        
    def calculate(self):
        try:
            zone_high = float(self.entry_zone_high.get().replace(",", ".").strip())
            zone_low = float(self.entry_zone_low.get().replace(",", ".").strip())
            deposit = float(self.entry_deposit.get().replace(",", ".").strip())
            risk_pct = float(self.entry_risk.get().replace(",", ".").strip())
            
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
        
        # Размер зоны = 100%
        zone_size = zone_high - zone_low
        
        # Расчёт точек
        # Точка входа: X% от размера зоны вниз от верхней границы
        entry_price = zone_high - (zone_size * params["entry_pct"] / 100)
        
        # Стоп: Y% от размера зоны вниз от нижней границы
        stop_price = zone_low - (zone_size * params["stop_pct"] / 100)
        
        # Расстояние стопа
        stop_distance = entry_price - stop_price
        
        # Тейк: R:R 1:1.8
        take_distance = stop_distance * self.rr_ratio
        take_price = entry_price + take_distance
        
        # Размер позиции
        risk_usd = deposit * (risk_pct / 100)
        position_size = risk_usd / stop_distance
        position_usd = position_size * entry_price
        
        # Потенциальная прибыль
        profit_usd = position_size * take_distance
        
        # Обновляем UI
        self.lbl_position.configure(text=f"{position_size:,.4f} ед.")
        self.lbl_position_usd.configure(text=f"= ${position_usd:,.2f} на позицию")
        
        self.lbl_entry.configure(text=f"{entry_price:,.2f}")
        self.lbl_stop.configure(text=f"{stop_price:,.2f}")
        self.lbl_take.configure(text=f"{take_price:,.2f}")
        
        self.lbl_risk_usd.configure(text=f"${risk_usd:,.2f}")
        self.lbl_profit_usd.configure(text=f"${profit_usd:,.2f}")
        self.lbl_rr.configure(text=f"1:{self.rr_ratio}")


if __name__ == "__main__":
    app = TradingCalculator()
    app.mainloop()
