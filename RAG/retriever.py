import os

class Retriever:
    def __init__(self, txt_file=r"dados/report.txt"):
        """Inicializa o retriever com o arquivo de texto."""
        if not os.path.isfile(txt_file):
            raise FileNotFoundError(f"Arquivo não encontrado: {txt_file}")

        # Carrega o conteúdo do arquivo TXT
        with open(txt_file, "r", encoding="utf-8") as file:
            self.data = file.readlines()

    def retrieve(self, query):
        """Busca informações relevantes no arquivo TXT."""
        resultados = [linha.strip() for linha in self.data if query.lower() in linha.lower()]
        
        if resultados:
            return resultados
        else:
            return ["Desculpe, não encontrei informações relevantes."]