import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib
from interface_rc import InterfaceRC
from interface_admin import InterfaceAdmin  

# 🎨 Palette
PRIMARY_COLOR = "#0D6EFD"
SECONDARY_COLOR = "#6C757D"
BACKGROUND_COLOR = "#F8F9FA"
TEXT_COLOR = "#212529"
ALERT_COLOR = "#DC3545"
SUCCESS_COLOR = "#198754"

class AuthManager:
    """Gestionnaire d'authentification et de sessions"""
    def __init__(self):
        self.current_user = None
        self.current_role = None
    
    def login(self, username, password):
        """Authentifie un utilisateur"""
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="centre_formation"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, role FROM users WHERE username=%s AND password_hash=%s",
                          (username, hashed_pass))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                self.current_user = result[0]
                self.current_role = result[1]
                return True, result[1]
            return False, None
            
        except mysql.connector.Error as err:
            return False, f"Erreur DB: {err}"
    
    def logout(self):
        """Déconnecte l'utilisateur"""
        self.current_user = None
        self.current_role = None
    
    def has_permission(self, permission):
        """Vérifie les permissions utilisateur"""
        permissions = {
            'admin': ['all'],  # Admin peut tout faire
            'rc': ['leads', 'enfants', 'appels', 'formations', 'sessions', 
                   'seances', 'inscriptions', 'factures', 'echeances', 'paiements']
            # RC ne peut pas gérer les formateurs (paie)
        }
        
        if self.current_role == 'admin':
            return True
        
        return permission in permissions.get(self.current_role, [])

# Instance globale
auth_manager = AuthManager()

def login():
    """Fonction de connexion"""
    username = entry_user.get()
    password = entry_pass.get()
    
    if not username or not password:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        return
    
    success, role_or_error = auth_manager.login(username, password)
    
    if success:
        messagebox.showinfo("Succès", f"Bienvenue {role_or_error}")
        root.destroy()  # Ferme la fenêtre login
        
        # Lance l'interface appropriée selon le rôle
        if role_or_error.lower() == "rc":
            app = InterfaceRC()
            app.auth_manager = auth_manager  # Passe le gestionnaire d'auth
            app.mainloop()
        elif role_or_error.lower() == "admin":
            app = InterfaceAdmin()
            app.auth_manager = auth_manager
            app.mainloop()
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects" if isinstance(role_or_error, str) and "Erreur DB" not in role_or_error else role_or_error)

def create_user_interface():
    """Interface pour créer un utilisateur (temporaire)"""
    def add_user():
        username = entry_new_user.get()
        password = entry_new_pass.get()
        role = combo_role.get()
        
        if not all([username, password, role]):
            messagebox.showerror("Erreur", "Tous les champs sont requis")
            return
        
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="centre_formation"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, role, created_at) VALUES (%s, %s, %s, NOW())",
                          (username, hashed_pass, role))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Succès", f"Utilisateur {role} créé avec succès")
            create_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur DB: {err}")
    
    create_window = tk.Toplevel(root)
    create_window.title("Créer un utilisateur")
    create_window.geometry("350x280")
    create_window.configure(bg=BACKGROUND_COLOR)
    create_window.resizable(False, False)
    
    # Centrer la fenêtre
    create_window.transient(root)
    create_window.grab_set()
    
    # Frame principal avec padding
    main_frame = tk.Frame(create_window, bg=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    tk.Label(main_frame, text="Nouveau utilisateur", font=("Segoe UI", 14, "bold"),
             bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=(0, 20))
    
    # Nom d'utilisateur
    tk.Label(main_frame, text="Nom d'utilisateur", bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
             font=("Segoe UI", 10)).pack(anchor="w")
    entry_new_user = tk.Entry(main_frame, font=("Segoe UI", 11), width=25, relief="solid", bd=1)
    entry_new_user.pack(pady=(2, 10), fill="x")
    
    # Mot de passe
    tk.Label(main_frame, text="Mot de passe", bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
             font=("Segoe UI", 10)).pack(anchor="w")
    entry_new_pass = tk.Entry(main_frame, show="*", font=("Segoe UI", 11), width=25, relief="solid", bd=1)
    entry_new_pass.pack(pady=(2, 10), fill="x")
    
    # Rôle
    tk.Label(main_frame, text="Rôle", bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
             font=("Segoe UI", 10)).pack(anchor="w")
    from tkinter import ttk
    combo_role = ttk.Combobox(main_frame, values=["admin", "rc"], state="readonly", font=("Segoe UI", 11))
    combo_role.pack(pady=(2, 20), fill="x")
    combo_role.set("rc")
    
    # Boutons
    button_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
    button_frame.pack(fill="x", pady=10)
    
    tk.Button(button_frame, text="Créer", command=add_user,
              bg=SUCCESS_COLOR, fg="white", font=("Segoe UI", 10, "bold"),
              bd=0, padx=20, pady=8, cursor="hand2").pack(side="left", padx=(0, 10))
    
    tk.Button(button_frame, text="Annuler", command=create_window.destroy,
              bg=SECONDARY_COLOR, fg="white", font=("Segoe UI", 10, "bold"),
              bd=0, padx=20, pady=8, cursor="hand2").pack(side="left")

# =============================
# Fenêtre login principale
# =============================
root = tk.Tk()
root.title("Centre de Formation - Connexion")
root.configure(bg=BACKGROUND_COLOR)
root.geometry("450x400")
root.resizable(False, False)

# Centrer la fenêtre sur l'écran
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
pos_y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

# Frame principal avec padding
main_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
main_frame.pack(fill="both", expand=True, padx=30, pady=30)

# Titre principal
title_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
title_frame.pack(pady=(0, 30))

tk.Label(title_frame, text="Centre de Formation", font=("Segoe UI", 22, "bold"),
         bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR).pack()
tk.Label(title_frame, text="Système de Gestion", font=("Segoe UI", 12),
         bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=(5, 0))

# Formulaire de connexion dans un frame dédié
form_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
form_frame.pack(fill="x", pady=(0, 20))

# Nom d'utilisateur
tk.Label(form_frame, text="Nom d'utilisateur", bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
         font=("Segoe UI", 10, "bold")).pack(anchor="w")
entry_user = tk.Entry(form_frame, font=("Segoe UI", 12), width=25, relief="solid", bd=1)
entry_user.pack(pady=(5, 15), fill="x")

# Mot de passe
tk.Label(form_frame, text="Mot de passe", bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
         font=("Segoe UI", 10, "bold")).pack(anchor="w")
entry_pass = tk.Entry(form_frame, show="*", font=("Segoe UI", 12), width=25, relief="solid", bd=1)
entry_pass.pack(pady=(5, 20), fill="x")

# Permettre connexion avec Entrée
entry_pass.bind('<Return>', lambda event: login())

# Boutons principaux dans un frame horizontal
button_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
button_frame.pack(fill="x", pady=(0, 15))

# Bouton Se connecter
btn_login = tk.Button(button_frame, text="Se connecter", command=login,
                      bg=PRIMARY_COLOR, fg="white", font=("Segoe UI", 11, "bold"),
                      bd=0, padx=25, pady=10, cursor="hand2", relief="flat")
btn_login.pack(side="left", padx=(0, 10), fill="x", expand=True)

# Bouton Annuler
btn_cancel = tk.Button(button_frame, text="Annuler", command=root.quit,
                       bg=SECONDARY_COLOR, fg="white", font=("Segoe UI", 11, "bold"),
                       bd=0, padx=25, pady=10, cursor="hand2", relief="flat")
btn_cancel.pack(side="left", fill="x", expand=True)

# Séparateur visuel
separator = tk.Frame(main_frame, height=1, bg=SECONDARY_COLOR)
separator.pack(fill="x", pady=15)

# Bouton pour créer un utilisateur (séparé des boutons principaux)
btn_create = tk.Button(main_frame, text="Créer un nouvel utilisateur", command=create_user_interface,
                       bg=SUCCESS_COLOR, fg="white", font=("Segoe UI", 10, "bold"),
                       bd=0, padx=20, pady=8, cursor="hand2", relief="flat")
btn_create.pack(pady=10)

# Focus sur le champ utilisateur au démarrage
entry_user.focus_set()

if __name__ == "__main__":
    root.mainloop()