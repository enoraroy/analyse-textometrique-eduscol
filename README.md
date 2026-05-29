# Projet Textométrique : Analyse des Fiches Éduscol d'Histoire-Géographie-EMC (Cycle 4)

## Description du Projet
Ce projet a été réalisé dans le cadre d'un TD d'histoire et informatique, consacré à l'analyse de données textuelles. Il propose une étude lexicométrique et textométrique du discours institutionnel de l'État à travers le prisme des fiches Éduscol (ressources d'accompagnement des programmes) destinées aux enseignants d'Histoire-Géographie et d'Enseignement Moral et Civique (EMC) au cycle 4 (classes de 5ème, 4ème et 3ème) en France métropolitaine.  L'analyse interroge le « changement dans l'École » (au sens d'Antoine Prost) en comparant les fiches de **2015** et de **2025** (qui reflètent respectivement les programmes de 2011 et de 2016). L'objectif est de saisir dans quelle mesure ces fiches traduisent les transformations des attentes pédagogiques et didactiques imposées par l'État et comment s'articule la tension entre uniformisation nationale et liberté pédagogique.
Cette initiation à la recherche a été réalisée entre mars 2025 et juin 2025.

---

## Structure du Corpus
Le corpus d'étude rassemble **79 fichiers** (fiches Éduscol officielles téléchargées directement ou récupérées via *Internet Archive* pour les éditions antérieures). Il se caractérise par les indicateurs textométriques suivants :
* **Occurrences totales** : 176 467 mots
* **Formes distinctes** : 13 370
* **Lemmes** : 8 093 (indiquant une variété lexicale concentrée de 0.05%)
* **Hapax** : 3 492
* **Masse textuelle par discipline** :
  * **EMC** : ~69 500 occurrences (discipline la plus volumineuse en 2025 en raison de la transversalité des fiches)
  * **Histoire** : ~58 560 occurrences
  * **Géographie** : ~48 407 occurrences

---

## Pipeline Technologique & Traitement des Données
Pour automatiser la structuration et l'intégration de ce corpus volumineux dans les logiciels de textométrie (comme **TXM**), un script **Python** sur-mesure a été développé (partiellement assisté par *MistralAI* pour l'ébauche initiale).

### Fonctionnalités majeures du script Python :
1. **Extraction PDF-to-Text** : Exploitation de la bibliothèque `PyMuPDF` (`import fitz`) pour extraire finement le texte par blocs, pages et spans de caractères.
2. **Balisage XML Hiérarchique** : Génération d'une arborescence XML structurée autour des balises `<Document>`, `<Page>`, `<Block>`, `<Line>` et `<Span>`.
3. **Enrichissement par Métadonnées** : Tagging automatique de chaque document avec des attributs sociolinguistiques essentiels pour les partitions : `matiere`, `classe`, `annee` et `nomfichier`.
4. **Nettoyage Automatique & Normalisation (Regex)** : 
   * Suppression des scories institutionnelles répétitives (ex: *"Ministère de l'Éducation nationale..."*, mentions de la *DGESCO*, numéros de page, adresses URL).
   * Correction des ruptures typographiques et encodages problématiques (ex: regroupement des ligatures comme la forme `œuvre` cassée à la conversion, uniformisation des apostrophes droites `'` et typographiques `’`).

---

## Méthodes d'Analyse Textométrique
Le dossier s'appuie sur plusieurs outils de la statistique textuelle :
* **Analyse Factorielle des Correspondances (AFC)** : Visualisation des plans factoriels selon les partitions `classematiereannee`, `classeannee` et `classe` afin d'identifier les axes majeurs de contrastes linguistiques (par exemple, l'opposition radicale entre l'Histoire et la Géographie sur le Facteur 1).
* **Calcul des Spécificités** : Identification des termes significativement sur-représentés ou sous-représentés en fonction de l'année (diachronie) ou de la matière.
* **Analyse des Concordances et Co-occurrences** : Exploration textuelle fine de lemmes clés tels que `permettre`, `changement`, `liberté`, ou des formes pivots `pièges` / `écueils`.
* **Analyse des Progressions** : Évaluation graphique de la distribution et de la fréquence cumulée de lemmes étalons au sein des documents.


---

## Principaux Résultats
* **Histoire (Recentrement et Renouvellement)** : Les fiches révèlent une attention accrue portée aux *gender studies* (lemme `femme`) et à l'histoire par le bas / coloniale (`traite`, `colonial`, `esclavage`), mais réinscrite dans un cadre politique républicain centralisateur (`République`, `vote`, `suffrage`). On note également un basculement grammatical majeur : les fiches de 2015 utilisaient préférentiellement le passé simple et l'imparfait, tandis que celles de 2025 imposent le présent, conférant au discours une valeur de vérité générale qui fige le fait historique.
* **Géographie (De l'Humanitaire au Technicisme)** : Glissement sémantique d'un discours centré en 2015 sur les catastrophes humanitaires, la pauvreté et les manques (`pauvreté`, `santé`, `eau`, `alimentaire`) vers un discours managérial, libéral et technique en 2025 articulé autour du concept de `changement global`, de la gestion des `ressources`, des `risques`, des `dynamiques` d'aménagement et des flux productifs (migrants économiques et tourisme).
* **Gouvernance Pédagogique Implicite** : Bien que la liberté pédagogique soit réaffirmée en façade, la structure même des fiches opère un cadrage fort. Le passage du segment `pièges à éviter` (2015) à `écueils à éviter` (2025) montre une codification des pratiques. De plus, la profusion du verbe `permettre` employé au présent de l'indicatif suivi d'un infinitif objectif (`permet d'aborder`, `permet de comprendre`) agit comme une injonction masquée sous l'apparence de la possibilité.
* **L'EMC ou l'Incarnation des Valeurs** : L'EMC monopolise le discours de la valeur. Alors qu'en HG, les élèves sont désignés au pluriel (*les élèves*) pour préserver une distance scientifique objective, l'EMC utilise massivement le singulier (*l'élève*), ciblant une personnalisation et une individualisation. De surcroît, la figure de l'enseignant y est fortement rappellée sous les traits universels (et exclusivement masculins dans le texte) du `professeur`, ce qui n'est pas sans rappeller le statut enseignant de la Troisième République.

---

## Outils mobilisés

- les [fiches Eduscol](https://eduscol.education.gouv.fr/)
- la bibliothèque [`PyMuPDF` en Python](https://pypi.org/project/PyMuPDF/)
- le site [AnalyseSHS](http://analyse.univ-paris1.fr/)
- le logiciel [TXM](https://txm.gitpages.huma-num.fr/textometrie/Telecharger/) pour toutes les autres analyses
