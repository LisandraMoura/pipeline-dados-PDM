import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
from google.cloud import storage
import joblib
import os
import io
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

MODEL_PATH = "model.pkl"

@app.route('/')
def home():
    """
    Rota para a página inicial.
    """
    return render_template('home.html')

# Função para carregar dados do GCS
def load_data_from_gcs(bucket_name, file_name):
    """Carrega dados do GCS para um DataFrame do Pandas."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()
    return pd.read_csv(io.StringIO(data))

@app.route('/train', methods=['GET', 'POST'])
def train_page():
    """
    Página para treinar o modelo via formulário ou API.
    """
    if request.method == 'GET':
        # Renderiza a página HTML com o formulário
        return render_template('train.html')

    elif request.method == 'POST':
        # Captura os dados do formulário ou do corpo JSON
        if request.form:  # Submissão via formulário HTML
            bucket_name = request.form.get('bucket_name')
            file_name = request.form.get('file_name')
            n_clusters = int(request.form.get('n_clusters', 3))
        else:  # Submissão via API
            content = request.get_json()
            bucket_name = content.get("bucket_name")
            file_name = content.get("file_name")
            n_clusters = content.get("n_clusters", 3)

        # Verifica se os parâmetros essenciais estão presentes
        if not bucket_name or not file_name:
            return jsonify({"error": "Bucket name e file name são obrigatórios."}), 400

        # Carregar os dados do GCS
        try:
            data = load_data_from_gcs(bucket_name, file_name)
        except Exception as e:
            return jsonify({"error": f"Erro ao carregar dados: {str(e)}"}), 400

        # Treinar o modelo
        features = ["Proporcao_negros_pardos_indigenas", "Proporcao_feminino", "RENDA"]
        X = data[features].dropna()
        y = data.loc[X.index, "NUM_PARTIDO"]

        if X.empty:
            return jsonify({"error": "Os dados fornecidos estão vazios ou incompletos para treinamento."}), 400
        
        if X.std().sum() == 0:
            return jsonify({"error": "Os dados não possuem variação suficiente para clustering."}), 400

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X_scaled)

        cluster_to_partido = {}
        for cluster in range(n_clusters):
            cluster_indices = (kmeans.labels_ == cluster)
            cluster_partidos = y[cluster_indices]
            if not cluster_partidos.empty:
                cluster_to_partido[cluster] = cluster_partidos.mode()[0]  # Partido mais frequente no cluster


        # Salvar o modelo localmente
        try:
            joblib.dump((kmeans, cluster_to_partido), MODEL_PATH)
        except Exception as e:
            return jsonify({"error": f"Erro ao salvar o modelo localmente: {str(e)}"}), 500

        # Fazer upload do modelo para o GCS
        try:
            gcs_model_path = "models/clustering_model.pkl"  # Caminho no GCS
            save_model_to_gcs(bucket_name, MODEL_PATH, gcs_model_path)
        except Exception as e:
            return jsonify({"error": f"Erro ao salvar o modelo no GCS: {str(e)}"}), 500

        # Retorna mensagem amigável ao navegador ou resposta JSON
        if request.form:
            return render_template(
                "train.html",
                message="Modelo treinado e salvo com sucesso no GCS.",
                bucket_name=bucket_name,
                file_name=file_name,
                n_clusters=n_clusters,
            )
        else:
            return jsonify({"message": "Modelo treinado e salvo com sucesso.", "n_clusters": n_clusters})



@app.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """
    Página para fazer inferência com o modelo treinado.
    """
    if request.method == 'GET':
        return render_template('predict.html')

    elif request.method == 'POST':
        try:
            # Capturar os dados de entrada do formulário
            proporcao_negros = float(request.form.get('Proporcao_negros_pardos_indigenas'))
            proporcao_feminino = float(request.form.get('Proporcao_feminino'))
            renda = float(request.form.get('RENDA'))
        except ValueError:
            return jsonify({"error": "Todos os valores devem ser numéricos."}), 400

        # Carregar o modelo treinado
        try:
            kmeans, cluster_to_partido = joblib.load(MODEL_PATH)
        except Exception as e:
            return jsonify({"error": f"Erro ao carregar o modelo: {str(e)}"}), 500

        # Criar o vetor de entrada para predição
        try:
            input_data = np.array([[proporcao_negros, proporcao_feminino, renda]])
            cluster = kmeans.predict(input_data)[0]
        except Exception as e:
            return jsonify({"error": f"Erro ao fazer a predição: {str(e)}"}), 500
        
        # Retornar o partido associado ao cluster
        try:
            num_partido_pred = cluster_to_partido.get(cluster, None)
            if num_partido_pred is None:
                return jsonify({"error": "Nenhum partido associado ao cluster identificado."}), 500
        except Exception as e:
            return jsonify({"error": f"Erro ao associar o cluster ao partido: {str(e)}"}), 500


        return jsonify({
            "cluster": int(cluster),
            "num_partido_pred": int(num_partido_pred),
            "message": "Inferência realizada com sucesso."
        })

def save_model_to_gcs(bucket_name, model_path, gcs_path):
    """Faz upload do modelo salvo localmente para o GCS."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    # Enviar o arquivo para o GCS
    blob.upload_from_filename(model_path)
    print(f"Modelo enviado para o GCS: gs://{bucket_name}/{gcs_path}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
