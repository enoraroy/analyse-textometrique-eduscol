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
    root = ET.Element(chaine, matiere="", classe="", annee="2015", nomfichier = filename)

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
    
    dico_pattern = {r'\.{3,}' : '..',
                    r"</Span><Span>" : "",
                    r"<Span> </Span>": "",
                    r"<Span> </Span>" : "",
                    r"<Span> </Span>" : "",
                    r"</Block><Block>" : "",
                    r"<Line><Span>" : "<Line>",
                    r"</Span></Line>" : "</Line>",
                    r"<Block><Line>" : "<Line>",
                    r"</Line></Block>" : "</Line>",
                    r"<Line> </Line>" : "",
                    r"<Line></Line>" : "",
                    r"<Line>M</Line><Line>" : r"<Line>M",
                    r"<Line>Ministère de l’Éducation nationale(.*?)</Line>" : "",
                    r"<Line>Ministère de l’éducation nationale(.*?)</Line>" : "",
                    r"<Line>(.*?)DGESCO(.*?)</Line>" : "",
                    r"<Line>&gt; www.Éduscol.education.fr/prog </Line>" : "",
                    r"<Line>Page(.*?)</Line>" : "",
                    r"<Line>Bureau(.*?)</Line>" : "",
                    r"'uvre" : "'oeuvre",
                    r"’uvre" : "’oeuvre",
                    r">uvre" : ">oeuvre",
                    r" uvre" : " oeuvre",
                    r"<Line>&gt; Éduscol.education.fr/prog </Line>" : "",
                    r"<Line>Histoire-géographie </Line>" : "",
                    r"<Line>éducation civique </Line>" : "",
                    r"<Line>BO spécial(.*?)</Line>" : "",
                    r"<Line>juillet 2011 </Line>" : "",
                    r"<Line>août 2010 </Line>" : "",
                    r"<Line>Février 2011 </Line>" : "",
                    r"<Line>avril 2014 </Line>" : "",
                    r"<Line>Septembre 2015</Line>" : "",
                    r"<Line>octobre 2010 </Line>" : "",
                    r"<Line>http://Éduscol.education.fr </Line>" : "",
                    r"<Line>éduscol</Line>": "",
                    r"<Line>(juillet 2011) </Line>" : "",
                    r"<Line>Éduscol</Line>" : "",
                    r"<Line>Histoire\s{2,}Géographie(.*?)</Line>" : "",
                    r"<Line> </Line>" : "",
                    r"<Line>Ressources pour faire(.*?)</Line>" : "",
                    r"<Line>Histoire - Géographie(.*?)</Line>" : "",
                    r"<Line>(.?)</Line>" : "", #ligne 6354
                    r"<Line>(.2?)</Line>" : "",
                    r"<Line>(.*?)Éduscol(.*?)</Line>" : "",
                    r"<Line>(.*?)éduscol(.*?)</Line>" : "",
                    r"<Line>- </Line>" : "",
                    r"<Line>(.*?)DNB </Line>" : "",
                    r"<Line>\s{2,}</Line>" : "",
                    r"<Line>.?. </Line>" : "",
                    }
    
    for key, val in dico_pattern.items():
        xml_string = re.sub(key, val, xml_string, flags=re.MULTILINE | re.DOTALL)

    # Ajouter une indentation au fichier XML
    #pretty_xml = prettify_xml(ET.fromstring(xml_string))
    pretty_xml = xml_string
    
    if filename=="College_Ressources_HGEC_5_Hist_08_BouleversementsCultetIntellectuels_152639.pdf":
        textometrie = pretty_xml
    
    # Sauvegarder le fichier XML avec indentation
    with open(xml_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)

number = "2015"        
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

# --------------------------------------------------------------------------
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def remove_empty_lines(text):
    """Remove empty lines from a text string."""
    return "\n".join(line for line in text.split("\n") if line.strip())

def simplify_line_elements(element):
    """Simplify <Line><Span>...</Span></Line> to <Line>...</Line> and replace empty <Line> with <Line/>."""
    for line in element.findall('.//Line'):
        spans = list(line.findall('Span'))
        if len(spans) == 1:
            # Replace <Line><Span>text</Span></Line> with <Line>text</Line>
            line.text = spans[0].text
            line.remove(spans[0])
        elif not line.text and not list(line):
            # Replace empty <Line> with <Line/>
            line.clear()

def combine_xml_files(directory_path, output_path):
    # Créer l'élément racine pour le fichier XML combiné
    root = ET.Element("CombinedDocument")

    # Parcourir tous les fichiers du répertoire
    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            #print(filename)
            file_path = os.path.join(directory_path, filename)

            # Analyser le fichier XML
            tree = ET.parse(file_path)
            file_root = tree.getroot()

            # Simplifier les éléments <Line>
            simplify_line_elements(file_root)

            # Ajouter le contenu du fichier XML à l'élément racine du fichier combiné
            root.append(file_root)

    # Convertir l'arbre XML combiné en chaîne
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Supprimer les lignes vides inutiles
    pretty_xml = remove_empty_lines(pretty_xml)

    # Sauvegarder le fichier XML combiné avec indentation
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)

# Chemin vers le dossier contenant les fichiers XML et le fichier XML de sortie
number = '2015'
directory_path = "ressources" + number
output_path = "out" + number + ".xml"

# Combiner les fichiers XML
combine_xml_files(directory_path, output_path)
