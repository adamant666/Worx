import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time
import re

# Windows 11 színséma
THEMES = {
    'light': {
        'bg': '#ffffff',           # Fehér háttér
        'fg': '#202020',           # Sötét szöveg
        'frame_bg': '#fafafa',     # Világos keret
        'text_bg': '#ffffff',      # Fehér szövegmező
        'text_fg': '#202020',      # Sötét szöveg
        'button_bg': '#e9e9e9',    # Világosszürke gomb
        'button_fg': '#202020',    # Sötét gomb szöveg
        'button_active': '#0067c0', # Win11 kék hover
        'entry_bg': '#ffffff',     # Fehér beviteli mező
        'accent': '#0067c0',       # Win11 kék kiemelés
        'warning': '#c42b1c',      # Win11 piros
        'led_off': '#808080',      # Szürke LED kikapcsolva
        'led_on': '#107c10',       # Win11 zöld LED
        'scale_bg': '#dddddd',     # Világosszürke csúszka
        'border': '#e1e1e1'        # Világosszürke keret
    },
    'dark': {
        'bg': '#202020',           # Sötét háttér
        'fg': '#ffffff',           # Fehér szöveg
        'frame_bg': '#1f1f1f',     # Sötét keret
        'text_bg': '#1f1f1f',      # Sötét szövegmező
        'text_fg': '#ffffff',      # Fehér szöveg
        'button_bg': '#323232',    # Sötétszürke gomb
        'button_fg': '#ffffff',    # Fehér gomb szöveg
        'button_active': '#0067c0', # Win11 kék hover
        'entry_bg': '#2b2b2b',     # Sötét beviteli mező
        'accent': '#60cdff',       # Win11 világoskék
        'warning': '#ff99a4',      # Win11 világos piros
        'led_off': '#404040',      # Sötét szürke LED kikapcsolva
        'led_on': '#92c353',       # Win11 világos zöld LED
        'scale_bg': '#333333',     # Sötét csúszka
        'border': '#404040'        # Sötét keret
    }
}

# Nyelvi szótárak
LANGUAGES = {
    'magyar': {
        'title': "Landrumower Robot Vezérlő",
        'serial_port': "Soros Port",
        'refresh': "Frissítés",
        'connect': "Csatlakozás",
        'disconnect': "Lecsatlakozás",
        'motor_control': "Motor Vezérlés",
        'left_motor': "Bal Motor",
        'right_motor': "Jobb Motor",
        'mow_motor': "Vágó Motor",
        'reset': "Reset",
        'test_motors': "Motorok Tesztelése",
        'stop_motors': "Motorok Leállítása",
        'clear_errors': "Motor Hibák Törlése",
        'sensor_status': "Szenzor Állapot",
        'battery': "Akkumulátor",
        'charging': "Töltés",
        'rain': "Eső",
        'lift': "Emelés",
        'bumper': "Ütköző",
        'stop': "Stop",
        'motor_currents': "Motoráramok",
        'mow_left_right': "Vágó/Bal/Jobb",
        'command_console': "Parancs Konzol",
        'send': "Küldés",
        'version': "Verzió",
        'status': "Állapot",
        'motor': "Motor",
        'test': "Teszt",
        'stop_cmd': "Stop",
        'start': "Indítás",
        'pause': "Szünet",
        'connection_error': "Nem sikerült csatlakozni: {}",
        'command_error': "Hiba a parancs küldésekor: {}",
        'sensor_error': "Hiba a szenzor adatok feldolgozásánál: {}",
        'light_mode': "Világos Mód",
        'dark_mode': "Sötét Mód"
    },
    'english': {
        'title': "Landrumower Robot Controller",
        'serial_port': "Serial Port",
        'refresh': "Refresh",
        'connect': "Connect",
        'disconnect': "Disconnect",
        'motor_control': "Motor Control",
        'left_motor': "Left Motor",
        'right_motor': "Right Motor",
        'mow_motor': "Mow Motor",
        'reset': "Reset",
        'test_motors': "Test Motors",
        'stop_motors': "Stop Motors",
        'clear_errors': "Clear Motor Errors",
        'sensor_status': "Sensor Status",
        'battery': "Battery",
        'charging': "Charging",
        'rain': "Rain",
        'lift': "Lift",
        'bumper': "Bumper",
        'stop': "Stop",
        'motor_currents': "Motor Currents",
        'mow_left_right': "Mow/Left/Right",
        'command_console': "Command Console",
        'send': "Send",
        'version': "Version",
        'status': "Status",
        'motor': "Motor",
        'test': "Test",
        'stop_cmd': "Stop",
        'start': "Start",
        'pause': "Pause",
        'connection_error': "Failed to connect: {}",
        'command_error': "Error sending command: {}",
        'sensor_error': "Error processing sensor data: {}",
        'light_mode': "Light Mode",
        'dark_mode': "Dark Mode"
    },
    'deutsch': {
        'title': "Landrumower Roboter Steuerung",
        'serial_port': "Serieller Port",
        'refresh': "Aktualisieren",
        'connect': "Verbinden",
        'disconnect': "Trennen",
        'motor_control': "Motorsteuerung",
        'left_motor': "Linker Motor",
        'right_motor': "Rechter Motor",
        'mow_motor': "Mähmotor",
        'reset': "Zurücksetzen",
        'test_motors': "Motoren Testen",
        'stop_motors': "Motoren Stoppen",
        'clear_errors': "Motorfehler Löschen",
        'sensor_status': "Sensorstatus",
        'battery': "Batterie",
        'charging': "Laden",
        'rain': "Regen",
        'lift': "Anheben",
        'bumper': "Stoßstange",
        'stop': "Stop",
        'motor_currents': "Motorströme",
        'mow_left_right': "Mähen/Links/Rechts",
        'command_console': "Befehls Konsole",
        'send': "Senden",
        'version': "Version",
        'status': "Status",
        'motor': "Motor",
        'test': "Test",
        'stop_cmd': "Stop",
        'start': "Start",
        'pause': "Pause",
        'connection_error': "Verbindung fehlgeschlagen: {}",
        'command_error': "Fehler beim Senden des Befehls: {}",
        'sensor_error': "Fehler bei der Verarbeitung der Sensordaten: {}",
        'light_mode': "Hell Modus",
        'dark_mode': "Dunkel Modus"
    }
}

class LEDIndicator(tk.Canvas):
    def __init__(self, parent, size=20, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.size = size
        self.led = self.create_oval(2, 2, size-2, size-2, fill='gray')
        
    def set_state(self, state):
        theme = THEMES['light' if self.master.master.master.is_light_mode else 'dark']
        color = theme['led_on'] if state else theme['led_off']
        self.itemconfig(self.led, fill=color)

class RobotControl:
    def __init__(self, root):
        self.root = root
        self.current_language = 'magyar'
        self.translations = LANGUAGES[self.current_language]
        self.is_light_mode = True
        
        self.root.title(self.translations['title'])
        self.root.geometry("800x900")
        
        # Minimum méret beállítása
        self.root.minsize(800, 900)
        
        # Style beállítása
        self.style = ttk.Style()
        self.apply_theme()
        
        self.serial_port = None
        self.connected = False
        
        # Változók a motorokhoz (-100 - 100 között)
        self.left_motor_pwm = tk.IntVar(value=0)
        self.right_motor_pwm = tk.IntVar(value=0)
        self.mow_motor_pwm = tk.IntVar(value=0)
        
        # Motor visszacsatolás változók
        self.motor_feedback = {
            'LEFT': {'speed': tk.StringVar(value="0 RPM"), 'current': tk.StringVar(value="0.0 A")},
            'RIGHT': {'speed': tk.StringVar(value="0 RPM"), 'current': tk.StringVar(value="0.0 A")},
            'MOW': {'speed': tk.StringVar(value="0 RPM"), 'current': tk.StringVar(value="0.0 A")}
        }
        
        # Szenzor változók
        self.sensor_values = {
            'BAT': tk.StringVar(value="0.0V"),
            'CHG': tk.StringVar(value="0.0V/0.0A"),
            'RAIN': [tk.BooleanVar(value=False), tk.BooleanVar(value=False)],
            'LIFT': [tk.BooleanVar(value=False), tk.BooleanVar(value=False)],
            'BUMP': [tk.BooleanVar(value=False), tk.BooleanVar(value=False)],
            'STOP': tk.BooleanVar(value=False),
            'MCURR': [tk.StringVar(value="0.0 A"), tk.StringVar(value="0.0 A"), tk.StringVar(value="0.0 A")]
        }
        
        # Parancs konzol változók
        self.command_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Windows 11 stílus beállítása
        self.style.configure('TButton',
                           padding=(10, 5),
                           relief="flat",
                           background=THEMES['light' if self.is_light_mode else 'dark']['button_bg'],
                           foreground=THEMES['light' if self.is_light_mode else 'dark']['button_fg'],
                           font=('Segoe UI Variable', 10))
        
        self.style.map('TButton',
                      background=[('active', THEMES['light' if self.is_light_mode else 'dark']['button_active']),
                                ('pressed', THEMES['light' if self.is_light_mode else 'dark']['button_active'])],
                      foreground=[('active', '#ffffff'),
                                ('pressed', '#ffffff')])
        
        # Keret stílusok
        self.style.configure('TFrame',
                           background=THEMES['light' if self.is_light_mode else 'dark']['bg'])
        
        self.style.configure('TLabelframe',
                           background=THEMES['light' if self.is_light_mode else 'dark']['frame_bg'],
                           relief="solid",
                           borderwidth=1,
                           bordercolor=THEMES['light' if self.is_light_mode else 'dark']['border'])
        
        self.style.configure('TLabelframe.Label',
                           background=THEMES['light' if self.is_light_mode else 'dark']['frame_bg'],
                           foreground=THEMES['light' if self.is_light_mode else 'dark']['fg'],
                           font=('Segoe UI Variable', 11, 'bold'))
        
        # Címke stílus
        self.style.configure('TLabel',
                           background=THEMES['light' if self.is_light_mode else 'dark']['bg'],
                           foreground=THEMES['light' if self.is_light_mode else 'dark']['fg'],
                           font=('Segoe UI Variable', 10))

        # Csúszka stílus
        self.style.layout('Horizontal.TScale',
                     [('Horizontal.Scale.trough',
                       {'sticky': 'nswe',
                        'children': [('Horizontal.Scale.slider',
                                    {'side': 'left', 'sticky': ''})]})])
        
        self.style.configure('Horizontal.TScale',
                           background=THEMES['light' if self.is_light_mode else 'dark']['bg'],
                           troughcolor=THEMES['light' if self.is_light_mode else 'dark']['scale_bg'],
                           borderwidth=0,
                           relief="flat")

        # Entry stílus
        self.style.configure('TEntry',
                           padding=5,
                           fieldbackground=THEMES['light' if self.is_light_mode else 'dark']['entry_bg'],
                           foreground=THEMES['light' if self.is_light_mode else 'dark']['fg'],
                           insertcolor=THEMES['light' if self.is_light_mode else 'dark']['fg'])

        # Radiobutton stílus
        self.style.configure('TRadiobutton',
                           background=THEMES['light' if self.is_light_mode else 'dark']['bg'],
                           foreground=THEMES['light' if self.is_light_mode else 'dark']['fg'],
                           font=('Segoe UI Variable', 10))

        # Combobox stílus
        self.style.configure('TCombobox',
                           padding=5,
                           selectbackground=THEMES['light' if self.is_light_mode else 'dark']['accent'],
                           selectforeground='#ffffff',
                           fieldbackground=THEMES['light' if self.is_light_mode else 'dark']['entry_bg'],
                           background=THEMES['light' if self.is_light_mode else 'dark']['button_bg'])

        # Nyelv választó
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill="x", padx=15, pady=5)
        
        ttk.Label(lang_frame, text="Nyelv/Language/Sprache:").pack(side="left", padx=5)
        
        self.lang_var = tk.StringVar(value=self.current_language)
        for lang in LANGUAGES.keys():
            ttk.Radiobutton(lang_frame, text=lang.capitalize(), 
                          value=lang, variable=self.lang_var,
                          command=lambda l=lang: self.change_language(l)).pack(side="left", padx=5)
        
        # Soros port választó
        port_frame = ttk.LabelFrame(self.root, text=self.translations['serial_port'], padding=10)
        port_frame.pack(fill="x", padx=15, pady=5)
        
        self.port_combo = ttk.Combobox(port_frame, width=30)
        self.port_combo.pack(side="left", padx=5)
        
        ttk.Button(port_frame, text=self.translations['refresh'], 
                  command=self.refresh_ports).pack(side="left", padx=5)
        self.connect_btn = ttk.Button(port_frame, text=self.translations['connect'], 
                                    command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        # Motor vezérlő
        motor_frame = ttk.LabelFrame(self.root, text=self.translations['motor_control'], padding=10)
        motor_frame.pack(fill="x", padx=15, pady=5)
        
        # Grid konfiguráció a motor vezérlőkhöz
        motor_frame.columnconfigure(1, weight=1)  # A csúszka oszlopa táguljon
        
        # Bal motor
        ttk.Label(motor_frame, text=self.translations['left_motor'], width=12).grid(row=0, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=-100, to=100, variable=self.left_motor_pwm, 
                 orient="horizontal", command=lambda x: self.left_motor_pwm.set(int(float(x)))).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.left_motor_pwm, width=4).grid(row=0, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['LEFT']['speed'], width=10).grid(row=0, column=3, padx=5)
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.left_motor_pwm.set(0)).grid(row=0, column=4, padx=5)
        
        # Jobb motor
        ttk.Label(motor_frame, text=self.translations['right_motor'], width=12).grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=-100, to=100, variable=self.right_motor_pwm,
                 orient="horizontal", command=lambda x: self.right_motor_pwm.set(int(float(x)))).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.right_motor_pwm, width=4).grid(row=1, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['RIGHT']['speed'], width=10).grid(row=1, column=3, padx=5)
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.right_motor_pwm.set(0)).grid(row=1, column=4, padx=5)
        
        # Vágó motor
        ttk.Label(motor_frame, text=self.translations['mow_motor'], width=12).grid(row=2, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=0, to=100, variable=self.mow_motor_pwm,
                 orient="horizontal", command=lambda x: self.mow_motor_pwm.set(int(float(x)))).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.mow_motor_pwm, width=4).grid(row=2, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['MOW']['speed'], width=10).grid(row=2, column=3, padx=5)
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.mow_motor_pwm.set(0)).grid(row=2, column=4, padx=5)

        # Motor vezérlő gombok
        control_frame = ttk.Frame(motor_frame)
        control_frame.grid(row=3, column=0, columnspan=5, pady=10)
        
        ttk.Button(control_frame, text=self.translations['test_motors'], command=self.test_motors).pack(side="left", padx=5)
        ttk.Button(control_frame, text=self.translations['stop_motors'], command=self.stop_motors).pack(side="left", padx=5)
        ttk.Button(control_frame, text=self.translations['clear_errors'], command=lambda: self.send_command("AT+R")).pack(side="left", padx=5)

        # Szenzor állapot
        sensor_frame = ttk.LabelFrame(self.root, text=self.translations['sensor_status'], padding=10)
        sensor_frame.pack(fill="x", padx=15, pady=5)
        
        # Szenzor panel konténer
        sensor_container = ttk.Frame(sensor_frame)
        sensor_container.pack(fill="x", expand=True)
        
        # Bal oldali szenzor panel
        left_sensor_frame = ttk.Frame(sensor_container)
        left_sensor_frame.pack(side="left", padx=15)
        
        # Akkumulátor és töltés
        ttk.Label(left_sensor_frame, text=self.translations['battery'], width=12).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(left_sensor_frame, textvariable=self.sensor_values['BAT'], width=8).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(left_sensor_frame, text=self.translations['charging'], width=12).grid(row=1, column=0, padx=5, pady=2, sticky="e")
        ttk.Label(left_sensor_frame, textvariable=self.sensor_values['CHG'], width=12).grid(row=1, column=1, padx=5, pady=2)
        
        # Középső szenzor panel
        middle_sensor_frame = ttk.Frame(sensor_container)
        middle_sensor_frame.pack(side="left", padx=20, expand=True)
        
        # LED-ek méretének növelése
        led_size = 25
        
        # Eső, Emelés, Ütköző, Stop
        ttk.Label(middle_sensor_frame, text=self.translations['rain'], width=8).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.rain_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.rain_led.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(middle_sensor_frame, text=self.translations['lift'], width=8).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.lift_left_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.lift_right_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.lift_left_led.grid(row=1, column=1, padx=5, pady=5)
        self.lift_right_led.grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(middle_sensor_frame, text=self.translations['bumper'], width=8).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.bump_x_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.bump_y_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.bump_x_led.grid(row=2, column=1, padx=5, pady=5)
        self.bump_y_led.grid(row=2, column=2, padx=5, pady=5)
        
        ttk.Label(middle_sensor_frame, text=self.translations['stop'], width=8).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.stop_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.stop_led.grid(row=3, column=1, padx=5, pady=5)
        
        # Jobb oldali szenzor panel
        right_sensor_frame = ttk.Frame(sensor_container)
        right_sensor_frame.pack(side="right", padx=15)
        
        ttk.Label(right_sensor_frame, text=self.translations['motor_currents'], font=('Segoe UI Variable', 10, 'bold')).grid(row=0, column=0, columnspan=3, padx=5, pady=2)
        ttk.Label(right_sensor_frame, text=self.translations['mow_left_right']).grid(row=1, column=0, columnspan=3, padx=5, pady=2)
        ttk.Label(right_sensor_frame, textvariable=self.sensor_values['MCURR'][0], width=8).grid(row=2, column=0, padx=5, pady=2)
        ttk.Label(right_sensor_frame, textvariable=self.sensor_values['MCURR'][1], width=8).grid(row=2, column=1, padx=5, pady=2)
        ttk.Label(right_sensor_frame, textvariable=self.sensor_values['MCURR'][2], width=8).grid(row=2, column=2, padx=5, pady=2)

        # Parancs konzol
        console_frame = ttk.LabelFrame(self.root, text=self.translations['command_console'], padding=10)
        console_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Parancs gombok két sorban
        command_buttons_frame = ttk.Frame(console_frame)
        command_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Felső sor gombok
        top_buttons_frame = ttk.Frame(command_buttons_frame)
        top_buttons_frame.pack(fill="x", pady=(0, 5))
        
        button_commands_top = [
            ("Verzió (AT+V)", "AT+V"),
            ("Állapot (AT+S)", "AT+S"),
            ("Motor (AT+M)", "AT+M"),
            ("Teszt (AT+E)", "AT+E"),
            ("Reset (AT+R)", "AT+R")
        ]
        
        for text, cmd in button_commands_top:
            ttk.Button(top_buttons_frame, text=text, command=lambda c=cmd: self.send_command(c), width=15).pack(side="left", padx=2)
        
        # Alsó sor gombok
        bottom_buttons_frame = ttk.Frame(command_buttons_frame)
        bottom_buttons_frame.pack(fill="x")
        
        button_commands_bottom = [
            ("Indítás (AT+Y1)", "AT+Y1"),
            ("Szünet (AT+Y2)", "AT+Y2"),
            ("Stop (AT+Y3)", "AT+Y3")
        ]
        
        for text, cmd in button_commands_bottom:
            ttk.Button(bottom_buttons_frame, text=text, command=lambda c=cmd: self.send_command(c), width=15).pack(side="left", padx=2)
        
        # Konzol kimenet nagyobb mérettel
        self.console_text = tk.Text(console_frame, height=40, width=80, font=('Consolas', 10))
        self.console_text.pack(fill="both", expand=True, pady=5)
        
        # Scrollbar a konzolhoz
        scrollbar = ttk.Scrollbar(self.console_text)
        scrollbar.pack(side="right", fill="y")
        self.console_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.console_text.yview)
        
        # Parancs bevitel
        input_frame = ttk.Frame(console_frame)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        self.command_entry = ttk.Entry(input_frame, textvariable=self.command_var)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.command_entry.bind('<Return>', self.send_manual_command)
        
        send_btn = ttk.Button(input_frame, text=self.translations['send'], width=15,
                            command=self.send_manual_command)
        send_btn.pack(side="right")
        
        # Modern konzol stílus
        self.console_text.configure(
            font=('Cascadia Code', 10),
            relief="solid",
            borderwidth=1,
            selectbackground=THEMES['light' if self.is_light_mode else 'dark']['accent']
        )

        # Kezdeti portok frissítése
        self.refresh_ports()
        
    def change_language(self, lang):
        """Nyelv váltása"""
        self.current_language = lang
        self.translations = LANGUAGES[lang]
        self.root.title(self.translations['title'])
        self.refresh_widgets()
        
    def refresh_widgets(self):
        """Widget-ek frissítése az új nyelv szerint"""
        # Ablak cím frissítése
        self.root.title(self.translations['title'])
        
        # Soros port címke frissítése
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                if widget.winfo_children():
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Button):
                            if child.cget('text') == LANGUAGES['magyar']['refresh'] or \
                               child.cget('text') == LANGUAGES['english']['refresh'] or \
                               child.cget('text') == LANGUAGES['deutsch']['refresh']:
                                child.configure(text=self.translations['refresh'])
                            elif child.cget('text') == LANGUAGES['magyar']['connect'] or \
                                 child.cget('text') == LANGUAGES['english']['connect'] or \
                                 child.cget('text') == LANGUAGES['deutsch']['connect']:
                                child.configure(text=self.translations['connect'])
                            elif child.cget('text') == LANGUAGES['magyar']['disconnect'] or \
                                 child.cget('text') == LANGUAGES['english']['disconnect'] or \
                                 child.cget('text') == LANGUAGES['deutsch']['disconnect']:
                                child.configure(text=self.translations['disconnect'])
                
                # Keret címkék frissítése
                if widget.cget('text') == LANGUAGES['magyar']['serial_port'] or \
                   widget.cget('text') == LANGUAGES['english']['serial_port'] or \
                   widget.cget('text') == LANGUAGES['deutsch']['serial_port']:
                    widget.configure(text=self.translations['serial_port'])
                elif widget.cget('text') == LANGUAGES['magyar']['motor_control'] or \
                     widget.cget('text') == LANGUAGES['english']['motor_control'] or \
                     widget.cget('text') == LANGUAGES['deutsch']['motor_control']:
                    widget.configure(text=self.translations['motor_control'])
                elif widget.cget('text') == LANGUAGES['magyar']['sensor_status'] or \
                     widget.cget('text') == LANGUAGES['english']['sensor_status'] or \
                     widget.cget('text') == LANGUAGES['deutsch']['sensor_status']:
                    widget.configure(text=self.translations['sensor_status'])
                elif widget.cget('text') == LANGUAGES['magyar']['command_console'] or \
                     widget.cget('text') == LANGUAGES['english']['command_console'] or \
                     widget.cget('text') == LANGUAGES['deutsch']['command_console']:
                    widget.configure(text=self.translations['command_console'])
                
                # Motor címkék és gombok frissítése
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        if child.cget('text') == LANGUAGES['magyar']['left_motor'] or \
                           child.cget('text') == LANGUAGES['english']['left_motor'] or \
                           child.cget('text') == LANGUAGES['deutsch']['left_motor']:
                            child.configure(text=self.translations['left_motor'])
                        elif child.cget('text') == LANGUAGES['magyar']['right_motor'] or \
                             child.cget('text') == LANGUAGES['english']['right_motor'] or \
                             child.cget('text') == LANGUAGES['deutsch']['right_motor']:
                            child.configure(text=self.translations['right_motor'])
                        elif child.cget('text') == LANGUAGES['magyar']['mow_motor'] or \
                             child.cget('text') == LANGUAGES['english']['mow_motor'] or \
                             child.cget('text') == LANGUAGES['deutsch']['mow_motor']:
                            child.configure(text=self.translations['mow_motor'])
                        elif child.cget('text') == LANGUAGES['magyar']['battery'] or \
                             child.cget('text') == LANGUAGES['english']['battery'] or \
                             child.cget('text') == LANGUAGES['deutsch']['battery']:
                            child.configure(text=self.translations['battery'])
                        elif child.cget('text') == LANGUAGES['magyar']['charging'] or \
                             child.cget('text') == LANGUAGES['english']['charging'] or \
                             child.cget('text') == LANGUAGES['deutsch']['charging']:
                            child.configure(text=self.translations['charging'])
                        elif child.cget('text') == LANGUAGES['magyar']['rain'] or \
                             child.cget('text') == LANGUAGES['english']['rain'] or \
                             child.cget('text') == LANGUAGES['deutsch']['rain']:
                            child.configure(text=self.translations['rain'])
                        elif child.cget('text') == LANGUAGES['magyar']['lift'] or \
                             child.cget('text') == LANGUAGES['english']['lift'] or \
                             child.cget('text') == LANGUAGES['deutsch']['lift']:
                            child.configure(text=self.translations['lift'])
                        elif child.cget('text') == LANGUAGES['magyar']['bumper'] or \
                             child.cget('text') == LANGUAGES['english']['bumper'] or \
                             child.cget('text') == LANGUAGES['deutsch']['bumper']:
                            child.configure(text=self.translations['bumper'])
                        elif child.cget('text') == LANGUAGES['magyar']['stop'] or \
                             child.cget('text') == LANGUAGES['english']['stop'] or \
                             child.cget('text') == LANGUAGES['deutsch']['stop']:
                            child.configure(text=self.translations['stop'])
                        elif child.cget('text') == LANGUAGES['magyar']['motor_currents'] or \
                             child.cget('text') == LANGUAGES['english']['motor_currents'] or \
                             child.cget('text') == LANGUAGES['deutsch']['motor_currents']:
                            child.configure(text=self.translations['motor_currents'])
                        elif child.cget('text') == LANGUAGES['magyar']['mow_left_right'] or \
                             child.cget('text') == LANGUAGES['english']['mow_left_right'] or \
                             child.cget('text') == LANGUAGES['deutsch']['mow_left_right']:
                            child.configure(text=self.translations['mow_left_right'])
                    
                    elif isinstance(child, ttk.Button):
                        if child.cget('text') == LANGUAGES['magyar']['reset'] or \
                           child.cget('text') == LANGUAGES['english']['reset'] or \
                           child.cget('text') == LANGUAGES['deutsch']['reset']:
                            child.configure(text=self.translations['reset'])
                        elif child.cget('text') == LANGUAGES['magyar']['test_motors'] or \
                             child.cget('text') == LANGUAGES['english']['test_motors'] or \
                             child.cget('text') == LANGUAGES['deutsch']['test_motors']:
                            child.configure(text=self.translations['test_motors'])
                        elif child.cget('text') == LANGUAGES['magyar']['stop_motors'] or \
                             child.cget('text') == LANGUAGES['english']['stop_motors'] or \
                             child.cget('text') == LANGUAGES['deutsch']['stop_motors']:
                            child.configure(text=self.translations['stop_motors'])
                        elif child.cget('text') == LANGUAGES['magyar']['clear_errors'] or \
                             child.cget('text') == LANGUAGES['english']['clear_errors'] or \
                             child.cget('text') == LANGUAGES['deutsch']['clear_errors']:
                            child.configure(text=self.translations['clear_errors'])
                        elif child.cget('text') == LANGUAGES['magyar']['send'] or \
                             child.cget('text') == LANGUAGES['english']['send'] or \
                             child.cget('text') == LANGUAGES['deutsch']['send']:
                            child.configure(text=self.translations['send'])
                        elif "AT+V" in child.cget('text'):
                            child.configure(text=f"{self.translations['version']} (AT+V)")
                        elif "AT+S" in child.cget('text'):
                            child.configure(text=f"{self.translations['status']} (AT+S)")
                        elif "AT+M" in child.cget('text'):
                            child.configure(text=f"{self.translations['motor']} (AT+M)")
                        elif "AT+E" in child.cget('text'):
                            child.configure(text=f"{self.translations['test']} (AT+E)")
                        elif "AT+R" in child.cget('text'):
                            child.configure(text=f"{self.translations['reset']} (AT+R)")
                        elif "AT+Y3" in child.cget('text'):
                            child.configure(text=f"{self.translations['stop_cmd']} (AT+Y3)")
        
        # Csatlakozás gomb frissítése
        if self.connected:
            self.connect_btn.configure(text=self.translations['disconnect'])
        else:
            self.connect_btn.configure(text=self.translations['connect'])
        
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
            
    def toggle_connection(self):
        if not self.connected:
            try:
                port = self.port_combo.get()
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.connected = True
                self.port_combo.configure(state="disabled")
                self.root.title(f"Landrumower Robot Vezérlő - {port}")
            except Exception as e:
                tk.messagebox.showerror("Hiba", f"Nem sikerült csatlakozni: {str(e)}")
        else:
            if self.serial_port:
                self.serial_port.close()
            self.connected = False
            self.port_combo.configure(state="readonly")
            self.root.title("Landrumower Robot Vezérlő")
            
    def send_command(self, command):
        if not self.connected:
            return None
            
        try:
            # CRC számítás
            crc = sum(command.encode('ascii')) % 256
            full_command = f"{command},{hex(crc)}\r\n"
            
            # Parancs kiírása a konzolba
            self.console_text.insert(tk.END, f"-> {command}\n")
            
            self.serial_port.write(full_command.encode())
            response = self.serial_port.readline().decode().strip()
            
            # Válasz kiírása a konzolba
            if response:
                self.console_text.insert(tk.END, f"<- {response}\n")
            
            # Görgetés az aljára
            self.console_text.see(tk.END)
            
            return response
        except Exception as e:
            error_msg = f"Hiba a parancs küldésekor: {str(e)}"
            self.console_text.insert(tk.END, f"!! {error_msg}\n")
            self.console_text.see(tk.END)
            print(error_msg)
            return None
            
    def scale_pwm(self, value, is_mow=False):
        """Átskálázza a -100 - 100 közötti értéket -65535 - 65535 közé"""
        if is_mow:
            return int((value * 65535) / 100)
        else:
            return int((value * 65535) / 100)
            
    def test_motors(self):
        if not self.connected:
            return
            
        # Bal motor teszt
        left_pwm = self.scale_pwm(self.left_motor_pwm.get())
        self.send_command(f"AT+T,MOTOR,L,{left_pwm}")
        time.sleep(0.1)
        
        # Jobb motor teszt
        right_pwm = self.scale_pwm(self.right_motor_pwm.get())
        self.send_command(f"AT+T,MOTOR,R,{right_pwm}")
        time.sleep(0.1)
        
        # Vágó motor teszt
        mow_pwm = self.scale_pwm(self.mow_motor_pwm.get(), is_mow=True)
        self.send_command(f"AT+T,MOTOR,M,{mow_pwm}")
        
    def stop_motors(self):
        if self.connected:
            self.send_command("AT+T,STOP")
            
    def parse_sensor_response(self, response):
        try:
            # BAT=12.3V
            bat_match = re.search(r'BAT=([\d.]+)V', response)
            if bat_match:
                self.sensor_values['BAT'].set(f"{float(bat_match.group(1)):.1f}V")
            
            # CHG=14.2V/1.5A
            chg_match = re.search(r'CHG=([\d.]+)V/([\d.]+)A', response)
            if chg_match:
                self.sensor_values['CHG'].set(f"{float(chg_match.group(1)):.1f}V/{float(chg_match.group(2)):.1f}A")
            
            # RAIN=0/1
            rain_match = re.search(r'RAIN=(\d+)/(\d+)', response)
            if rain_match:
                self.sensor_values['RAIN'][0].set(bool(int(rain_match.group(1))))
                self.sensor_values['RAIN'][1].set(bool(int(rain_match.group(2))))
                self.rain_led.set_state(bool(int(rain_match.group(2))))
            
            # LIFT=0/1
            lift_match = re.search(r'LIFT=(\d+)/(\d+)', response)
            if lift_match:
                self.sensor_values['LIFT'][0].set(bool(int(lift_match.group(1))))
                self.sensor_values['LIFT'][1].set(bool(int(lift_match.group(2))))
                self.lift_left_led.set_state(bool(int(lift_match.group(1))))
                self.lift_right_led.set_state(bool(int(lift_match.group(2))))
            
            # BUMP=0/1
            bump_match = re.search(r'BUMP=(\d+)/(\d+)', response)
            if bump_match:
                self.sensor_values['BUMP'][0].set(bool(int(bump_match.group(1))))
                self.sensor_values['BUMP'][1].set(bool(int(bump_match.group(2))))
                self.bump_x_led.set_state(bool(int(bump_match.group(1))))
                self.bump_y_led.set_state(bool(int(bump_match.group(2))))
            
            # STOP=0/1
            stop_match = re.search(r'STOP=(\d+)', response)
            if stop_match:
                self.sensor_values['STOP'].set(bool(int(stop_match.group(1))))
                self.stop_led.set_state(bool(int(stop_match.group(1))))
            
            # MCURR=0.5/0.3/0.4
            mcurr_match = re.search(r'MCURR=([\d.]+)/([\d.]+)/([\d.]+)', response)
            if mcurr_match:
                self.sensor_values['MCURR'][0].set(f"{float(mcurr_match.group(1)):.1f} A")
                self.sensor_values['MCURR'][1].set(f"{float(mcurr_match.group(2)):.1f} A")
                self.sensor_values['MCURR'][2].set(f"{float(mcurr_match.group(3)):.1f} A")
                
            # Motor visszacsatolás feldolgozása
            # Példa válasz: SPEED=1234/2345/3456,CURRENT=1.2/2.3/3.4
            speed_match = re.search(r'SPEED=([\d-]+)/([\d-]+)/([\d-]+)', response)
            if speed_match:
                self.motor_feedback['LEFT']['speed'].set(f"{speed_match.group(1)} RPM")
                self.motor_feedback['RIGHT']['speed'].set(f"{speed_match.group(2)} RPM")
                self.motor_feedback['MOW']['speed'].set(f"{speed_match.group(3)} RPM")
            
            current_match = re.search(r'CURRENT=([\d.]+)/([\d.]+)/([\d.]+)', response)
            if current_match:
                self.motor_feedback['LEFT']['current'].set(f"{float(current_match.group(1)):.1f} A")
                self.motor_feedback['RIGHT']['current'].set(f"{float(current_match.group(2)):.1f} A")
                self.motor_feedback['MOW']['current'].set(f"{float(current_match.group(3)):.1f} A")
                
        except Exception as e:
            print(f"Hiba a szenzor adatok feldolgozásánál: {str(e)}")
            
    def query_sensors(self):
        if self.connected:
            # Állapot lekérdezése
            response = self.send_command("AT+S")
            if response:
                self.parse_sensor_response(response)
                
    def refresh_sensors(self):
        self.query_sensors()
        if self.connected:
            self.root.after(1000, self.refresh_sensors)

    def send_manual_command(self, event=None):
        if not self.connected:
            return
        
        command = self.command_var.get().strip()
        if command:
            self.send_command(command)
            self.command_var.set("")  # Beviteli mező törlése

    def quick_command(self, command):
        """Gyorsbillentyű parancs küldése"""
        if self.connected:
            self.send_command(command)
            return "break"  # Megakadályozza az eredeti billentyű eseményt

    def apply_theme(self):
        """Modern téma alkalmazása"""
        theme = THEMES['light' if self.is_light_mode else 'dark']
        
        # Modern stílusok frissítése
        self.style.configure('TButton',
                           background=theme['button_bg'],
                           foreground=theme['button_fg'],
                           font=('Segoe UI Variable', 10))
        
        self.style.map('TButton',
                      background=[('active', theme['button_active']),
                                ('pressed', theme['button_active'])],
                      foreground=[('active', '#ffffff'),
                                ('pressed', '#ffffff')])
        
        self.style.configure('TFrame',
                           background=theme['bg'])
        
        self.style.configure('TLabelframe',
                           background=theme['frame_bg'])
        
        self.style.configure('TLabelframe.Label',
                           background=theme['frame_bg'],
                           foreground=theme['fg'])
        
        self.style.configure('TLabel',
                           background=theme['bg'],
                           foreground=theme['fg'])
        
        # Modern csúszka stílus frissítése
        self.style.configure('Horizontal.TScale',
                           background=theme['bg'],
                           troughcolor=theme['scale_bg'])
        
        # Alap színek beállítása
        self.root.configure(bg=theme['bg'])
        
        # Konzol színek beállítása
        if hasattr(self, 'console_text'):
            self.console_text.configure(
                bg=theme['text_bg'],
                fg=theme['text_fg'],
                insertbackground=theme['fg'],
                selectbackground=theme['accent']
            )
        
        # Beviteli mező színek
        if hasattr(self, 'command_entry'):
            self.style.configure('TEntry',
                               fieldbackground=theme['entry_bg'],
                               foreground=theme['fg'])
            self.command_entry.configure(style='TEntry')
        
        # Téma gomb szövegének frissítése
        if hasattr(self, 'theme_btn'):
            self.theme_btn.configure(
                text=self.translations['light_mode' if not self.is_light_mode else 'dark_mode']
            )

    def toggle_theme(self):
        """Téma váltása"""
        self.is_light_mode = not self.is_light_mode
        self.apply_theme()

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControl(root)
    root.mainloop() 