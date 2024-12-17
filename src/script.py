"""
pip install google-cloud-storage

export GOOGLE_APPLICATION_CREDENTIALS="pdm-class-2024-a52322c9a911.json"
"""
import os
from google.cloud import storage


def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """
    Upload a file to Google Cloud Storage.

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_file_path (str): Local path to the file.
        destination_blob_name (str): Path in GCS (object name).
    """
    try:
        # Inicializa o cliente do Google Cloud Storage
        client = storage.Client()

        # Acessa o bucket
        bucket = client.bucket(bucket_name)

        # Cria um objeto (blob) no GCS e faz o upload
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path, timeout=500)

        print(f"Arquivo {source_file_path} foi enviado para {bucket_name}/{destination_blob_name}")

    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")
