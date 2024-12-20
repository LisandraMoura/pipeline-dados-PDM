# Documentação do Projeto Final: Processamento de Dados Massivos

### Objetivo

O objetivo deste trabalho é validar a viabilidade de usar dados abertos do IBGE e TSE para fins de marketing político estratégico utilizando Inteligência Artificial (IA).

A relevância de campanhas baseadas em dados tem crescido, possibilitando maior compreensão do comportamento do eleitorado. Em 2022, as campanhas presidenciais no Brasil investiram mais de R$ 1 bilhão, com uma parcela significativa em publicidade digital. Dados mostram que:

- Campanhas que utilizam dados apresentam 64% mais eficiência na segmentação de público.

- Eleitores têm 40% mais engajamento com mensagens personalizadas.

### Dados Utilizados

#### IBGE

- Fonte: Censo Demográfico de 2010

- Abrangência: Agregados por setor censitário do estado de Goiás

- Tabelas:

    - Basico_GO.csv

    - Pessoas04.csv

#### TSE

- Resultados das Eleições:

    - Anos: 2012, 2016 e 2020

#### Processamento de Dados

Utilizamos a arquitetura Medallion para estruturar o pipeline de dados em três camadas:

1. Bronze: Dados brutos coletados diretamente das fontes originais.

2. Silver: Dados processados com filtragens, limpezas e enriquecimentos.

3. Gold: Dados prontos para análise e geração de insights.

#### Agregações Realizadas

Na camada final, consolidamos as informações em uma tabela única por ano, contendo os seguintes campos:

- Ano Eleitoral: ```ANO_ELEICAO```

- Localidade: ```NM_MUNICIPIO```, ```NR_ZONA```, ```NR_SECAO```, ```NM_LOCAL_VOTACAO```, ```Nome_do_subdistrito```

- Dados Eleitorais: ```CD_TIPO_ELEICAO```, ```NR_TURNO```, ```DS_CARGO```, ```NM_VOTAVEL```, ```NR_VOTAVEL```, ```QT_VOTOS```

- Dados Demográficos: ```Situacao_setor_x```, ```V005```, ```V009```, ```Proporcao_negros_pardos_indigenas```, ```Proporcao_feminino```, ```Proporcao_18_39```, ```RENDA```

Essas tabelas foram estruturadas para permitir correlações entre variáveis demográficas e resultados eleitorais.

#### Visualização e Análise

##### Tabelas Gold

As tabelas da camada gold foram otimizadas para suporte à análise no **Metabase**, permitindo a geração de gráficos e dashboards interativos para exploração dos dados.

#### Pasta de Notebooks

Na pasta notebooks, disponibilizamos exemplos de execução e demonstração do pipeline.

Os notebooks principais (```pasta dataproc```) foram executados no **Google Cloud Dataproc**, com versões completas armazenadas no GCS.

#### Ativação do KNN no Cloud Run

##### Configurações do GCS CLI


1. Faça o download e instale o Google Cloud CLI

2. Após a instalação, autentique-se:

    ```gcloud auth login```

3. Defina o projeto padrão:

    ```gcloud config set project [PROJECT_ID]```


##### Recompilar a Imagem Docker

```docker build -t gcr.io/pdm-class-2024/clustering-app:latest .```

##### Subir a Imagem para o GCR

```docker push gcr.io/pdm-class-2024/clustering-app:latest```

##### Realizar o Redeploy no Cloud Run

```
gcloud run deploy clustering-app \
    --image gcr.io/pdm-class-2024/clustering-app:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```


#### Ativação do RAG no Cloud Run


##### Configurações do GCS CLI


1. Faça o download e instale o Google Cloud CLI

2. Após a instalação, autentique-se:

    ```gcloud auth login```

3. Defina o projeto padrão:

    ```gcloud config set project [PROJECT_ID]```
    

##### Recompilar a Imagem Docker

```docker build -t gcr.io/pdm-class-2024/rag:latest .```

#### Subir a Imagem para o GCR

```docker push gcr.io/pdm-class-2024/rag:latest```

##### Realizar o Redeploy no Cloud Run


```
gcloud run deploy rag \
    --image gcr.io/pdm-class-2024/rag:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```
