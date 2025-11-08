#!/usr/bin/env python3
"""
NVIDIA GPU Power Controller
Professional GPU power management tool with automatic detection
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import threading
import time

class GPUPowerController:
    def __init__(self, root):
        self.root = root
        self.root.title("NVIDIA GPU Power Controller")
        self.root.geometry("520x400")
        self.root.resizable(False, False)
        
        # Colors - Industrial style
        self.bg_dark = "#2b2b2b"
        self.bg_medium = "#3a3a3a"
        self.fg_light = "#e0e0e0"
        self.fg_accent = "#ff8800"
        self.fg_dim = "#888888"
        
        self.root.configure(bg=self.bg_dark)
        
        # GPU data
        self.gpu_name = "Detecting..."
        self.min_power = 0
        self.max_power = 0
        self.current_power = 0
        self.default_power = 0
        self.temperature = 0
        self.gpu_utilization = 0
        self.power_draw = 0
        self.vram_total = 0
        self.vram_used = 0
        self.vram_percent = 0
        
        # Detect GPU and limits
        self.detect_gpu()
        
        # Build UI
        self.create_widgets()
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_gpu, daemon=True)
        self.monitor_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def detect_gpu(self):
        """Detect GPU name and power limits"""
        try:
            # Get GPU name
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                check=True
            )
            self.gpu_name = result.stdout.strip()
            
            # Get power limits
            result = subprocess.run(
                ['nvidia-smi', '-q'],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout
            
            # Parse power limits
            min_match = re.search(r'Min Power Limit\s+:\s+([\d.]+)\s+W', output)
            max_match = re.search(r'Max Power Limit\s+:\s+([\d.]+)\s+W', output)
            default_match = re.search(r'Default Power Limit\s+:\s+([\d.]+)\s+W', output)
            current_match = re.search(r'Current Power Limit\s+:\s+([\d.]+)\s+W', output)
            
            if min_match and max_match:
                self.min_power = float(min_match.group(1))
                self.max_power = float(max_match.group(1))
                self.default_power = float(default_match.group(1)) if default_match else self.max_power
                self.current_power = float(current_match.group(1)) if current_match else self.max_power
            else:
                raise ValueError("Could not parse power limits")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect GPU:\n{str(e)}")
            self.gpu_name = "Unknown GPU"
            self.min_power = 100
            self.max_power = 200
            self.default_power = 200
            self.current_power = 200
    
    def get_gpu_stats(self):
        """Get current GPU statistics"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu,utilization.gpu,power.draw,memory.total,memory.used',
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                check=True
            )
            
            values = result.stdout.strip().split(', ')
            self.temperature = int(values[0])
            self.gpu_utilization = int(values[1])
            self.power_draw = float(values[2])
            self.vram_total = int(values[3])
            self.vram_used = int(values[4])
            self.vram_percent = int((self.vram_used / self.vram_total) * 100) if self.vram_total > 0 else 0
            
        except Exception:
            pass
    
    def monitor_gpu(self):
        """Background thread to monitor GPU stats"""
        while self.monitoring:
            self.get_gpu_stats()
            self.root.after(0, self.update_stats_display)
            time.sleep(2)
    
    def update_stats_display(self):
        """Update the stats labels"""
        self.temp_label.config(text=f"Temp: {self.temperature}°C")
        self.power_label.config(text=f"Power: {self.power_draw:.1f}W")
        self.util_label.config(text=f"Usage: {self.gpu_utilization}%")
        self.vram_label.config(text=f"VRAM: {self.vram_used}MB / {self.vram_total}MB | ({self.vram_percent}%)")
    
    def create_widgets(self):
        """Create UI elements"""
        
        # Top section - GPU Info
        info_frame = tk.Frame(self.root, bg=self.bg_medium, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # GPU Name
        gpu_label = tk.Label(
            info_frame,
            text=self.gpu_name,
            font=("Consolas", 13, "bold"),
            bg=self.bg_medium,
            fg=self.fg_accent,
            anchor="w"
        )
        gpu_label.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Stats row
        stats_frame = tk.Frame(info_frame, bg=self.bg_medium)
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.temp_label = tk.Label(
            stats_frame,
            text=f"Temp: {self.temperature}°C",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_light
        )
        self.temp_label.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            stats_frame,
            text="|",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_dim
        ).pack(side=tk.LEFT, padx=5)
        
        self.power_label = tk.Label(
            stats_frame,
            text=f"Power: {self.power_draw:.1f}W",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_light
        )
        self.power_label.pack(side=tk.LEFT, padx=(10, 15))
        
        tk.Label(
            stats_frame,
            text="|",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_dim
        ).pack(side=tk.LEFT, padx=5)
        
        self.util_label = tk.Label(
            stats_frame,
            text=f"Usage: {self.gpu_utilization}%",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_light
        )
        self.util_label.pack(side=tk.LEFT, padx=10)
        
        # VRAM row
        vram_frame = tk.Frame(info_frame, bg=self.bg_medium)
        vram_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.vram_label = tk.Label(
            vram_frame,
            #text=f"VRAM: {self.vram_total}MB / {self.vram_used}MB ({self.vram_percent}%)",
            text=f"VRAM: {self.vram_used}MB / {self.vram_total}MB | ({self.vram_percent}%)",
            font=("Consolas", 10),
            bg=self.bg_medium,
            fg=self.fg_light
        )
        self.vram_label.pack(side=tk.LEFT)
        
        # Middle section - Power Control
        control_frame = tk.Frame(self.root, bg=self.bg_dark)
        control_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            control_frame,
            text="POWER LIMIT CONTROL",
            font=("Consolas", 11, "bold"),
            bg=self.bg_dark,
            fg=self.fg_light
        )
        title_label.pack(pady=(15, 10))
        
        # Current power limit display
        self.power_display = tk.Label(
            control_frame,
            text=f"{int(self.current_power)}W ({int((self.current_power/self.max_power)*100)}%)",
            font=("Consolas", 16, "bold"),
            bg=self.bg_dark,
            fg=self.fg_accent
        )
        self.power_display.pack(pady=5)
        
        # Slider
        slider_frame = tk.Frame(control_frame, bg=self.bg_dark)
        slider_frame.pack(pady=10)
        
        self.power_slider = tk.Scale(
            slider_frame,
            from_=self.min_power,
            to=self.max_power,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.update_power_display,
            showvalue=False,
            bg=self.bg_medium,
            fg=self.fg_light,
            troughcolor=self.bg_dark,
            highlightthickness=0,
            activebackground=self.fg_accent,
            sliderrelief=tk.FLAT
        )
        self.power_slider.set(self.current_power)
        self.power_slider.pack()
        
        # Min/Max labels
        limits_frame = tk.Frame(control_frame, bg=self.bg_dark)
        limits_frame.pack(fill=tk.X, padx=60)
        
        tk.Label(
            limits_frame,
            text=f"Min: {int(self.min_power)}W",
            font=("Consolas", 9),
            bg=self.bg_dark,
            fg=self.fg_dim
        ).pack(side=tk.LEFT)
        
        tk.Label(
            limits_frame,
            text=f"Max: {int(self.max_power)}W",
            font=("Consolas", 9),
            bg=self.bg_dark,
            fg=self.fg_dim
        ).pack(side=tk.RIGHT)
        
        # Bottom section - Buttons
        button_frame = tk.Frame(self.root, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Apply button
        apply_btn = tk.Button(
            button_frame,
            text="APPLY",
            command=self.apply_power_limit,
            bg=self.fg_accent,
            fg="#000000",
            font=("Consolas", 10, "bold"),
            relief=tk.FLAT,
            width=12,
            height=2,
            activebackground="#ff9900",
            cursor="hand2"
        )
        apply_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="RESET",
            command=self.reset_power,
            bg=self.bg_medium,
            fg=self.fg_light,
            font=("Consolas", 10, "bold"),
            relief=tk.FLAT,
            width=12,
            height=2,
            activebackground="#4a4a4a",
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Help button
        help_btn = tk.Button(
            button_frame,
            text="HELP",
            command=self.show_help,
            bg=self.bg_medium,
            fg=self.fg_light,
            font=("Consolas", 10, "bold"),
            relief=tk.FLAT,
            width=12,
            height=2,
            activebackground="#4a4a4a",
            cursor="hand2"
        )
        help_btn.pack(side=tk.LEFT, padx=5)
    
    def update_power_display(self, value):
        """Update the power display label"""
        power = int(float(value))
        percentage = int((power / self.max_power) * 100)
        self.power_display.config(text=f"{power}W ({percentage}%)")
    
    def apply_power_limit(self):
        """Apply the selected power limit"""
        power = int(self.power_slider.get())
        
        confirm = messagebox.askyesno(
            "Confirm",
            f"Apply power limit of {power}W?\n\nThis requires root privileges."
        )
        
        if not confirm:
            return
        
        try:
            result = subprocess.run(
                ['pkexec', 'nvidia-smi', '-pl', str(power)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.current_power = power
                messagebox.showinfo("Success", f"Power limit set to {power}W")
            else:
                messagebox.showerror("Error", f"Failed to apply limit:\n{result.stderr}")
        
        except FileNotFoundError:
            messagebox.showwarning(
                "pkexec not found",
                f"Run manually:\nsudo nvidia-smi -pl {power}"
            )
        
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{str(e)}")
    
    def reset_power(self):
        """Reset to default power limit"""
        self.power_slider.set(self.default_power)
        self.update_power_display(str(self.default_power))
    
    def show_help(self):
        """Show help dialog"""
        help_text = f"""NVIDIA GPU Power Controller

HOW IT WORKS:
This tool uses nvidia-smi to read and set GPU power limits.

Commands used:
• nvidia-smi --query-gpu=... (read GPU info)
• nvidia-smi -q (read power limits)
• nvidia-smi -pl <watts> (set power limit)

Statistics monitored:
• Temperature, Power Draw, GPU Usage
• VRAM Total, Used, and Usage Percentage

YOUR GPU:
• Name: {self.gpu_name}
• Min Power: {int(self.min_power)}W
• Max Power: {int(self.max_power)}W
• Default: {int(self.default_power)}W
• VRAM: {self.vram_total}MB

UNINSTALL:
1. Delete this script file
2. Remove desktop shortcut:
   rm ~/.local/share/applications/gpu-power-control.desktop
3. Update cache:
   update-desktop-database ~/.local/share/applications/

NOTE:
Power limit settings do not persist after reboot.
You must reapply them after each restart.

For more information, see README.md
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x450")
        help_window.configure(bg=self.bg_dark)
        help_window.resizable(False, False)
        
        text_widget = tk.Text(
            help_window,
            font=("Consolas", 9),
            bg=self.bg_medium,
            fg=self.fg_light,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_btn = tk.Button(
            help_window,
            text="CLOSE",
            command=help_window.destroy,
            bg=self.bg_medium,
            fg=self.fg_light,
            font=("Consolas", 10, "bold"),
            relief=tk.FLAT,
            width=15,
            height=2
        )
        close_btn.pack(pady=(0, 15))
    
    def on_closing(self):
        """Handle window close"""
        self.monitoring = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = GPUPowerController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
