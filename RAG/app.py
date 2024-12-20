from flask import Flask, request, render_template, jsonify
from retriever import Retriever
from evaluation import AnswerRelevance
import os

app = Flask(__name__)

# Inicializa o retriever e avaliador
retriever = Retriever(txt_file="Dados/report.txt")
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
        resultados = retriever.retrieve(query)
        return render_template('retrieve.html', resultados=resultados)
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
    app.run(host='0.0.0.0', port=8080)
