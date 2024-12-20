import os
import openai
from dotenv import load_dotenv
from retriever import Retriever

# Carrega variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AnswerRelevance:
    def __init__(self, txt_file="resultado_avaliacao.txt"):
        """Inicializa a avaliação e o retriever."""
        self.txt_file = txt_file
        self.retriever = Retriever()

    def evaluate_with_llm(self, query, documents):
        """Avalia respostas usando a API OpenAI."""
        if not documents or "Desculpe" in documents[0]:
            return "Desculpe, não encontrei informações relevantes para responder sua consulta."

        # Formata o prompt
        prompt = (
            f"Você é um consultor político experiente.\n\n"
            f"Consulta: {query}\n\n"
            f"Documentos Recuperados:\n{documents}\n\n"
            f"Responda de forma clara e profissional."
        )

        # Chamada à API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Substitua por gpt-4 se desejar
            messages=[
                {"role": "system", "content": "Você é um consultor político experiente."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()

    def process_query(self, query):
        """Processa a consulta e salva a resposta."""
        # Recupera informações relevantes
        texts = self.retriever.retrieve(query)

        # Avalia a resposta usando OpenAI
        response_text = self.evaluate_with_llm(query, "\n\n".join(texts))

        # Salva consulta e resposta no arquivo TXT
        with open(self.txt_file, "a", encoding="utf-8") as file:
            file.write(f"Consulta: {query}\n")
            file.write(f"Resposta Avaliada: {response_text}\n")
            file.write("-" * 40 + "\n")

        print(f"Resposta Avaliada: {response_text}")

# Execução Principal
if __name__ == "__main__":
    evaluator = AnswerRelevance()

    while True:
        query = input("Digite sua consulta (ou 'sair' para encerrar): ")
        if query.lower() == "sair":
            break
        evaluator.process_query(query)