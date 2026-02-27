"""Interface Streamlit pour l'extraction de documents non structurés."""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from src.extractors import extract_document
from src.models import Invoice, Order

# Configuration de la page
st.set_page_config(
    page_title="NAF_ISB - Extracteur de Documents",
    page_icon="📄",
    layout="wide"
)

# Titre et description
st.title("📄 NAF_ISB - Extracteur de Documents Structurés")
st.markdown("""
Cette application extrait automatiquement les données structurées depuis vos documents 
(factures, commandes, bons de commande) en utilisant l'IA générative.

**Formats supportés :** PDF, Word (DOCX), Texte (TXT), Excel (XLSX, XLS), CSV
""")

# Barre latérale avec informations
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    **Types de documents supportés :**
    - 📋 Factures (Invoices)
    - 📦 Commandes (Orders)
    - 🛒 Bons de commande (Purchase Orders)
    
    **Formats acceptés :**
    - 📝 PDF, Word (DOCX), TXT
    -  Excel (XLSX, XLS), CSV
    
    **Comment ça marche ?**
    1. Uploadez un ou plusieurs fichiers
    2. L'IA détecte le type de document
    3. Les données sont extraites automatiquement
    4. Téléchargez le résultat en JSON
    """)
    
    st.divider()
    st.caption("Projet MSBNS3IN03 - IA Générative")

# Zone d'upload de fichiers
uploaded_files = st.file_uploader(
    "📤 Glissez-déposez vos fichiers ici",
    type=["pdf", "docx", "txt", "text", "xlsx", "xls", "csv"],
    accept_multiple_files=True,
    help="Vous pouvez uploader plusieurs fichiers de différents formats à la fois"
)

# Traitement des fichiers uploadés
if uploaded_files:
    st.divider()
    
    # Affichage du nombre de fichiers
    st.subheader(f"📊 {len(uploaded_files)} fichier(s) à traiter")
    
    # Création de colonnes pour afficher les résultats
    for idx, uploaded_file in enumerate(uploaded_files):
        with st.expander(f"📄 {uploaded_file.name}", expanded=True):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 🔍 Traitement")
                
                # Déterminer le suffix du fichier
                file_suffix = Path(uploaded_file.name).suffix
                
                # Créer un fichier temporaire avec le bon suffix
                with NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = Path(tmp_file.name)
                
                try:
                    # Afficher un spinner pendant le traitement
                    with st.spinner(f"Analyse de {uploaded_file.name}..."):
                        # Extraction du document
                        document = extract_document(tmp_path)
                        
                        # Afficher le type détecté
                        doc_type = document.document_type
                        
                        # Icône selon le type
                        icon = {
                            "Invoice": "📋",
                            "Order": "📦",
                            "Purchase Order": "🛒"
                        }.get(doc_type, "📄")
                        
                        st.success(f"{icon} **Type détecté :** {doc_type}")
                        
                        # Informations supplémentaires selon le type
                        if isinstance(document, Invoice):
                            if document.total:
                                st.metric("💰 Montant total", f"{document.total} {document.currency or ''}")
                            if document.invoice_date:
                                st.info(f"📅 Date : {document.invoice_date}")
                            if document.seller and document.seller.name:
                                st.info(f"🏢 Vendeur : {document.seller.name}")
                        elif isinstance(document, Order):
                            if document.total_price:
                                st.metric("💰 Montant total", f"{document.total_price} {document.currency or ''}")
                            if document.order_date:
                                st.info(f"📅 Date : {document.order_date}")
                            if document.customer_name:
                                st.info(f"👤 Client : {document.customer_name}")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors du traitement : {str(e)}")
                    document = None
                finally:
                    # Nettoyer le fichier temporaire
                    tmp_path.unlink(missing_ok=True)
            
            with col2:
                st.markdown("### 📋 Données extraites (JSON)")
                
                if document:
                    # Convertir en JSON
                    json_data = document.model_dump(mode="json")
                    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
                    
                    # Afficher le JSON dans une zone de code
                    st.code(json_str, language="json", line_numbers=True)
                    
                    # Bouton de téléchargement
                    filename = Path(uploaded_file.name).stem + '.json'
                    st.download_button(
                        label=f"⬇️ Télécharger {filename}",
                        data=json_str,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )
        
        # Séparateur entre fichiers
        if idx < len(uploaded_files) - 1:
            st.divider()

else:
    # Message d'accueil si aucun fichier n'est uploadé
    st.info("👆 Commencez par uploader un ou plusieurs fichiers ci-dessus")
    
    # Exemple visuel
    st.markdown("### 💡 Exemple de résultat")
    st.markdown("""
    Après l'upload d'une facture, vous obtiendrez un JSON structuré contenant :
    - Type de document
    - Informations du fournisseur
    - Date de la facture
    - Montant total (TTC, HT, TVA)
    - Lignes de facturation détaillées
    - Et bien plus...
    """)

# Footer
st.divider()
st.caption("💻 Développé avec Streamlit + OpenAI | NAF & ISB © 2026")
