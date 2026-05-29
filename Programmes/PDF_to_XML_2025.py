import fitz  # PyMuPDF
import xml.etree.ElementTree as ET
from xml.dom import minidom
#import html
import re
import os

textometrie = 0

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def escape_text(text):
    """Escape special characters in text for XML and remove non-printable characters."""
    # Remove non-printable characters, but keep apostrophes (both straight and typographic) and 'Œ'
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\xA0-\xFFFD\'\’Œ]', '', text)
    return text #html.escape(text)

def pdf_to_xml(pdf_path, xml_path,filename):
    global textometrie    
    # Ouvrir le fichier PDF
    document = fitz.open(pdf_path)
    chaine = "Document"
    root = ET.Element(chaine, matiere="histoire", classe="3", annee="2025", nomfichier = filename)

    # Parcourir chaque page du PDF
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        page_element = ET.SubElement(root, "Page", number=str(page_num + 1))

        # Extraire le texte de la page
        text = page.get_text("dict")
        blocks = text["blocks"]

        # Parcourir chaque bloc de texte
        for block in blocks:
            block_element = ET.SubElement(page_element, "Block")

            # Vérifier si le bloc contient des lignes
            if "lines" in block:
                # Parcourir chaque ligne dans le bloc
                for line in block["lines"]:
                    line_element = ET.SubElement(block_element, "Line")

                    # Parcourir chaque span dans la ligne
                    spans = line["spans"]
                    if len(spans) == 1:
                        # Si une seule span, ajouter directement le texte à la ligne
                        span_text = escape_text(spans[0]["text"])
                        if span_text:
                            line_element.text = span_text
                    else:
                        # Sinon, ajouter chaque span comme sous-élément
                        for span in spans:
                            span_text = escape_text(span["text"])
                            if span_text:
                                span_element = ET.SubElement(line_element, "Span")
                                span_element.text = span_text

                    # Supprimer les éléments <Line> vides
                    if not line_element.text and not list(line_element):
                        block_element.remove(line_element)

            # Supprimer les éléments <Block> vides
            if not block_element.text and not list(block_element):
                page_element.remove(block_element)

    # Convertir l'arbre XML en chaîne
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    xml_string = reparsed.toxml()
    
    # Supprimer les occurrences de "</Span><Span>"
    for val in ["</Span><Span>", "<Span> </Span>", "<Span> </Span>", "<Span> </Span>", "</Block><Block>"]:
        xml_string = xml_string.replace(val, "")

    # Ajouter une indentation au fichier XML
    pretty_xml = prettify_xml(ET.fromstring(xml_string))
    
    pretty_xml = re.sub(r"<Block>(.*?)sur</Line>", "", pretty_xml, flags=re.DOTALL)
    
    pretty_xml = re.sub(r"</Block>", "\n", pretty_xml, flags=re.DOTALL)
    
    pretty_xml = re.sub(r'\n\s{2,}<Line/>\n', '\n', pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"<Line>4</Line>", "",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"<Line>\n\s{2,}<Span>", "<Line>",pretty_xml,flags=re.DOTALL)

    pretty_xml = re.sub(r"</Span>\n\s{2,}</Line>", "</Line>",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"\n\s{2,}<Line>\s{1,}</Line>\n", "\n",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r" uvre ", " oeuvre ",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"</Line>\n\s{2,}<Line>’", "'",pretty_xml,flags=re.DOTALL)
        
   # Expression régulière pour extraire les informations
    match = re.search(r"<Line>(\w+) / classe de (\w+)</Line>", pretty_xml)
    
    if match:
        chaine_matiere = ' matiere="' + match.group(1) + '"'
        pretty_xml = re.sub(r' matiere="histoire"', chaine_matiere, pretty_xml, flags=re.DOTALL)
        chaine_classe = ' classe="' + match.group(2)+'"'
        pretty_xml = re.sub(r' classe="3"', chaine_classe, pretty_xml, flags=re.DOTALL)
    else:
        print("Aucune correspondance trouvée.")
        print(filename)

    pretty_xml = re.sub(r"<Line>(.*?) / classe de (.*?)</Line>", "\n",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"\n\s{2,}\n", "\n",pretty_xml,flags=re.DOTALL)
    
    pretty_xml = re.sub(r"\n\s{2,}<Line>Extrait du programme.*?\n", "\n", pretty_xml, flags=re.MULTILINE | re.DOTALL)
    
    pretty_xml = re.sub(r"<Line>-</Line>", "",pretty_xml,flags=re.DOTALL) 
    
    pretty_xml = re.sub(r'\.{3,}', '..',pretty_xml,flags=re.DOTALL) 
    
    pretty_xml = re.sub(r'\n</Line>\n', '</Line>\n',pretty_xml,flags=re.DOTALL)
    
    textometrie = pretty_xml
    
    # Sauvegarder le fichier XML avec indentation
    with open(xml_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)

number = "2025"        
input_directory = "ressources" + number
liste_fichier = os.listdir(input_directory)
compteur = 0
# Lire tous les fichiers PDF dans le répertoire "ressources"
for filename in liste_fichier:
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_directory, filename)
        # # Convertir le PDF en XML
        xml_path = pdf_path[:-4]+".xml"
        try:
            xml_tree = pdf_to_xml(pdf_path, xml_path,filename)
            compteur += 1
            # pb avec 
            #College_Ressources_HGEC_4_Hist_12_AffirmNationalismes_187669.pdf
            #MuPDF error: format error: No default Layer config
            #College_Ressources_HGEC_4_Geo_04_LieuxCommand_187683.pdf
        except:
            print("**********",filename)
            
print('\n nombre de fichier traité : ',compteur)
