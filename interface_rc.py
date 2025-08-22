import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from backend import *  # Import du vrai backend MySQL
from datetime import datetime

class InterfaceRC(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface RC - Centre de Formation")
        self.geometry("1400x800")
        self.resizable(True, True)
        self.configure(bg="#f0f0f0")

        # ===== MENU GAUCHE =====
        self.menu_frame = tk.Frame(self, width=200, bg="#2c3e50")
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        # Titre du menu
        tk.Label(self.menu_frame, text="MODULES", font=("Arial", 14, "bold"), 
                fg="white", bg="#2c3e50").pack(pady=10)

        self.content_frame = tk.Frame(self, bg="#ecf0f1")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Liste des modules que le RC peut gérer
        self.modules = [
            "Leads/Parents", "Enfants", "Appels", "Formations", 
            "Sessions", "Séances", "Inscriptions", "Factures", 
            "Échéances", "Paiements", "Formateurs"
        ]

        self.buttons = []
        for module in self.modules:
            btn = tk.Button(self.menu_frame, text=module, fg="white", bg="#34495e",
                            font=("Arial", 11), relief="flat", bd=0, pady=8,
                            command=lambda m=module: self.show_module(m))
            btn.pack(fill="x", padx=5, pady=2)
            self.buttons.append(btn)

        self.current_frame = None
        self.show_module("Leads/Parents")  # affichage par défaut

    def show_module(self, module_name):
        # Réinitialiser les couleurs des boutons
        for btn in self.buttons:
            btn.configure(bg="#34495e")
        
        # Colorer le bouton actif
        for i, module in enumerate(self.modules):
            if module == module_name:
                self.buttons[i].configure(bg="#3498db")
                break

        if self.current_frame:
            self.current_frame.destroy()

        frames = {
            "Enfants": EnfantsFrame,
            "Leads/Parents": LeadsFrame,
            "Appels": AppelsFrame,
            "Formations": FormationsFrame,
            "Sessions": SessionsFrame,
            "Séances": SeancesFrame,
            "Inscriptions": InscriptionsFrame,
            "Factures": FacturesFrame,
            "Échéances": EcheancesFrame,
            "Paiements": PaiementsFrame,
            "Formateurs": FormateursFrame
        }

        self.current_frame = frames[module_name](self.content_frame)
        self.current_frame.pack(expand=True, fill="both", padx=10, pady=10)


# ===== MODULE DE BASE POUR CRUD =====
class BaseCRUDFrame(tk.Frame):
    def __init__(self, parent, title, columns, fields):
        super().__init__(parent, bg="#ecf0f1")
        self.title = title
        self.columns = columns
        self.fields = fields

        # Titre principal
        title_frame = tk.Frame(self, bg="#ecf0f1")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text=f"{title} - Formulaire", font=("Arial", 16, "bold"), 
                bg="#ecf0f1").pack(side="left")

        # Créer le conteneur principal avec deux sections
        main_container = tk.Frame(self, bg="#ecf0f1")
        main_container.pack(expand=True, fill="both")

        # ===== SECTION FORMULAIRE =====
        form_frame = tk.LabelFrame(main_container, text="Formulaire", font=("Arial", 12, "bold"),
                                  bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        form_frame.pack(fill="x", padx=5, pady=5)

        # Créer les champs dynamiquement
        self.entries = {}
        self.create_form_fields(form_frame)

        # Séparateur visuel
        separator = tk.Frame(form_frame, height=2, bg="#bdc3c7")
        separator.pack(fill="x", pady=10)

        # Boutons d'action - maintenant après les champs
        btn_frame = tk.Frame(form_frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="Ajouter", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 command=self.add_item, width=12, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modifier", bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                 command=self.update_item, width=12, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Supprimer", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 command=self.delete_item, width=12, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Vider", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                 command=self.clear_form, width=12, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rafraîchir", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 command=self.load_data, width=12, height=2).pack(side="left", padx=5)

        # ===== SECTION TABLEAU =====
        table_frame = tk.LabelFrame(main_container, text="Liste des données", font=("Arial", 12, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        table_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Treeview avec scrollbars
        tree_container = tk.Frame(table_frame, bg="#ecf0f1")
        tree_container.pack(expand=True, fill="both", padx=5, pady=5)

        self.tree = ttk.Treeview(tree_container, columns=self.columns, show="headings", height=15)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Placement du treeview et des scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configuration des colonnes
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=80)

        # Bind pour sélection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_data()

    def create_form_fields(self, parent):
        """Créer les champs du formulaire dynamiquement avec une meilleure organisation"""
        # Frame principal pour les champs
        fields_container = tk.Frame(parent, bg="#ecf0f1")
        fields_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Calculer le nombre de lignes nécessaires (3 colonnes par ligne)
        cols_per_row = 3
        rows_needed = (len(self.fields) + cols_per_row - 1) // cols_per_row
        
        # Si on a plus de 4 lignes, on crée un canvas avec scrollbar
        if rows_needed > 4:
            # Canvas pour permettre le scroll
            canvas = tk.Canvas(fields_container, bg="#ecf0f1", height=200)
            scrollbar = ttk.Scrollbar(fields_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            form_frame = scrollable_frame
        else:
            form_frame = fields_container

        # Créer les champs dans le frame
        row = 0
        col = 0
        
        for field in self.fields:
            # Frame pour chaque champ (label + widget)
            field_frame = tk.Frame(form_frame, bg="#ecf0f1")
            field_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            # Label
            label_text = field.replace('_', ' ').title()
            if field == 'id':
                label_text = "ID"
            elif field == 'whatsapp_url':
                label_text = "WhatsApp URL"
            elif field == 'num_tel_papa':
                label_text = "Tél Papa"
            elif field == 'num_tel_maman':
                label_text = "Tél Maman"
            elif field == 'num_tel_enfant':
                label_text = "Tél Enfant"
                
            tk.Label(field_frame, text=f"{label_text}:", 
                    bg="#ecf0f1", font=("Arial", 9, "bold"), fg="#2c3e50").pack(anchor="w")
            
            # Widget de saisie selon le type de champ
            if field in ['description', 'notes', 'remarques', 'disponibilites', 'commentaire']:
                # Champ texte multiligne pour les descriptions longues
                text_widget = tk.Text(field_frame, font=("Arial", 9), width=20, height=3,
                                    relief="solid", bd=1, bg="white")
                text_widget.pack(fill="x", pady=2)
                self.entries[field] = text_widget
            else:
                # Champ texte simple
                entry = tk.Entry(field_frame, font=("Arial", 9), width=20,
                               relief="solid", bd=1, bg="white")
                entry.pack(fill="x", pady=2)
                self.entries[field] = entry
            
            # Passer à la colonne suivante
            col += 1
            if col >= cols_per_row:
                col = 0
                row += 1

        # Configurer le redimensionnement des colonnes
        for i in range(cols_per_row):
            form_frame.grid_columnconfigure(i, weight=1)

    def clear_form(self):
        """Vider tous les champs du formulaire"""
        for field, widget in self.entries.items():
            if isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)
            else:
                widget.delete(0, tk.END)

    def fill_form(self, data):
        """Remplir le formulaire avec les données"""
        self.clear_form()
        for field, widget in self.entries.items():
            if field in data and data[field] is not None:
                if isinstance(widget, tk.Text):
                    widget.insert(1.0, str(data[field]))
                else:
                    widget.insert(0, str(data[field]))

    def get_form_data(self):
        """Récupérer les données du formulaire"""
        data = {}
        for field, widget in self.entries.items():
            if isinstance(widget, tk.Text):
                value = widget.get(1.0, tk.END).strip()
            else:
                value = widget.get().strip()
            
            # Ne pas ajouter les valeurs vides sauf si c'est explicitement autorisé
            if value:
                data[field] = value
            elif field in ['description', 'notes', 'remarques', 'whatsapp_url', 'disponibilites', 
                          'num_tel_papa', 'num_tel_maman', 'num_tel_enfant', 'niveau_scolaire',
                          'prochain_rappel_at', 'dernier_rappel_at', 'date_tolerance', 'moyen',
                          'encaisse_par', 'justificatif_url', 'commentaire', 'date_arrivee', 'date_depart']:
                data[field] = None if not value else value
        return data

    def on_select(self, event):
        """Gérer la sélection dans le tableau"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            if values:
                # Créer un dictionnaire avec les données sélectionnées
                data = {}
                for i, col in enumerate(self.columns):
                    if i < len(values):
                        # Mapper les noms de colonnes aux noms de champs
                        field_name = col.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e')
                        if field_name == 'prenom':
                            field_name = 'prenom'
                        elif field_name == 'telephone':
                            field_name = 'telephone'
                        elif field_name == 'tel_papa':
                            field_name = 'num_tel_papa'
                        elif field_name == 'tel_maman':
                            field_name = 'num_tel_maman'
                        elif field_name == 'tel_enfant':
                            field_name = 'num_tel_enfant'
                        data[field_name] = values[i]
                self.fill_form(data)

    # Méthodes à implémenter dans les classes filles
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def add_item(self):
        pass

    def update_item(self):
        pass

    def delete_item(self):
        pass


# ===== MODULES SPÉCIFIQUES AVEC TOUS LES CHAMPS =====

class LeadsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Leads/Parents",
                         ("ID", "Nom", "Prénom", "Téléphone", "WhatsApp", "Disponibilités", "Statut", "Source"),
                         ["nom", "prenom", "telephone", "whatsapp_url", "disponibilites", "statut_pipeline", "source"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            leads = get_leads()
            for item in leads:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("nom", ""),
                    item.get("prenom", ""),
                    item.get("telephone", ""),
                    item.get("whatsapp_url", ""),
                    item.get("disponibilites", ""),
                    item.get("statut_pipeline", ""),
                    item.get("source", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des leads: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("nom") or not data.get("prenom"):
                messagebox.showerror("Erreur", "Nom et prénom sont obligatoires")
                return
            
            add_lead(
                nom=data.get("nom"),
                prenom=data.get("prenom"),
                telephone=data.get("telephone"),
                whatsapp_url=data.get("whatsapp_url"),
                disponibilites=data.get("disponibilites"),
                statut_pipeline=data.get("statut_pipeline", "nouveau"),
                source=data.get("source")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Lead ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un lead")
                return
            
            lead_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                update_lead(lead_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Lead modifié avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un lead")
                return
            
            lead_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer ce lead ?"):
                delete_lead(lead_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Lead supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class EnfantsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Enfants",
                         ("ID", "Parent ID", "Nom", "Prénom", "Naissance", "Tél Papa", "Tél Maman", "Tél Enfant", "Sexe", "Niveau", "Avant Centre", "Remarques"),
                         ["parent_id", "nom", "prenom", "date_naissance", "num_tel_papa", "num_tel_maman", 
                          "num_tel_enfant", "sexe", "niveau_scolaire", "niveau_avant_centre", "remarques"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            enfants = get_enfants()
            for item in enfants:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("parent_id", ""),
                    item.get("nom", ""),
                    item.get("prenom", ""),
                    item.get("date_naissance", ""),
                    item.get("num_tel_papa", ""),
                    item.get("num_tel_maman", ""),
                    item.get("num_tel_enfant", ""),
                    item.get("sexe", ""),
                    item.get("niveau_scolaire", ""),
                    item.get("niveau_avant_centre", ""),
                    item.get("remarques", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des enfants: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("nom") or not data.get("prenom") or not data.get("parent_id"):
                messagebox.showerror("Erreur", "Nom, prénom et parent ID sont obligatoires")
                return
            
            # Convertir parent_id en entier
            try:
                parent_id = int(data.get("parent_id"))
            except ValueError:
                messagebox.showerror("Erreur", "Parent ID doit être un nombre")
                return
            
            # Convertir niveau_avant_centre en booléen
            niveau_avant_centre = False
            if data.get("niveau_avant_centre"):
                niveau_avant_centre = data.get("niveau_avant_centre").lower() in ['true', '1', 'oui', 'yes']
            
            add_enfant(
                parent_id=parent_id,
                nom=data.get("nom"),
                prenom=data.get("prenom"),
                date_naissance=data.get("date_naissance"),
                num_tel_papa=data.get("num_tel_papa"),
                num_tel_maman=data.get("num_tel_maman"),
                num_tel_enfant=data.get("num_tel_enfant"),
                sexe=data.get("sexe"),
                niveau_scolaire=data.get("niveau_scolaire"),
                niveau_avant_centre=niveau_avant_centre,
                remarques=data.get("remarques")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Enfant ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un enfant")
                return
            
            enfant_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir parent_id en entier si fourni
                if 'parent_id' in data and data['parent_id']:
                    try:
                        data['parent_id'] = int(data['parent_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Parent ID doit être un nombre")
                        return
                
                # Convertir niveau_avant_centre en booléen si fourni
                if 'niveau_avant_centre' in data and data['niveau_avant_centre']:
                    data['niveau_avant_centre'] = data['niveau_avant_centre'].lower() in ['true', '1', 'oui', 'yes']
                
                update_enfant(enfant_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Enfant modifié avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un enfant")
                return
            
            enfant_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cet enfant ?"):
                delete_enfant(enfant_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Enfant supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class AppelsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Appels",
                         ("ID", "Lead ID", "Date", "Canal", "Résultat", "Notes", "Prochain Rappel", "Dernier Rappel", "Nb Rappels"),
                         ["lead_id", "date_appel", "canal", "resultat", "notes", "prochain_rappel_at", "dernier_rappel_at", "nb_rappels_programmes"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            appels = get_appels()
            for item in appels:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("lead_id", ""),
                    item.get("date_appel", ""),
                    item.get("canal", ""),
                    item.get("resultat", ""),
                    item.get("notes", ""),
                    item.get("prochain_rappel_at", ""),
                    item.get("dernier_rappel_at", ""),
                    item.get("nb_rappels_programmes", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des appels: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("lead_id"):
                messagebox.showerror("Erreur", "Lead ID est obligatoire")
                return
            
            # Convertir lead_id et nb_rappels_programmes en entier
            try:
                lead_id = int(data.get("lead_id"))
                nb_rappels = int(data.get("nb_rappels_programmes", 0))
            except ValueError:
                messagebox.showerror("Erreur", "Lead ID et nombre de rappels doivent être des nombres")
                return
            
            add_appel(
                lead_id=lead_id,
                date_appel=data.get("date_appel"),
                canal=data.get("canal", "tel"),
                resultat=data.get("resultat"),
                notes=data.get("notes"),
                prochain_rappel_at=data.get("prochain_rappel_at"),
                dernier_rappel_at=data.get("dernier_rappel_at"),
                nb_rappels_programmes=nb_rappels
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Appel ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un appel")
                return
            
            appel_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les types numériques
                if 'lead_id' in data and data['lead_id']:
                    try:
                        data['lead_id'] = int(data['lead_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Lead ID doit être un nombre")
                        return
                
                if 'nb_rappels_programmes' in data and data['nb_rappels_programmes']:
                    try:
                        data['nb_rappels_programmes'] = int(data['nb_rappels_programmes'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Nombre de rappels doit être un nombre")
                        return
                
                update_appel(appel_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Appel modifié avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un appel")
                return
            
            appel_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cet appel ?"):
                delete_appel(appel_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Appel supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class FormationsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Formations",
                         ("ID", "Nom", "Description", "Actif"),
                         ["nom", "description", "actif"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            formations = get_formations()
            for item in formations:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("nom", ""),
                    item.get("description", ""),
                    item.get("actif", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des formations: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("nom"):
                messagebox.showerror("Erreur", "Nom est obligatoire")
                return
            
            # Convertir actif en booléen
            actif = True
            if data.get("actif"):
                actif = data.get("actif").lower() in ['true', '1', 'oui', 'yes']
            
            add_formation(
                nom=data.get("nom"),
                description=data.get("description"),
                actif=actif
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Formation ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une formation")
                return
            
            formation_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir actif en booléen si fourni
                if 'actif' in data and data['actif']:
                    data['actif'] = data['actif'].lower() in ['true', '1', 'oui', 'yes']
                
                update_formation(formation_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Formation modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une formation")
                return
            
            formation_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette formation ?"):
                delete_formation(formation_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Formation supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class SessionsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Sessions",
                         ("ID", "Formation ID", "Nom Session", "Prix Base", "Date Début", "Date Fin", "Statut", "Coef Paiement"),
                         ["formation_id", "nom_session", "prix_base", "date_debut", "date_fin", "statut", "paiement_coef"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            sessions = get_sessions()
            for item in sessions:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("formation_id", ""),
                    item.get("nom_session", ""),
                    item.get("prix_base", ""),
                    item.get("date_debut", ""),
                    item.get("date_fin", ""),
                    item.get("statut", ""),
                    item.get("paiement_coef", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des sessions: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("formation_id") or not data.get("nom_session"):
                messagebox.showerror("Erreur", "Formation ID et nom session sont obligatoires")
                return
            
            # Convertir formation_id en entier
            try:
                formation_id = int(data.get("formation_id"))
            except ValueError:
                messagebox.showerror("Erreur", "Formation ID doit être un nombre")
                return
            
            # Convertir prix_base et paiement_coef en float si fournis
            prix_base = None
            paiement_coef = 37.5  # valeur par défaut
            
            if data.get("prix_base"):
                try:
                    prix_base = float(data.get("prix_base"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix doit être un nombre")
                    return
            
            if data.get("paiement_coef"):
                try:
                    paiement_coef = float(data.get("paiement_coef"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le coefficient de paiement doit être un nombre")
                    return
            
            add_session(
                formation_id=formation_id,
                nom_session=data.get("nom_session"),
                prix_base=prix_base,
                date_debut=data.get("date_debut"),
                date_fin=data.get("date_fin"),
                statut=data.get("statut", "planifiée"),
                paiement_coef=paiement_coef
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Session ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une session")
                return
            
            session_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les types si nécessaire
                if 'formation_id' in data and data['formation_id']:
                    try:
                        data['formation_id'] = int(data['formation_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Formation ID doit être un nombre")
                        return
                
                if 'prix_base' in data and data['prix_base']:
                    try:
                        data['prix_base'] = float(data['prix_base'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Le prix doit être un nombre")
                        return
                
                if 'paiement_coef' in data and data['paiement_coef']:
                    try:
                        data['paiement_coef'] = float(data['paiement_coef'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Le coefficient de paiement doit être un nombre")
                        return
                
                update_session(session_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Session modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une session")
                return
            
            session_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette session ?"):
                delete_session(session_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Session supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class SeancesFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Séances",
                         ("ID", "Session ID", "Type", "Date Début", "Date Fin", "Statut"),
                         ["session_id", "type", "date_debut", "date_fin", "statut"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            seances = get_seances()
            for item in seances:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("session_id", ""),
                    item.get("type", ""),
                    item.get("date_debut", ""),
                    item.get("date_fin", ""),
                    item.get("statut", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des séances: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("session_id"):
                messagebox.showerror("Erreur", "Session ID est obligatoire")
                return
            
            # Convertir session_id en entier
            try:
                session_id = int(data.get("session_id"))
            except ValueError:
                messagebox.showerror("Erreur", "Session ID doit être un nombre")
                return
            
            add_seance(
                session_id=session_id,
                type_seance=data.get("type", "cours"),
                date_debut=data.get("date_debut"),
                date_fin=data.get("date_fin"),
                statut=data.get("statut", "prévue")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Séance ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une séance")
                return
            
            seance_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Adapter les noms de champs et convertir les types
                if "type" in data:
                    data["type_seance"] = data.pop("type")
                
                if 'session_id' in data and data['session_id']:
                    try:
                        data['session_id'] = int(data['session_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Session ID doit être un nombre")
                        return
                
                update_seance(seance_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Séance modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une séance")
                return
            
            seance_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette séance ?"):
                delete_seance(seance_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Séance supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class InscriptionsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Inscriptions",
                         ("ID", "Lead ID", "Enfant ID", "Session ID", "Statut", "Date", "Prix Négocié", "Remise"),
                         ["lead_id", "enfant_id", "session_id", "statut", "date_inscription", "prix_negocie", "remise_total"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            inscriptions = get_inscriptions()
            for item in inscriptions:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("lead_id", ""),
                    item.get("enfant_id", ""),
                    item.get("session_id", ""),
                    item.get("statut", ""),
                    item.get("date_inscription", ""),
                    item.get("prix_negocie", ""),
                    item.get("remise_total", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des inscriptions: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("lead_id") or not data.get("session_id"):
                messagebox.showerror("Erreur", "Lead ID et Session ID sont obligatoires")
                return
            
            # Convertir les IDs en entiers
            try:
                lead_id = int(data.get("lead_id"))
                session_id = int(data.get("session_id"))
                enfant_id = int(data.get("enfant_id")) if data.get("enfant_id") else None
            except ValueError:
                messagebox.showerror("Erreur", "Les IDs doivent être des nombres")
                return
            
            # Convertir prix_negocie et remise_total en float si fournis
            prix_negocie = None
            remise_total = None
            
            if data.get("prix_negocie"):
                try:
                    prix_negocie = float(data.get("prix_negocie"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix négocié doit être un nombre")
                    return
            
            if data.get("remise_total"):
                try:
                    remise_total = float(data.get("remise_total"))
                except ValueError:
                    messagebox.showerror("Erreur", "La remise doit être un nombre")
                    return
            
            add_inscription(
                lead_id=lead_id,
                enfant_id=enfant_id,
                session_id=session_id,
                statut=data.get("statut", "preinscrit"),
                date_inscription=data.get("date_inscription"),
                prix_negocie=prix_negocie,
                remise_total=remise_total
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Inscription ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une inscription")
                return
            
            inscription_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les IDs en entiers si fournis
                for field in ['lead_id', 'enfant_id', 'session_id']:
                    if field in data and data[field]:
                        try:
                            data[field] = int(data[field])
                        except ValueError:
                            messagebox.showerror("Erreur", f"{field} doit être un nombre")
                            return
                
                # Convertir les montants en float si fournis
                for field in ['prix_negocie', 'remise_total']:
                    if field in data and data[field]:
                        try:
                            data[field] = float(data[field])
                        except ValueError:
                            messagebox.showerror("Erreur", f"{field} doit être un nombre")
                            return
                
                update_inscription(inscription_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Inscription modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une inscription")
                return
            
            inscription_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette inscription ?"):
                delete_inscription(inscription_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Inscription supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class FacturesFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Factures",
                         ("ID", "Inscription ID", "Numéro", "Date Émission", "Total HT", "Total Taxes", "Total TTC", "Statut"),
                         ["inscription_id", "numero", "date_emission", "total_ht", "total_taxes", "total_ttc", "statut"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            factures = get_factures()
            for item in factures:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("inscription_id", ""),
                    item.get("numero", ""),
                    item.get("date_emission", ""),
                    item.get("total_ht", ""),
                    item.get("total_taxes", ""),
                    item.get("total_ttc", ""),
                    item.get("statut", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des factures: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("inscription_id") or not data.get("numero"):
                messagebox.showerror("Erreur", "Inscription ID et numéro sont obligatoires")
                return
            
            # Convertir inscription_id en entier
            try:
                inscription_id = int(data.get("inscription_id"))
            except ValueError:
                messagebox.showerror("Erreur", "Inscription ID doit être un nombre")
                return
            
            # Convertir les montants en float si fournis
            total_ht = None
            total_taxes = None
            total_ttc = None
            
            if data.get("total_ht"):
                try:
                    total_ht = float(data.get("total_ht"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le total HT doit être un nombre")
                    return
            
            if data.get("total_taxes"):
                try:
                    total_taxes = float(data.get("total_taxes"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le total taxes doit être un nombre")
                    return
            
            if data.get("total_ttc"):
                try:
                    total_ttc = float(data.get("total_ttc"))
                except ValueError:
                    messagebox.showerror("Erreur", "Le total TTC doit être un nombre")
                    return
            
            add_facture(
                inscription_id=inscription_id,
                numero=data.get("numero"),
                date_emission=data.get("date_emission"),
                total_ht=total_ht,
                total_taxes=total_taxes,
                total_ttc=total_ttc,
                statut=data.get("statut", "brouillon")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Facture ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une facture")
                return
            
            facture_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les types si nécessaire
                if 'inscription_id' in data and data['inscription_id']:
                    try:
                        data['inscription_id'] = int(data['inscription_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Inscription ID doit être un nombre")
                        return
                
                for field in ['total_ht', 'total_taxes', 'total_ttc']:
                    if field in data and data[field]:
                        try:
                            data[field] = float(data[field])
                        except ValueError:
                            messagebox.showerror("Erreur", f"Le {field} doit être un nombre")
                            return
                
                update_facture(facture_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Facture modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une facture")
                return
            
            facture_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette facture ?"):
                delete_facture(facture_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Facture supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class EcheancesFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Échéances",
                         ("ID", "Facture ID", "Libellé", "Montant", "Date Échéance", "Date Tolérance", "Statut"),
                         ["facture_id", "libelle", "montant_du", "date_echeance", "date_tolerance", "statut"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            echeances = get_echeances()
            for item in echeances:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("facture_id", ""),
                    item.get("libelle", ""),
                    item.get("montant_du", ""),
                    item.get("date_echeance", ""),
                    item.get("date_tolerance", ""),
                    item.get("statut", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des échéances: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("facture_id") or not data.get("montant_du"):
                messagebox.showerror("Erreur", "Facture ID et montant sont obligatoires")
                return
            
            # Convertir facture_id en entier et montant_du en float
            try:
                facture_id = int(data.get("facture_id"))
                montant_du = float(data.get("montant_du"))
            except ValueError:
                messagebox.showerror("Erreur", "Facture ID doit être un nombre et montant doit être un nombre décimal")
                return
            
            add_echeance(
                facture_id=facture_id,
                libelle=data.get("libelle"),
                montant_du=montant_du,
                date_echeance=data.get("date_echeance"),
                date_tolerance=data.get("date_tolerance"),
                statut=data.get("statut", "du")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Échéance ajoutée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une échéance")
                return
            
            echeance_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les types si nécessaire
                if 'facture_id' in data and data['facture_id']:
                    try:
                        data['facture_id'] = int(data['facture_id'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Facture ID doit être un nombre")
                        return
                
                if 'montant_du' in data and data['montant_du']:
                    try:
                        data['montant_du'] = float(data['montant_du'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Le montant doit être un nombre")
                        return
                
                update_echeance(echeance_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Échéance modifiée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner une échéance")
                return
            
            echeance_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette échéance ?"):
                delete_echeance(echeance_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Échéance supprimée avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class PaiementsFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Paiements",
                         ("ID", "Inscription ID", "Facture ID", "Échéance ID", "Date", "Montant", "Moyen", "Statut", "Encaissé Par", "Justificatif", "Commentaire"),
                         ["inscription_id", "facture_id", "echeance_id", "date_paiement", "montant", "moyen", "statut", "encaisse_par", "justificatif_url", "commentaire"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            paiements = get_paiements()
            for item in paiements:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("inscription_id", ""),
                    item.get("facture_id", ""),
                    item.get("echeance_id", ""),
                    item.get("date_paiement", ""),
                    item.get("montant", ""),
                    item.get("moyen", ""),
                    item.get("statut", ""),
                    item.get("encaisse_par", ""),
                    item.get("justificatif_url", ""),
                    item.get("commentaire", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des paiements: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("montant"):
                messagebox.showerror("Erreur", "Montant est obligatoire")
                return
            
            # Convertir les types
            try:
                montant = float(data.get("montant"))
                inscription_id = int(data.get("inscription_id")) if data.get("inscription_id") else None
                facture_id = int(data.get("facture_id")) if data.get("facture_id") else None
                echeance_id = int(data.get("echeance_id")) if data.get("echeance_id") else None
            except ValueError:
                messagebox.showerror("Erreur", "Les IDs doivent être des nombres et le montant un nombre décimal")
                return
            
            add_paiement(
                inscription_id=inscription_id,
                facture_id=facture_id,
                echeance_id=echeance_id,
                date_paiement=data.get("date_paiement"),
                montant=montant,
                moyen=data.get("moyen"),
                statut=data.get("statut", "en_attente"),
                encaisse_par=data.get("encaisse_par"),
                justificatif_url=data.get("justificatif_url"),
                commentaire=data.get("commentaire")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Paiement ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un paiement")
                return
            
            paiement_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                # Convertir les types si nécessaire
                for field in ['inscription_id', 'facture_id', 'echeance_id']:
                    if field in data and data[field]:
                        try:
                            data[field] = int(data[field])
                        except ValueError:
                            messagebox.showerror("Erreur", f"{field} doit être un nombre")
                            return
                
                if 'montant' in data and data['montant']:
                    try:
                        data['montant'] = float(data['montant'])
                    except ValueError:
                        messagebox.showerror("Erreur", "Le montant doit être un nombre")
                        return
                
                update_paiement(paiement_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Paiement modifié avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un paiement")
                return
            
            paiement_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer ce paiement ?"):
                delete_paiement(paiement_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Paiement supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


class FormateursFrame(BaseCRUDFrame):
    def __init__(self, parent):
        super().__init__(parent, "Formateurs",
                         ("ID", "Nom", "Prénom", "Téléphone", "Email", "Date Arrivée", "Date Départ", "Disponibilités", "Statut"),
                         ["nom", "prenom", "telephone", "email", "date_arrivee", "date_depart", "disponibilites", "statut"])

    def load_data(self):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)
            formateurs = get_formateurs()
            for item in formateurs:
                self.tree.insert("", "end", values=[
                    item.get("id", ""),
                    item.get("nom", ""),
                    item.get("prenom", ""),
                    item.get("telephone", ""),
                    item.get("email", ""),
                    item.get("date_arrivee", ""),
                    item.get("date_depart", ""),
                    item.get("disponibilites", ""),
                    item.get("statut", "")
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des formateurs: {str(e)}")

    def add_item(self):
        try:
            data = self.get_form_data()
            if not data.get("nom") or not data.get("prenom"):
                messagebox.showerror("Erreur", "Nom et prénom sont obligatoires")
                return
            
            add_formateur(
                nom=data.get("nom"),
                prenom=data.get("prenom"),
                telephone=data.get("telephone"),
                email=data.get("email"),
                date_arrivee=data.get("date_arrivee"),
                date_depart=data.get("date_depart"),
                disponibilites=data.get("disponibilites"),
                statut=data.get("statut", "actif")
            )
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Succès", "Formateur ajouté avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")

    def update_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un formateur")
                return
            
            formateur_id = self.tree.item(selected[0])["values"][0]
            data = self.get_form_data()
            
            if data:
                update_formateur(formateur_id, **data)
                self.load_data()
                messagebox.showinfo("Succès", "Formateur modifié avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def delete_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Veuillez sélectionner un formateur")
                return
            
            formateur_id = self.tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer ce formateur ?"):
                delete_formateur(formateur_id)
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Succès", "Formateur supprimé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")


# ===== LANCER L'APPLICATION =====
if __name__ == "__main__":
    app = InterfaceRC()
    app.mainloop()