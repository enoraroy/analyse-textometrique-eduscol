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
            print(filename)
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
