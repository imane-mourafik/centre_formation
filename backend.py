import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

# ===================================
# Connexion à la base de données
# ===================================
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="centre_formation"
        )
    except Error as err:
        print("Erreur DB:", err)
        return None

# ===================================
# USERS
# ===================================
def get_user(username, hashed_password):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=%s AND password_hash=%s", (username, hashed_password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_user(username, hashed_password, role):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username,password_hash,role,created_at) VALUES (%s,%s,%s,%s)",
                       (username, hashed_password, role, datetime.now()))
        conn.commit()
        conn.close()

def update_user(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k, v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_user(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# LEADS
# ===================================
def get_leads():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM leads")
        result = cursor.fetchall()
        conn.close()
    return result

def add_lead(nom, prenom, telephone, whatsapp_url=None, disponibilites=None,
             statut_pipeline="nouveau", source=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leads 
            (nom, prenom, telephone, whatsapp_url, disponibilites, statut_pipeline, source, created_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nom, prenom, telephone, whatsapp_url, disponibilites, statut_pipeline, source, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()

def update_lead(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE leads SET {', '.join(updates)}, updated_at=%s WHERE id=%s"
        values.insert(-1, datetime.now())
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_lead(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leads WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# ENFANTS
# ===================================
def get_enfants():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM enfants")
        result = cursor.fetchall()
        conn.close()
    return result

def add_enfant(parent_id, nom, prenom, date_naissance=None, num_tel_papa=None,
               num_tel_maman=None, num_tel_enfant=None, sexe=None, niveau_scolaire=None,
               niveau_avant_centre=False, sessions_realisees=None, remarques=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO enfants
            (parent_id, nom, prenom, date_naissance, num_tel_papa, num_tel_maman,
            num_tel_enfant, sexe, niveau_scolaire, niveau_avant_centre, sessions_realisees,
            remarques, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (parent_id, nom, prenom, date_naissance, num_tel_papa, num_tel_maman,
              num_tel_enfant, sexe, niveau_scolaire, niveau_avant_centre,
              json.dumps(sessions_realisees or []), remarques, datetime.now()))
        conn.commit()
        conn.close()

def update_enfant(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            if k=="sessions_realisees" and v is not None:
                v = json.dumps(v)
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE enfants SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_enfant(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enfants WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# APPELS
# ===================================
def get_appels():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appels")
        result = cursor.fetchall()
        conn.close()
    return result

def add_appel(lead_id, date_appel=None, canal="tel", resultat=None, notes=None,
              prochain_rappel_at=None, dernier_rappel_at=None, nb_rappels_programmes=0):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appels
            (lead_id, date_appel, canal, resultat, notes, prochain_rappel_at,
            dernier_rappel_at, nb_rappels_programmes, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (lead_id, date_appel, canal, resultat, notes, prochain_rappel_at,
              dernier_rappel_at, nb_rappels_programmes, datetime.now()))
        conn.commit()
        conn.close()

def update_appel(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE appels SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_appel(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appels WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# FORMATIONS
# ===================================
def get_formations():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM formations")
        result = cursor.fetchall()
        conn.close()
    return result

def add_formation(nom, description, actif=True):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO formations (nom, description, actif, created_at) 
            VALUES (%s,%s,%s,%s)
        """, (nom, description, actif, datetime.now()))
        conn.commit()
        conn.close()

def update_formation(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE formations SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_formation(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM formations WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# SESSIONS
# ===================================
def get_sessions():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sessions")
        result = cursor.fetchall()
        conn.close()
    return result

def add_session(formation_id, nom_session, prix_base=None, date_debut=None, date_fin=None,
                statut="planifiée", paiement_coef=37.5, seances_realisees=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions
            (formation_id, nom_session, prix_base, date_debut, date_fin, statut, paiement_coef, seances_realisees, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (formation_id, nom_session, prix_base, date_debut, date_fin, statut, paiement_coef,
              json.dumps(seances_realisees or []), datetime.now()))
        conn.commit()
        conn.close()

def update_session(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            if k=="seances_realisees" and v is not None:
                v = json.dumps(v)
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE sessions SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_session(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# SEANCES
# ===================================
def get_seances():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM seances")
        result = cursor.fetchall()
        conn.close()
    return result

def add_seance(session_id, type_seance="cours", date_debut=None, date_fin=None, statut="prévue"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO seances (session_id, type, date_debut, date_fin, statut, created_at)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (session_id, type_seance, date_debut, date_fin, statut, datetime.now()))
        conn.commit()
        conn.close()

def update_seance(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE seances SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_seance(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM seances WHERE id=%s", (id,))
        conn.commit()
        conn.close()
# ===================================
# INSCRIPTIONS
# ===================================
def get_inscriptions():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inscriptions")
        result = cursor.fetchall()
        conn.close()
    return result

def add_inscription(lead_id, enfant_id, session_id, statut="preinscrit",
                    date_inscription=None, prix_negocie=None, remise_total=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inscriptions
            (lead_id, enfant_id, session_id, statut, date_inscription, prix_negocie, remise_total, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (lead_id, enfant_id, session_id, statut, date_inscription, prix_negocie, remise_total, datetime.now()))
        conn.commit()
        conn.close()

def update_inscription(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE inscriptions SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_inscription(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inscriptions WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# FACTURES
# ===================================
def get_factures():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM factures")
        result = cursor.fetchall()
        conn.close()
    return result

def add_facture(inscription_id, numero, date_emission=None, total_ht=None,
                total_taxes=None, total_ttc=None, statut="brouillon"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factures
            (inscription_id, numero, date_emission, total_ht, total_taxes, total_ttc, statut, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (inscription_id, numero, date_emission, total_ht, total_taxes, total_ttc, statut, datetime.now()))
        conn.commit()
        conn.close()

def update_facture(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE factures SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_facture(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM factures WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# ECHEANCES
# ===================================
def get_echeances():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM echeances")
        result = cursor.fetchall()
        conn.close()
    return result

def add_echeance(facture_id, libelle, montant_du, date_echeance, date_tolerance=None,
                 statut="du"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO echeances
            (facture_id, libelle, montant_du, date_echeance, date_tolerance, statut, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (facture_id, libelle, montant_du, date_echeance, date_tolerance, statut, datetime.now()))
        conn.commit()
        conn.close()

def update_echeance(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE echeances SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_echeance(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM echeances WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# PAIEMENTS
# ===================================
def get_paiements():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM paiements")
        result = cursor.fetchall()
        conn.close()
    return result

def add_paiement(inscription_id=None, facture_id=None, echeance_id=None,
                 date_paiement=None, montant=None, moyen=None, statut="en_attente",
                 encaisse_par=None, justificatif_url=None, commentaire=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO paiements
            (inscription_id, facture_id, echeance_id, date_paiement, montant, moyen, statut,
            encaisse_par, justificatif_url, commentaire, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (inscription_id, facture_id, echeance_id, date_paiement, montant, moyen, statut,
              encaisse_par, justificatif_url, commentaire, datetime.now()))
        conn.commit()
        conn.close()

def update_paiement(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE paiements SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_paiement(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paiements WHERE id=%s", (id,))
        conn.commit()
        conn.close()

# ===================================
# FORMATEURS
# ===================================
def get_formateurs():
    conn = get_connection()
    result=[]
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM formateurs")
        result = cursor.fetchall()
        conn.close()
    return result

def add_formateur(nom, prenom, telephone=None, email=None, date_arrivee=None,
                  date_depart=None, disponibilites=None, statut="actif"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO formateurs
            (nom, prenom, telephone, email, date_arrivee, date_depart, disponibilites, statut, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nom, prenom, telephone, email, date_arrivee, date_depart, disponibilites, statut, datetime.now()))
        conn.commit()
        conn.close()

def update_formateur(id, **kwargs):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        updates, values = [], []
        for k,v in kwargs.items():
            updates.append(f"{k}=%s")
            values.append(v)
        values.append(id)
        sql = f"UPDATE formateurs SET {', '.join(updates)} WHERE id=%s"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def delete_formateur(id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM formateurs WHERE id=%s", (id,))
        conn.commit()
        conn.close()
