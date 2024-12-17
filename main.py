
import os
from src.script import upload_to_gcs

# Configurações dos dados
credentials_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/pdm-class-2024-a52322c9a911.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Nome do bucket - padrão
bucket_name = "trabalho-final-pdm" 

# Dados do IBGE

source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/IBGE/Basico_GO.csv"  # Caminho do arquivo local
destination_blob_name = "bronze/Basico_GO" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

### descrição dos dados IBGE
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/IBGE/infos.pdf"
destination_blob_name = "bronze/ibge_infos" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# Dados TSE
# votacao_secao_2012_GO
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/tse/votacao_secao_2012_GO/votacao_secao_2012_GO.csv"
destination_blob_name = "bronze/votacao_secao_2012_GO" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# votacao_secao_2016_GO
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/tse/votacao_secao_2016_GO/votacao_secao_2016_GO.csv"
destination_blob_name = "bronze/votacao_secao_2016_GO" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# votacao_secao_2020_GO
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/tse/votacao_secao_2020_GO/votacao_secao_2020_GO.csv"
destination_blob_name = "bronze/votacao_secao_2020_GO" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# votacao_secao_2024_GO
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/tse/votacao_secao_2024_GO/votacao_secao_2024_GO.csv"
destination_blob_name = "bronze/votacao_secao_2024_GO" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# zonas_goânia
source_file_path = "/home/lisamenezes/Searches/pipeline-dados-PDM/data/zonas_goiania.csv"
destination_blob_name = "bronze/zonas_goiania" 
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)


