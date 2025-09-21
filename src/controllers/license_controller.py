"""
License Dialog for Business Management App
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from controllers.license_controller import LicenseController

class LicenseDialog:
    """Dialog for license input and validation"""
    
    def __init__(self, parent):
        self.parent = parent
        self.license_controller = LicenseController()
        self.result = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Aktivasi Lisensi")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.create_widgets()
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Aktivasi Lisensi Aplikasi", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # App info
        info_text = """
Business Management App v1.0.0

Aplikasi ini memerlukan lisensi untuk dapat digunakan.
Silakan masukkan kode lisensi yang Anda dapatkan.

Untuk demo, gunakan: DEMO-KEY-1234-5678
        """
        
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # Hardware ID
        hw_frame = ttk.Frame(main_frame)
        hw_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(hw_frame, text="Hardware ID:").grid(row=0, column=0, sticky=tk.W)
        
        hardware_id = self.license_controller.get_hardware_id()
        hw_id_var = tk.StringVar(value=hardware_id)
        
        hw_id_entry = ttk.Entry(hw_frame, textvariable=hw_id_var, width=40, state="readonly")
        hw_id_entry.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
        
        # Copy button
        copy_btn = ttk.Button(hw_frame, text="Salin", 
                             command=lambda: self.copy_to_clipboard(hardware_id))
        copy_btn.grid(row=1, column=1, padx=(5, 0))
        
        # License key
        ttk.Label(main_frame, text="Kode Lisensi:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.license_var = tk.StringVar()
        self.license_entry = ttk.Entry(main_frame, textvariable=self.license_var, width=40)
        self.license_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Bind Enter key
        self.license_entry.bind('<Return>', lambda e: self.on_activate())
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # Activate button
        activate_btn = ttk.Button(button_frame, text="Aktivasi", 
                                 command=self.on_activate)
        activate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Demo button
        demo_btn = ttk.Button(button_frame, text="Gunakan Demo", 
                             command=self.on_demo)
        demo_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Keluar", 
                             command=self.on_cancel)
        exit_btn.grid(row=0, column=2)
        
        # Status label
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                     foreground="red")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        hw_frame.columnconfigure(0, weight=1)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(text)
        messagebox.showinfo("Info", "Hardware ID telah disalin ke clipboard!")
    
    def on_activate(self):
        """Handle license activation"""
        license_key = self.license_var.get().strip()
        
        if not license_key:
            self.status_var.set("Silakan masukkan kode lisensi!")
            return
        
        # Validate license
        if self.license_controller.validate_license_key(license_key):
            # Save license
            if self.license_controller.save_license(license_key):
                messagebox.showinfo("Sukses", "Lisensi berhasil diaktifkan!")
                self.result = True
                self.dialog.destroy()
            else:
                self.status_var.set("Gagal menyimpan lisensi!")
        else:
            self.status_var.set("Kode lisensi tidak valid!")
    
    def on_demo(self):
        """Handle demo license"""
        demo_key = self.license_controller.create_demo_license()
        if demo_key:
            messagebox.showinfo("Demo", 
                              f"Lisensi demo berhasil diaktifkan!\n\n"
                              f"Kode: {demo_key}\n\n"
                              f"Lisensi demo berlaku selama 30 hari.")
            self.result = True
            self.dialog.destroy()
        else:
            self.status_var.set("Gagal membuat lisensi demo!")
    
    def on_cancel(self):
        """Handle cancel"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda ingin keluar dari aplikasi?"):
            self.result = False
            self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return result"""
        self.dialog.wait_window()
        return self.result

def show_license_dialog():
    """Standalone function to show license dialog"""
    root = tk.Tk()
    root.withdraw()
    
    dialog = LicenseDialog(root)
    result = dialog.show()
    
    root.destroy()
    return result

if __name__ == "__main__":
    result = show_license_dialog()
    print(f"Dialog result: {result}")