import re
import json

def roman_to_int(roman):
    # Function to convert Roman numeral to integer
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    
    for letter in reversed(roman):
        value = roman_numerals[letter]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
        
    return total

class TextCleaner():

    def __init__(self, input_path: str):

        self.input_path: str = input_path

        with open(self.input_path, "r", encoding="utf-8") as f:
            self.text: str = f.read()

    def replace_roman_numbers(self, text):
    # Function to replace Roman numerals with integers

        def replacement(match):
            # Convert Roman numeral to integer
            word = match.group(1)
            roman = match.group(3)
            normal_number = roman_to_int(roman)
            return f"{word} {normal_number}"
        
        # Regex pattern to find Roman numerals after SECÇÃO, CAPÍTULO, or SUBSECÇÃO (case-insensitive)
        pattern = r'(LIVRO|TÍTULO|SUBTÍTULO|CAPÍTULO|SECÇÃO|SUBSECÇÃO|DIVISÃO)(\s+)([IVXLCDM]+)'
        
        # Replace the Roman numerals using the regex
        return re.sub(pattern, replacement, text)
    
    def clean_txt(self, codigo_type: str = "CIVIL"):

        self.codigo_type = codigo_type

        if codigo_type == "CIVIL":
            self.text = re.sub(r"CÓDIGO CIVIL.*?CÓDIGO CIVIL", "CÓDIGO CIVIL", self.text, flags=re.S)

        elif codigo_type == "PENAL":
            self.text = re.sub(r"CÓDIGO PENAL.*?CÓDIGO PENAL", "CÓDIGO PENAL", self.text, flags=re.S)

        # Ensure fully uppercase words have a newline before and after
        self.text = re.sub(r"(\s*)([A-ZÀ-ÖØ-Ý]{2,})(\s*)", r"\n\2\n", self.text)

        # Replace multiple spaces and newlines with a single space
        self.text = re.sub(r"\s+", " ", self.text)

        # Restore newlines for better formatting
        self.text = self.text.replace(". ", ".\n")

        # Standardize common punctuation
        self.text = self.text.replace("“", '"').replace("”", '"')  # Convert curly quotes to straight
        self.text = self.text.replace("‘", "'").replace("’", "'")  # Convert curly apostrophes to straight
        self.text = self.text.replace("—", "-")  # Convert em-dashes to simple dashes

        # Trim leading/trailing spaces
        self.text = self.text.strip()

        # Fix numbered sections (e.g., "2.\nSome self.text" → "2. Some self.text")
        self.text = re.sub(r"(\d+)\.\s*\n\s*", r"\1. ", self.text)

        # Fix numbers followed by a hyphen (e.g., "2 -" → "2.")
        self.text = re.sub(r"(\d+)\s*-\s*", r"\1. ", self.text)

        # Ensure "Artigo X.º (Title)" is on its own line
        self.text = re.sub(r"(Artigo \d+[.ººª]* \([^)]+\))", r"\n\1\n", self.text)

        # Remove accidental newlines inside "Artigo X.º (Title)", preserving dots in the title
        self.text = re.sub(r"(Artigo \d+[.ºª]* \([^\n]+)\n([^\n]+\))", r"\1 \2", self.text)

        # Trim leading/trailing spaces
        self.text = '\n'.join([line.lstrip() for line in self.text.splitlines()])

        # Remove all blank lines
        self.text = re.sub(r"\n+", "\n", self.text)

        self.text = re.sub(r"(\s*)CAPÍTULO", r"\nCAPÍTULO", self.text)

        self.text = re.sub(r"(\s*)Contém as alterações introduzidas pelos seguintes diplomas", r"\nContém as alterações introduzidas pelos seguintes diplomas", self.text)

        self.text = re.sub(r"(\s*)Versões anteriores deste artigo:", r"\nVersões anteriores deste artigo:", self.text)

        self.text = re.sub(r" SECÇÃO", r"\nSECÇÃO", self.text)
        self.text = re.sub(r" SUBSECÇÃO", r"\nSUBSECÇÃO", self.text)
        self.text = re.sub(r"(\s*)Artigo", r"\nArtigo", self.text)
        self.text = re.sub(r"(\s*)TÍTULO", r"\nTÍTULO", self.text)
        self.text = re.sub(r"(\s*)LIVRO", r"\nLIVRO", self.text)

        self.text = '\n'.join([line for line in self.text.splitlines() if "Contém as alterações introduzidas pelos seguintes diplomas:" not in line])

        self.text = '\n'.join([line for line in self.text.splitlines() if "Versões anteriores deste artigo:" not in line])

        self.text = '\n'.join([line for line in self.text.splitlines() if "Revogado pelo Decreto-Lei" not in line])

        # This regex matches a number followed by a dot, followed by a space, and then an uppercase word
        self.text = re.sub(r"(\d+\.\s*[A-Z]+)", r"\n\1", self.text)

        # Remove all blank lines
        self.text = re.sub(r"\n+", "\n", self.text)

        # Convert the Roman numerals in the self.text
        self.text = self.replace_roman_numbers(self.text)

    def create_livro_json(self, json_livro):

        livro = json_livro["metadata"]['Livro']
        livro_text = json_livro["text"]

        # Regular expression to match "Artigo X.º (Title)"
        matches = re.split(r"(TÍTULO \d+)", livro_text)[1:]  # Skip empty first element if any

        # Structure the data
        titulo_data = [
            {
                "text": matches[i + 1].strip(),
                "metadata": {
                    "Livro": livro,
                    "Titulo": matches[i],
                },
            }
            for i in range(0, len(matches), 2)
        ]

        return titulo_data

    def create_subtitulo_json(self, json_titulo):

        livro = json_titulo["metadata"]['Livro']
        titulo = json_titulo["metadata"]['Titulo']
        titulo_text = json_titulo["text"]

        # Regular expression to match "Artigo X.º (Title)"
        matches = re.split(r"(SUBTÍTULO \d+)", titulo_text)[1:]  # Skip empty first element if any

        if matches:

            # Structure the data
            subtitulo_data = [
                {
                    "text": matches[i + 1].strip(),
                    "metadata": {
                        "Livro": livro,
                        "Titulo": titulo,
                        "Subtitulo": matches[i],
                    },
                }
                for i in range(0, len(matches), 2)
            ]

        else:
            # No matches found, return entire text with empty titulo metadata
            subtitulo_data = [
                {
                    "text": titulo_text.strip(),
                    "metadata": {
                        "Livro": livro,
                        "Titulo": titulo,
                        "Subtitulo": "",
                    },
                }
            ]
        
        return subtitulo_data

    def create_capitulo_json(self, json_subtitulo):

        livro = json_subtitulo["metadata"]['Livro']
        titulo = json_subtitulo["metadata"]['Titulo']
        subtitulo = json_subtitulo["metadata"]['Subtitulo']
        subtitulo_text = json_subtitulo["text"]

        # Split based on the chapter headings
        matches = re.split(r"(CAPÍTULO \d+)", subtitulo_text)[1:]  # Skip empty first element if any

        # Structure the data
        capitulo_data = [
            {"text": matches[i + 1].strip(),
                        "metadata": {
                        "Livro": livro,
                        "Titulo": titulo,
                        "Subtitulo": subtitulo,
                        "capitulo": matches[i]
                    },}
            for i in range(0, len(matches), 2)
        ]

        return capitulo_data

    def create_seccao_json(self, json_seccao):

        livro = json_seccao["metadata"]['Livro']
        titulo = json_seccao["metadata"]['Titulo']
        subtitulo = json_seccao["metadata"]['Subtitulo']
        capitulo = json_seccao["metadata"]['capitulo']
        capitulo_text = json_seccao["text"]

        # Regular expression to match "Artigo X.º (Title)"
        matches = re.split(r"(SECÇÃO \d+)", capitulo_text)[1:]  # Skip empty first element if any

        if matches:

            # Structure the data
            seccao_data = [
                {
                    "text": matches[i + 1].strip(),
                    "metadata": {
                        "Livro": livro,
                        "Titulo": titulo,
                        "Subtitulo": subtitulo,
                        "capitulo": capitulo,
                        "sexao": matches[i]
                    },
                }
                for i in range(0, len(matches), 2)
            ]

        else:
            # No matches found, return entire text with empty titulo metadata
            seccao_data = [
                {
                    "text": capitulo_text.strip(),
                    "metadata": {
                        "Livro": livro,
                        "Titulo": titulo,
                        "Subtitulo": subtitulo,
                        "capitulo": capitulo,
                        "sexao": ""
                    },
                }
            ]

        return seccao_data


    def clean_text(self, text):
        """Removes line breaks and numbers followed by a period."""
        text = re.sub(r"\d+\.\s*", "", text)  # Remove numbers followed by a period and space
        return " ".join(text.splitlines())  # Remove line breaks

    def create_artigo_civil_json(self, json_artigo):

        livro = json_artigo["metadata"]['Livro']
        titulo = json_artigo["metadata"]['Titulo']
        subtitulo = json_artigo["metadata"]['Subtitulo']
        capitulo = json_artigo["metadata"]['capitulo']
        capitulo_text = json_artigo["text"]
        seccao = json_artigo["metadata"]["sexao"]

        # Regular expression to match "Artigo X.º (Title)"
        pattern = r"(Artigo \d+\.º) \(([^)]+)\)"

        # Split based on the article headings
        matches = re.split(pattern, capitulo_text)[1:]  # Skip empty first element if any

        # Structure the data
        artigo_data = [
            {
                "text": self.clean_text(matches[i + 2].strip()), #matches[i + 2].strip(),
                "Livro": livro,
                "Titulo": titulo,
                "Subtitulo": subtitulo,
                "capitulo": capitulo,
                "sexao": seccao,
                "artigo": matches[i],
                "titulo_artigo": matches[i + 1],
            }
            for i in range(0, len(matches), 3)
        ]

        return artigo_data
    
    def create_artigo_penal_json(self, json_artigo):

        livro = json_artigo["metadata"]['Livro']
        titulo = json_artigo["metadata"]['Titulo']
        subtitulo = json_artigo["metadata"]['Subtitulo']
        capitulo = json_artigo["metadata"]['capitulo']
        capitulo_text = json_artigo["text"]
        seccao = json_artigo["metadata"]["sexao"]

        # Regular expression to match "Artigo X.º (Title)"
        pattern = r"(Artigo \d+\.º) ([A-Z][a-zà-ú]+(?: [a-zà-ú]+)*)"

        # Split based on the article headings
        matches = re.split(pattern, capitulo_text)[1:]  # Skip empty first element if any

        # Structure the data
        artigo_data = [
            {
                "text": self.clean_text(matches[i + 2].strip()), #matches[i + 2].strip(),
                "Livro": livro,
                "Titulo": titulo,
                "Subtitulo": subtitulo,
                "capitulo": capitulo,
                "sexao": seccao,
                "artigo": matches[i],
                "titulo_artigo": matches[i + 1],
            }
            for i in range(0, len(matches), 3)
        ]

        return artigo_data


    def create_json_data(self):

        # Split based on the chapter headings
        matches = re.split(r"(LIVRO \d+)", self.text)[1:]  # Skip empty first element if any

        # Structure the data
        livro_data = [
            {"text": matches[i + 1].strip(), "metadata": {"Livro": matches[i]}}
            for i in range(0, len(matches), 2)
        ]

        self.concatenated_json = []

        for json_livro in livro_data:

            titulo_data = self.create_livro_json(json_livro)

            for json_titulo in titulo_data:

                subtitulo_data = self.create_subtitulo_json(json_titulo)

                for json_subtitulo in subtitulo_data:

                    capitulo_data = self.create_capitulo_json(json_subtitulo)

                    for json_capitulo in capitulo_data:

                        seccao_data = self.create_seccao_json(json_capitulo)

                        for json_seccao in seccao_data:
                            
                            if self.codigo_type == "CIVIL":

                                capitulo_data = self.create_artigo_civil_json(json_seccao)

                            elif self.codigo_type == "PENAL":

                                capitulo_data = self.create_artigo_penal_json(json_seccao)

                            self.concatenated_json = self.concatenated_json + capitulo_data

    def save_json_data(self, file_name: str):
        
        # Save to a file
        with open(f"artifacts/{file_name}.json", "w") as file:
            json.dump(self.concatenated_json, file, indent=4)  # `indent=4` makes it readable