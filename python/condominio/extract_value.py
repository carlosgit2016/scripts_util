import re
import PyPDF2
import sys
import os 

def extract_valor_from_pdf(pdf_path):

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()

            lines = text.split('\n')

            # Index
            login_index = lines.index('LOGIN:   ALYSON      SENHA:  170479')
            n_index = lines.index('N')
            fundo_index = lines.index('FUNDO DE RESERVA')

            # Calc valor index
            valor_index = n_index + (fundo_index - login_index)

            return lines[valor_index - 2]

    return None

def normalize(value) -> float:
    pattern = r'R\$\s([0-9]+),([0-9]+)'
    match = re.search(pattern, value)
    n_str = f'{match.group(1)}.{match.group(2)}'
    return float(n_str)

if __name__ == "__main__":
    folder_path = sys.argv[1]

    total = 0.0
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            valor = extract_valor_from_pdf(pdf_path)
            total += normalize(valor)
            print(f"{filename}: {valor}")
    print(round(total, 2))
