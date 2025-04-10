import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import serial
import serial.tools.list_ports
import time
import re
import os

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
        'start': "Indítás",
        'dock': "Dokkolás",
        'motor_currents': "Motoráramok",
        'mow_left_right': "Vágó/Bal/Jobb",
        'command_console': "Parancs Konzol",
        'send': "Küldés",
        'version': "Verzió",
        'status': "Állapot",
        'motor': "Motor",
        'test': "Teszt",
        'stop_cmd': "Stop",
        'start_cmd': "Indítás",
        'pause': "Szünet",
        'dock_cmd': "Dokkolás",
        'connection_error': "Nem sikerült csatlakozni: {}",
        'command_error': "Hiba a parancs küldésekor: {}",
        'sensor_error': "Hiba a szenzor adatok feldolgozásánál: {}",
        'light_mode': "Világos Mód",
        'dark_mode': "Sötét Mód",
        'pwm': "PWM",
        'current': "Áram",
        'rpm': "RPM",
        'file_list': "Fájl Lista",
        'download': "Letöltés",
        'upload': "Feltöltés",
        'save': "Mentés",
        'file_download': "Fájl Letöltése",
        'file_upload': "Fájl Feltöltése",
        'file_save': "Fájl Mentése",
        'enter_filename': "Add meg a fájl nevét:",
        'success': "Siker",
        'file_downloaded': "A {} fájl sikeresen letöltve!",
        'file_uploaded': "A {} fájl sikeresen feltöltve!",
        'error': "Hiba",
        'connect_first': "Először csatlakozz a készülékhez!",
        'file_list_error': "Nem sikerült listázni a fájlokat: {}",
        'file_download_error': "Nem sikerült letölteni a fájlt: {}",
        'file_upload_error': "Nem sikerült feltölteni a fájlt: {}",
        'warning': "Figyelmeztetés",
        'no_file_selected': "Nincs kiválasztott fájl!",
        'python_files': "Python fájlok",
        'files_on_pico': "Python fájlok a Pico-n:"
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
        'start': "Start",
        'dock': "Dock",
        'motor_currents': "Motor Currents",
        'mow_left_right': "Mow/Left/Right",
        'command_console': "Command Console",
        'send': "Send",
        'version': "Version",
        'status': "Status",
        'motor': "Motor",
        'test': "Test",
        'stop_cmd': "Stop",
        'start_cmd': "Start",
        'pause': "Pause",
        'dock_cmd': "Dock",
        'connection_error': "Failed to connect: {}",
        'command_error': "Error sending command: {}",
        'sensor_error': "Error processing sensor data: {}",
        'light_mode': "Light Mode",
        'dark_mode': "Dark Mode",
        'pwm': "PWM",
        'current': "Current",
        'rpm': "RPM",
        'file_list': "File List",
        'download': "Download",
        'upload': "Upload",
        'save': "Save",
        'file_download': "Download File",
        'file_upload': "Upload File",
        'file_save': "Save File",
        'enter_filename': "Enter filename:",
        'success': "Success",
        'file_downloaded': "File {} downloaded successfully!",
        'file_uploaded': "File {} uploaded successfully!",
        'error': "Error",
        'connect_first': "Please connect to the device first!",
        'file_list_error': "Failed to list files: {}",
        'file_download_error': "Failed to download file: {}",
        'file_upload_error': "Failed to upload file: {}",
        'warning': "Warning",
        'no_file_selected': "No file selected!",
        'python_files': "Python files",
        'files_on_pico': "Python files on Pico:"
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
        'start': "Start",
        'dock': "Andocken",
        'motor_currents': "Motorströme",
        'mow_left_right': "Mähen/Links/Rechts",
        'command_console': "Befehls Konsole",
        'send': "Senden",
        'version': "Version",
        'status': "Status",
        'motor': "Motor",
        'test': "Test",
        'stop_cmd': "Stop",
        'start_cmd': "Start",
        'pause': "Pause",
        'dock_cmd': "Andocken",
        'connection_error': "Verbindung fehlgeschlagen: {}",
        'command_error': "Fehler beim Senden des Befehls: {}",
        'sensor_error': "Fehler bei der Verarbeitung der Sensordaten: {}",
        'light_mode': "Hell Modus",
        'dark_mode': "Dunkel Modus",
        'pwm': "PWM",
        'current': "Strom",
        'rpm': "RPM",
        'file_list': "Dateiliste",
        'download': "Herunterladen",
        'upload': "Hochladen",
        'save': "Speichern",
        'file_download': "Datei Herunterladen",
        'file_upload': "Datei Hochladen",
        'file_save': "Datei Speichern",
        'enter_filename': "Dateinamen eingeben:",
        'success': "Erfolg",
        'file_downloaded': "Datei {} erfolgreich heruntergeladen!",
        'file_uploaded': "Datei {} erfolgreich hochgeladen!",
        'error': "Fehler",
        'connect_first': "Bitte zuerst mit dem Gerät verbinden!",
        'file_list_error': "Fehler beim Auflisten der Dateien: {}",
        'file_download_error': "Fehler beim Herunterladen der Datei: {}",
        'file_upload_error': "Fehler beim Hochladen der Datei: {}",
        'warning': "Warnung",
        'no_file_selected': "Keine Datei ausgewählt!",
        'python_files': "Python Dateien",
        'files_on_pico': "Python Dateien auf dem Pico:"
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
            'RAIN': tk.BooleanVar(value=False),
            'LIFT': tk.BooleanVar(value=False),
            'BUMP_X': tk.BooleanVar(value=False),
            'BUMP_Y': tk.BooleanVar(value=False),
            'STOP': tk.BooleanVar(value=False),
            'START': tk.BooleanVar(value=False),
            'DOCK': tk.BooleanVar(value=False),
            'MCURR': [tk.StringVar(value="0.0 A"), tk.StringVar(value="0.0 A"), tk.StringVar(value="0.0 A")]
        }
        
        # Parancs konzol változók
        self.command_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Windows 11 stílusok beállítása
        self.style.configure('TButton',
                           padding=5,
                           font=('Segoe UI Variable', 9))

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
        motor_frame.columnconfigure(1, weight=1)
        
        # Bal motor
        ttk.Label(motor_frame, text=self.translations['left_motor'], width=12).grid(row=0, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=-100, to=100, variable=self.left_motor_pwm, 
                 orient="horizontal", command=lambda x: self.left_motor_pwm.set(int(float(x)))).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.left_motor_pwm, width=4).grid(row=0, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['LEFT']['speed'], width=8).grid(row=0, column=3, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['LEFT']['current'], width=8).grid(row=0, column=4, padx=5)
        ttk.Label(motor_frame, text="A").grid(row=0, column=5, padx=(0,5))
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.left_motor_pwm.set(0)).grid(row=0, column=6, padx=5)
        
        # Jobb motor
        ttk.Label(motor_frame, text=self.translations['right_motor'], width=12).grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=-100, to=100, variable=self.right_motor_pwm,
                 orient="horizontal", command=lambda x: self.right_motor_pwm.set(int(float(x)))).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.right_motor_pwm, width=4).grid(row=1, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['RIGHT']['speed'], width=8).grid(row=1, column=3, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['RIGHT']['current'], width=8).grid(row=1, column=4, padx=5)
        ttk.Label(motor_frame, text="A").grid(row=1, column=5, padx=(0,5))
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.right_motor_pwm.set(0)).grid(row=1, column=6, padx=5)
        
        # Vágó motor
        ttk.Label(motor_frame, text=self.translations['mow_motor'], width=12).grid(row=2, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=0, to=100, variable=self.mow_motor_pwm,
                 orient="horizontal", command=lambda x: self.mow_motor_pwm.set(int(float(x)))).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(motor_frame, textvariable=self.mow_motor_pwm, width=4).grid(row=2, column=2, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['MOW']['speed'], width=8).grid(row=2, column=3, padx=5)
        ttk.Label(motor_frame, textvariable=self.motor_feedback['MOW']['current'], width=8).grid(row=2, column=4, padx=5)
        ttk.Label(motor_frame, text="A").grid(row=2, column=5, padx=(0,5))
        ttk.Button(motor_frame, text=self.translations['reset'],
                  command=lambda: self.mow_motor_pwm.set(0)).grid(row=2, column=6, padx=5)

        # Oszlop fejlécek
        ttk.Label(motor_frame, text=self.translations['pwm'], width=4).grid(row=3, column=2, padx=5, pady=(5,0))
        ttk.Label(motor_frame, text=self.translations['rpm'], width=8).grid(row=3, column=3, padx=5, pady=(5,0))
        ttk.Label(motor_frame, text=self.translations['current'], width=8).grid(row=3, column=4, padx=5, pady=(5,0))

        # Motor vezérlő gombok
        control_frame = ttk.Frame(motor_frame)
        control_frame.grid(row=4, column=0, columnspan=7, pady=10)
        
        ttk.Button(control_frame, text=self.translations['test_motors'], 
                  command=self.test_motors, width=20).pack(side="left", padx=5)
        ttk.Button(control_frame, text=self.translations['stop_motors'], 
                  command=self.stop_motors, width=20).pack(side="left", padx=5)
        ttk.Button(control_frame, text=self.translations['clear_errors'], 
                  command=lambda: self.send_command("AT+R"), width=20).pack(side="left", padx=5)

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
        self.lift_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.lift_led.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(middle_sensor_frame, text=self.translations['bumper'], width=8).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.bump_x_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.bump_y_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.bump_x_led.grid(row=2, column=1, padx=5, pady=5)
        self.bump_y_led.grid(row=2, column=2, padx=5, pady=5)
        
        ttk.Label(middle_sensor_frame, text=self.translations['stop'], width=8).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.stop_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.stop_led.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(middle_sensor_frame, text=self.translations['start'], width=8).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.start_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.start_led.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(middle_sensor_frame, text=self.translations['dock'], width=8).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.dock_led = LEDIndicator(middle_sensor_frame, size=led_size)
        self.dock_led.grid(row=5, column=1, padx=5, pady=5)

        # Parancs konzol
        console_frame = ttk.LabelFrame(self.root, text=self.translations['command_console'], padding=10)
        console_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Parancs gombok
        command_buttons_frame = ttk.Frame(console_frame)
        command_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Felső sor gombok
        top_buttons = ttk.Frame(command_buttons_frame)
        top_buttons.pack(fill="x", pady=(0,5))
        
        for text, cmd in [
            (f"{self.translations['version']} (AT+V)", "AT+V"),
            (f"{self.translations['status']} (AT+S)", "AT+S"),
            (f"{self.translations['motor']} (AT+M)", "AT+M"),
            (f"{self.translations['test']} (AT+E)", "AT+E"),
            (f"{self.translations['reset']} (AT+R)", "AT+R")
        ]:
            ttk.Button(top_buttons, text=text, command=lambda c=cmd: self.send_command(c), 
                      width=15).pack(side="left", padx=2)
        
        # Alsó sor gombok
        bottom_buttons = ttk.Frame(command_buttons_frame)
        bottom_buttons.pack(fill="x")
        
        for text, cmd in [
            (f"{self.translations['start_cmd']} (AT+Y1)", "AT+Y1"),
            (f"{self.translations['pause']} (AT+Y2)", "AT+Y2"),
            (f"{self.translations['stop_cmd']} (AT+Y3)", "AT+Y3"),
            (f"{self.translations['dock_cmd']} (AT+Y4)", "AT+Y4")
        ]:
            ttk.Button(bottom_buttons, text=text, command=lambda c=cmd: self.send_command(c), 
                      width=15).pack(side="left", padx=2)
        
        # Konzol kimenet
        self.console_text = tk.Text(console_frame, height=15, width=80, font=('Cascadia Code', 10))
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
        
        send_btn = ttk.Button(input_frame, text=self.translations['send'],
                             command=self.send_manual_command)
        send_btn.pack(side="right")

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
        
        # Keretek címkéinek frissítése
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                if widget.cget('text') in [LANGUAGES[lang]['serial_port'] for lang in LANGUAGES]:
                    widget.configure(text=self.translations['serial_port'])
                elif widget.cget('text') in [LANGUAGES[lang]['motor_control'] for lang in LANGUAGES]:
                    widget.configure(text=self.translations['motor_control'])
                elif widget.cget('text') in [LANGUAGES[lang]['sensor_status'] for lang in LANGUAGES]:
                    widget.configure(text=self.translations['sensor_status'])
                elif widget.cget('text') in [LANGUAGES[lang]['command_console'] for lang in LANGUAGES]:
                    widget.configure(text=self.translations['command_console'])
                
                # Gombok és címkék frissítése a keretben
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        # Beágyazott frame-ek kezelése
                        for subchild in child.winfo_children():
                            self._update_widget_text(subchild)
                    else:
                        self._update_widget_text(child)
        
        # Csatlakozás gomb frissítése
        if self.connected:
            self.connect_btn.configure(text=self.translations['disconnect'])
        else:
            self.connect_btn.configure(text=self.translations['connect'])

    def _update_widget_text(self, widget):
        """Egy widget szövegének frissítése"""
        if isinstance(widget, (ttk.Label, ttk.Button)):
            current_text = widget.cget('text')
            
            # Alap szövegek
            text_keys = [
                'refresh', 'connect', 'disconnect', 'left_motor', 'right_motor', 
                'mow_motor', 'reset', 'test_motors', 'stop_motors', 'clear_errors',
                'battery', 'charging', 'rain', 'lift', 'bumper', 'stop', 'start',
                'dock', 'motor_currents', 'mow_left_right', 'send', 'pwm', 'rpm',
                'current'
            ]
            
            # AT parancsok szövegei
            command_texts = {
                'version': 'AT+V',
                'status': 'AT+S',
                'motor': 'AT+M',
                'test': 'AT+E',
                'reset': 'AT+R',
                'start_cmd': 'AT+Y1',
                'pause': 'AT+Y2',
                'stop_cmd': 'AT+Y3',
                'dock_cmd': 'AT+Y4'
            }
            
            # Alap szövegek ellenőrzése
            for key in text_keys:
                if current_text in [LANGUAGES[lang][key] for lang in LANGUAGES]:
                    widget.configure(text=self.translations[key])
                    return
            
            # AT parancsok ellenőrzése
            for key, cmd in command_texts.items():
                if cmd in current_text:
                    widget.configure(text=f"{self.translations[key]} ({cmd})")
                    return

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
            
            # RAIN=1
            rain_match = re.search(r'RAIN=(\d+)', response)
            if rain_match:
                self.sensor_values['RAIN'].set(bool(int(rain_match.group(1))))
                self.rain_led.set_state(bool(int(rain_match.group(1))))
            
            # LIFT=1
            lift_match = re.search(r'LIFT=(\d+)', response)
            if lift_match:
                self.sensor_values['LIFT'].set(bool(int(lift_match.group(1))))
                self.lift_led.set_state(bool(int(lift_match.group(1))))
            
            # BUMP=0/1
            bump_match = re.search(r'BUMP=(\d+)/(\d+)', response)
            if bump_match:
                self.sensor_values['BUMP_X'].set(bool(int(bump_match.group(1))))
                self.sensor_values['BUMP_Y'].set(bool(int(bump_match.group(2))))
                self.bump_x_led.set_state(bool(int(bump_match.group(1))))
                self.bump_y_led.set_state(bool(int(bump_match.group(2))))
            
            # STOP=1
            stop_match = re.search(r'STOP=(\d+)', response)
            if stop_match:
                self.sensor_values['STOP'].set(bool(int(stop_match.group(1))))
                self.stop_led.set_state(bool(int(stop_match.group(1))))
            
            # START=1
            start_match = re.search(r'START=(\d+)', response)
            if start_match:
                self.sensor_values['START'].set(bool(int(start_match.group(1))))
                self.start_led.set_state(bool(int(start_match.group(1))))
            
            # DOCK=1
            dock_match = re.search(r'DOCK=(\d+)', response)
            if dock_match:
                self.sensor_values['DOCK'].set(bool(int(dock_match.group(1))))
                self.dock_led.set_state(bool(int(dock_match.group(1))))
            
            # MCURR=0.5/0.3/0.4
            mcurr_match = re.search(r'MCURR=([\d.]+)/([\d.]+)/([\d.]+)', response)
            if mcurr_match:
                self.sensor_values['MCURR'][0].set(f"{float(mcurr_match.group(1)):.1f} A")
                self.sensor_values['MCURR'][1].set(f"{float(mcurr_match.group(2)):.1f} A")
                self.sensor_values['MCURR'][2].set(f"{float(mcurr_match.group(3)):.1f} A")
                
            # Motor visszacsatolás feldolgozása
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

    def list_files(self):
        """Pico-n lévő fájlok listázása"""
        if not self.connected:
            messagebox.showerror(self.translations['error'], self.translations['connect_first'])
            return
            
        try:
            response = self.send_command("AT+LS")
            if response:
                self.console_text.insert(tk.END, self.translations['files_on_pico'] + "\n")
                self.console_text.insert(tk.END, response + "\n")
                self.console_text.see(tk.END)
        except Exception as e:
            messagebox.showerror(self.translations['error'], 
                               self.translations['file_list_error'].format(str(e)))
    
    def download_file(self):
        """Fájl letöltése a Pico-ról"""
        if not self.connected:
            messagebox.showerror(self.translations['error'], self.translations['connect_first'])
            return
            
        filename = simpledialog.askstring(self.translations['file_download'], 
                                        self.translations['enter_filename'])
        if filename:
            try:
                response = self.send_command(f"AT+GET,{filename}")
                if response:
                    save_path = filedialog.asksaveasfilename(
                        defaultextension=".py",
                        filetypes=[(self.translations['python_files'], "*.py")],
                        initialfile=filename
                    )
                    if save_path:
                        with open(save_path, 'w') as f:
                            f.write(response)
                        messagebox.showinfo(self.translations['success'], 
                                          self.translations['file_downloaded'].format(filename))
            except Exception as e:
                messagebox.showerror(self.translations['error'], 
                                   self.translations['file_download_error'].format(str(e)))
    
    def upload_file(self):
        """Fájl feltöltése a Pico-ra"""
        if not self.connected:
            messagebox.showerror(self.translations['error'], self.translations['connect_first'])
            return
            
        filename = filedialog.askopenfilename(
            filetypes=[(self.translations['python_files'], "*.py")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                basename = os.path.basename(filename)
                self.send_command(f"AT+PUT,{basename},{content}")
                messagebox.showinfo(self.translations['success'], 
                                  self.translations['file_uploaded'].format(basename))
            except Exception as e:
                messagebox.showerror(self.translations['error'], 
                                   self.translations['file_upload_error'].format(str(e)))

    def on_file_select(self, event):
        if not self.file_listbox.curselection():
            return
        selected_file = self.file_listbox.get(self.file_listbox.curselection())
        self.current_file = selected_file
        self.send_command(f"AT+GET,{selected_file}")
    
    def save_file(self):
        if not hasattr(self, 'current_file'):
            messagebox.showwarning(self.translations['warning'], 
                                 self.translations['no_file_selected'])
            return
        content = self.editor_text.get("1.0", "end-1c")
        self.send_command(f"AT+PUT,{self.current_file},{content}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControl(root)
    root.mainloop() 