#!/usr/bin/env python3
"""
🌙 MOONLIGHT - Monitor de Sistema COMPLETO
Versión: 3.0 - Interfaz gráfica completa
"""
import tkinter as tk
from tkinter import ttk, font
import psutil
import time
import threading
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess

class Moonlight:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌙 Moonlight Monitor")
        self.root.geometry("850x650")
        
        # Configurar para cerrar con ESC
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Variables
        self.running = True
        self.update_interval = 2000  # 2 segundos en milisegundos
        
        # Nuestro proceso
        self.process = psutil.Process()
        
        # Configuración
        self.config_dir = Path.home() / '.config' / 'moonlight'
        self.config_file = self.config_dir / 'settings.json'
        self.config = self.load_config()
        
        # Detectar GPU
        self.has_gpu = self.detect_gpu()
        
        # Historial
        self.cpu_history = []
        self.ram_history = []
        self.history_max = 30
        
        # Estilos
        self.setup_styles()
        
        # Construir interfaz
        self.build_ui()
        
        # Iniciar actualización
        self.update_data()
        
    def setup_styles(self):
        """Configura los estilos visuales"""
        self.colors = {
            'bg': '#0f0f23',
            'card_bg': '#1a1a2e',
            'text': '#ffffff',
            'accent': '#4fc3f7',
            'warning': '#ffb74d',
            'danger': '#ff6b6b',
            'success': '#69f0ae',
            'gpu': '#ba68c8',
            'graph_bg': '#000000'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
    def detect_gpu(self):
        """Detecta si hay GPU NVIDIA"""
        try:
            result = subprocess.run(['which', 'nvidia-smi'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def get_gpu_info(self):
        """Obtiene información de la GPU"""
        if not self.has_gpu:
            return {'usage': 0, 'memory': 0, 'temp': 0}
        
        try:
            # Usar nvidia-smi para obtener datos
            cmd = [
                'nvidia-smi',
                '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu',
                '--format=csv,noheader,nounits'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                gpu_usage, mem_used, mem_total, temp = map(float, result.stdout.strip().split(', '))
                mem_percent = (mem_used / mem_total) * 100
                return {
                    'usage': gpu_usage,
                    'memory': mem_percent,
                    'temp': temp
                }
        except Exception as e:
            print(f"Error GPU: {e}")
        
        return {'usage': 0, 'memory': 0, 'temp': 0}
    
    def load_config(self):
        """Carga configuración desde archivo"""
        default = {
            'update_interval': 2.0,
            'theme': 'dark',
            'show_gpu': True,
            'show_temp': True
        }
        
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default.update(loaded)
        except:
            pass
        
        return default
    
    def build_ui(self):
        """Construye la interfaz completa"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🌙 MOONLIGHT MONITOR",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        ).pack(side=tk.LEFT)
        
        # Status
        self.status_label = tk.Label(
            title_frame,
            text="● Monitoreando",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['success']
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Frame para métricas principales
        metrics_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Crear 4 cards en 2x2
        self.cpu_card = self.create_card(metrics_frame, "CPU", "0%", 0, 0)
        self.ram_card = self.create_card(metrics_frame, "RAM", "0%", 0, 1)
        self.gpu_card = self.create_card(metrics_frame, "GPU", "0%", 1, 0)
        self.temp_card = self.create_card(metrics_frame, "TEMP", "0°C", 1, 1)
        
        # Frame para info detallada
        detail_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Info Moonlight (izquierda)
        ml_frame = tk.Frame(detail_frame, bg=self.colors['card_bg'], bd=1, relief=tk.SUNKEN)
        ml_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            ml_frame,
            text="📊 MOONLIGHT (Esta App)",
            font=("Arial", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['accent']
        ).pack(pady=(15, 10))
        
        self.ml_cpu_label = tk.Label(
            ml_frame,
            text="CPU: 0.0%",
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        )
        self.ml_cpu_label.pack(pady=5)
        
        self.ml_ram_label = tk.Label(
            ml_frame,
            text="RAM: 0.0 MB",
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        )
        self.ml_ram_label.pack(pady=5)
        
        self.ml_percent_label = tk.Label(
            ml_frame,
            text="(0.000% del total)",
            font=("Arial", 9),
            bg=self.colors['card_bg'],
            fg="#888888"
        )
        self.ml_percent_label.pack(pady=5)
        
        # Info Sistema (derecha)
        sys_frame = tk.Frame(detail_frame, bg=self.colors['card_bg'], bd=1, relief=tk.SUNKEN)
        sys_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            sys_frame,
            text="💻 SISTEMA",
            font=("Arial", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['accent']
        ).pack(pady=(15, 10))
        
        self.disk_label = tk.Label(
            sys_frame,
            text="Disco: 0% (0.0 GB libre)",
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        )
        self.disk_label.pack(pady=5)
        
        self.net_label = tk.Label(
            sys_frame,
            text="Red: ↑ 0 MB ↓ 0 MB",
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        )
        self.net_label.pack(pady=5)
        
        self.time_label = tk.Label(
            sys_frame,
            text="Actualizado: --:--:--",
            font=("Arial", 9),
            bg=self.colors['card_bg'],
            fg="#888888"
        )
        self.time_label.pack(pady=5)
        
        # Frame para gráficos
        graph_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Canvas para gráfico de CPU
        self.cpu_canvas = tk.Canvas(
            graph_frame,
            bg=self.colors['graph_bg'],
            height=120,
            highlightthickness=0
        )
        self.cpu_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        tk.Label(
            graph_frame,
            text="Historial CPU (últimos 30 segundos)",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        # Frame para procesos
        proc_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        proc_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            proc_frame,
            text="📋 PROCESOS ACTIVOS",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Lista de procesos
        self.proc_listbox = tk.Listbox(
            proc_frame,
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['accent'],
            font=("Consolas", 9),
            height=6
        )
        
        scrollbar = ttk.Scrollbar(proc_frame, orient=tk.VERTICAL)
        self.proc_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.proc_listbox.yview)
        
        self.proc_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pie de página
        footer = tk.Frame(main_frame, bg=self.colors['bg'])
        footer.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            footer,
            text="🕹️ Modo Gaming - Bajo consumo | ESC para salir",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg="#888888"
        ).pack()
    
    def create_card(self, parent, title, value, row, col):
        """Crea una tarjeta de métrica"""
        card = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            bd=1,
            relief=tk.RAISED
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configurar grid
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)
        
        # Título
        tk.Label(
            card,
            text=title,
            font=("Arial", 11),
            bg=self.colors['card_bg'],
            fg="#aaaaaa"
        ).pack(pady=(15, 5))
        
        # Valor
        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 20, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['accent']
        )
        value_label.pack(pady=5)
        
        # Barra de progreso
        bar_canvas = tk.Canvas(
            card,
            height=10,
            bg=self.colors['card_bg'],
            highlightthickness=0
        )
        bar_canvas.pack(pady=(5, 15), padx=15, fill=tk.X)
        
        return {
            'frame': card,
            'value': value_label,
            'bar': bar_canvas,
            'title': title
        }
    
    def update_bar(self, canvas, percent, is_gpu=False):
        """Actualiza la barra de progreso con color apropiado"""
        canvas.delete("all")
        
        width = canvas.winfo_width()
        if width < 10:
            width = 150
        
        # Determinar color según porcentaje y tipo
        if percent > 85:
            color = self.colors['danger']
        elif percent > 70:
            color = self.colors['warning']
        elif is_gpu:
            color = self.colors['gpu']
        else:
            color = self.colors['success']
        
        # Dibujar barra
        bar_width = min(int(width * percent / 100), width)
        canvas.create_rectangle(0, 0, bar_width, 10, fill=color, outline="")
        
        # Fondo gris para el resto
        canvas.create_rectangle(bar_width, 0, width, 10, fill="#333333", outline="")
    
    def draw_graph(self, canvas, history, color):
        """Dibuja un gráfico simple en el canvas"""
        canvas.delete("all")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
        
        if not history:
            return
        
        # Escalar valores
        max_val = max(history) if max(history) > 0 else 100
        scaled = [(value / max_val) * (height - 20) for value in history]
        
        # Dibujar línea
        points = []
        for i, val in enumerate(scaled):
            x = (i / len(history)) * width
            y = height - val - 10
            points.extend([x, y])
        
        if len(points) >= 4:
            canvas.create_line(points, fill=color, width=2, smooth=True)
    
    def update_data(self):
        """Actualiza todos los datos y la interfaz"""
        if not self.running:
            return
        
        try:
            # Obtener datos del sistema
            cpu_percent = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net = psutil.net_io_counters()
            
            # Obtener nuestro consumo
            ml_cpu = self.process.cpu_percent(interval=0.1)
            ml_mem = self.process.memory_info().rss / 1024 / 1024  # MB
            ml_mem_percent = (self.process.memory_info().rss / mem.total) * 100
            
            # Obtener GPU
            gpu_data = self.get_gpu_info()
            
            # Temperatura
            cpu_temp = 0
            try:
                if hasattr(psutil, 'sensors_temperatures'):
                    temps = psutil.sensors_temperatures()
                    if 'coretemp' in temps:
                        cpu_temp = temps['coretemp'][0].current
            except:
                pass
            
            # Actualizar historial
            self.cpu_history.append(cpu_percent)
            self.ram_history.append(mem.percent)
            if len(self.cpu_history) > self.history_max:
                self.cpu_history.pop(0)
                self.ram_history.pop(0)
            
            # Actualizar cards
            self.update_card(self.cpu_card, cpu_percent, f"{cpu_percent:.1f}%")
            self.update_card(self.ram_card, mem.percent, f"{mem.percent:.1f}%")
            
            # GPU
            if gpu_data['usage'] > 0:
                self.update_card(self.gpu_card, gpu_data['usage'], f"{gpu_data['usage']:.1f}%", is_gpu=True)
            else:
                self.cards['gpu']['value'].config(text="N/A")
                self.update_bar(self.cards['gpu']['bar'], 0)
            
            # Temperatura
            if cpu_temp > 0:
                self.update_card(self.temp_card, min(cpu_temp, 100), f"{cpu_temp:.0f}°C")
            else:
                self.cards['temp']['value'].config(text="N/A")
                self.update_bar(self.cards['temp']['bar'], 0)
            
            # Actualizar info Moonlight
            self.ml_cpu_label.config(text=f"CPU: {ml_cpu:.1f}%")
            self.ml_ram_label.config(text=f"RAM: {ml_mem:.1f} MB")
            self.ml_percent_label.config(text=f"({ml_mem_percent:.3f}% del total)")
            
            # Actualizar info sistema
            self.disk_label.config(text=f"Disco: {disk.percent:.1f}% ({disk.free/1e9:.1f} GB libre)")
            self.net_label.config(text=f"Red: ↑ {net.bytes_sent/1e6:.1f} MB ↓ {net.bytes_recv/1e6:.1f} MB")
            self.time_label.config(text=f"Actualizado: {datetime.now().strftime('%H:%M:%S')}")
            
            # Actualizar gráfico
            self.draw_graph(self.cpu_canvas, self.cpu_history, self.colors['accent'])
            
            # Actualizar lista de procesos
            self.update_process_list()
            
            # Actualizar estado
            load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
            if load_avg > 5:
                self.status_label.config(text="⚠️ Alta carga", fg=self.colors['warning'])
            else:
                self.status_label.config(text="● Monitoreando", fg=self.colors['success'])
            
        except Exception as e:
            print(f"Error actualizando: {e}")
            self.status_label.config(text="⚠️ Error", fg=self.colors['danger'])
        
        # Programar próxima actualización
        self.root.after(self.update_interval, self.update_data)
    
    def update_card(self, card, percent, text, is_gpu=False):
        """Actualiza una tarjeta individual"""
        card['value'].config(text=text)
        self.update_bar(card['bar'], percent, is_gpu)
    
    def update_process_list(self):
        """Actualiza la lista de procesos"""
        self.proc_listbox.delete(0, tk.END)
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    # Excluirnos a nosotros mismos
                    if proc.pid != os.getpid():
                        processes.append(proc.info)
                except:
                    pass
                
                if len(processes) >= 8:
                    break
            
            # Ordenar por CPU
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            for proc in processes[:7]:
                name = proc.get('name', 'N/A')[:25]
                cpu = proc.get('cpu_percent', 0)
                mem = proc.get('memory_percent', 0)
                self.proc_listbox.insert(tk.END, f"{name:25} | CPU: {cpu:5.1f}% | RAM: {mem:5.1f}%")
        
        except Exception as e:
            self.proc_listbox.insert(tk.END, f"Error obteniendo procesos: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Hacer que las cards se expandan
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
        
        self.root.mainloop()

def main():
    """Función principal"""
    # Verificar dependencias
    try:
        import psutil
    except ImportError:
        print("❌ ERROR: psutil no está instalado")
        print("Instala con: sudo pacman -S python-psutil")
        input("Presiona Enter para salir...")
        return
    
    print("🌙 Iniciando Moonlight Monitor...")
    print("   Interfaz gráfica - Se abrirá en 2 segundos")
    
    # Crear y ejecutar aplicación
    app = Moonlight()
    app.run()

if __name__ == "__main__":
    main()