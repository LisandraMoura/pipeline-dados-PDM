import os

class Indexer:
    def __init__(self, txt_file=r"dados/report.txt"):
        """Inicializa o indexador com um arquivo de texto."""
        self.txt_file = txt_file

    def ingest_data(self):
        """Carrega e exibe informações do arquivo TXT."""
        if not os.path.isfile(self.txt_file):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.txt_file}")

        try:
            with open(self.txt_file, "r", encoding="utf-8") as file:
                linhas = file.readlines()

            print("Conteúdo do arquivo:\n")
            for linha in linhas:
                print(linha.strip())  # Remove espaços extras

            print("\nIngestão concluída!")
        except Exception as e:
            raise ValueError(f"Erro ao carregar o arquivo TXT: {e}")

# Execução Principal
if __name__ == "__main__":
    indexer = Indexer()
    indexer.ingest_data()