from flask import Flask, request, render_template, jsonify
from retriever import Retriever
from evaluation import AnswerRelevance
import os
from hugchat import hugchat
from hugchat.login import Login
import time

# Configurações de login
EMAIL = ""
PASSWD = ""
cookie_path_dir = "./cookies/"  # O diretório onde os cookies serão salvos

# Realiza o login no HuggingChat e configura o chatbot
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def call_huggingchat(prompt, model_name, retries=3, delay=20):
    try:
        models = chatbot.get_available_llm_models()
        model_index = next((i for i, m in enumerate(models) if m.id == model_name), None)

        if model_index is not None:
            chatbot.switch_llm(model_index)
            print(f"Modelo '{model_name}' selecionado com sucesso!")
        else:
            raise ValueError(f"Modelo '{model_name}' não encontrado.")

        for attempt in range(retries):
            try:
                chatbot.new_conversation(switch_to=True)
                response = chatbot.chat(prompt)
                return response
            except Exception as e:
                print(f"Erro na tentativa {attempt + 1}: {e}")
                if "You are sending too many messages" in str(e):
                    time.sleep(delay)
                else:
                    raise
    except Exception as e:
        print(f"Erro crítico em call_huggingchat: {e}")
        raise

app = Flask(__name__)

# Inicializa o retriever e avaliador
retriever = Retriever(txt_file="dados/report.txt")
evaluator = AnswerRelevance()

@app.route('/')
def home():
    """Página inicial."""
    return render_template('home.html')

@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    """Página para consulta de informações."""
    if request.method == 'POST':
        query = request.form.get('query')
        resultados_brutos = retriever.retrieve(query)
        if not resultados_brutos:
            return render_template('retrieve.html', 
                                   resultados=["Nenhuma informação encontrada para sua consulta."])
        prompt = (
            f"""Você é um assistente altamente inteligente. Eu fornecerei informações brutas,e você deverá refiná-las para serem mais claras, concisas e úteis para um humano com base na query do usuário.
            {resultados_brutos}
            Crie uma resposta coerente e resumida para a consulta do usuário: '{query}'."""
        )

        
        # Chama o HuggingChat para refinar os resultados
        try:
            resposta_refinada = call_huggingchat(prompt, model_name="Qwen/Qwen2.5-72B-Instruct")
        except Exception as e:
            print(f"Erro ao usar o HuggingChat: {e}")
            resposta_refinada = "Houve um erro ao gerar a resposta. Tente novamente mais tarde."
        
        # Retorna a página com os resultados
        return render_template('retrieve.html', 
                               resultados=[resposta_refinada])
    return render_template('retrieve.html')


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    """Página para avaliar resposta com LLM."""
    if request.method == 'POST':
        query = request.form.get('query')
        documentos = retriever.retrieve(query)
        resposta = evaluator.evaluate_with_llm(query, "\n".join(documentos))
        return render_template('evaluate.html', resposta=resposta)
    return render_template('evaluate.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
