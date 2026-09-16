# 🚨 CityOps AI

### Plataforma de Inteligência Operacional baseada em Dados, Machine Learning e IA Generativa

> Transformando milhões de solicitações urbanas em informações acionáveis para apoiar decisões operacionais.

---

## 📌 Sobre o projeto

O **CityOps AI** é uma plataforma de análise e inteligência operacional desenvolvida para investigar e antecipar problemas relacionados a solicitações de serviços urbanos.

O projeto utiliza dados públicos do **NYC 311 Service Requests** para construir uma arquitetura completa de dados, combinando:

- Engenharia de Dados
- SQL
- Data Warehouse
- ETL/ELT
- Analytics
- Machine Learning
- Explainable AI
- NLP e Embeddings
- RAG
- IA Generativa
- APIs
- Automação
- Visualização de dados
- MLOps
- Containerização

O objetivo não é apenas responder **"quantos chamados existem?"**, mas transformar os dados em respostas para perguntas como:

> **Onde os problemas estão concentrados?**

> **Quais solicitações apresentam maior risco operacional?**

> **Quais regiões estão apresentando comportamento anormal?**

> **Quais categorias estão pressionando a operação?**

> **Quais fatores contribuem para o atraso de uma solicitação?**

> **O que os dados indicam que deveria ser investigado?**

---

# 🎯 Problema de negócio

Grandes operações públicas recebem milhares de solicitações diariamente.

Quando esses dados são analisados apenas por relatórios tradicionais, informações importantes podem permanecer ocultas:

- aumento repentino de determinados problemas;
- concentração geográfica;
- aumento de backlog;
- categorias com alto tempo de resolução;
- agências sobrecarregadas;
- padrões sazonais;
- solicitações semelhantes;
- risco de violação de SLA.

O CityOps AI busca criar uma camada de inteligência sobre esses dados.

---

# 🧠 Proposta

A plataforma combina dados históricos, Machine Learning e IA Generativa para criar um ciclo:

```text
                    DADOS
                      │
                      ▼
              INGESTÃO / ETL
                      │
                      ▼
              DATA WAREHOUSE
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      ANALYTICS       ML         GENAI
          │           │           │
          ▼           ▼           ▼
       Power BI   Predições      RAG
                      │           │
                      └─────┬─────┘
                            ▼
                           API
                            │
                            ▼
                         React
                            │
                            ▼
                           n8n
```

---

# 📊 Dataset

O projeto utiliza o dataset público:

**NYC 311 Service Requests**

O conjunto contém registros de solicitações realizadas por cidadãos de Nova York envolvendo diferentes tipos de serviços e problemas urbanos.

Entre os dados utilizados estão:

- identificador da solicitação;
- data de criação;
- data de encerramento;
- agência responsável;
- tipo de reclamação;
- descrição;
- localização;
- bairro;
- CEP;
- latitude;
- longitude.

> O projeto utilizará um recorte controlado do dataset durante o desenvolvimento e poderá ser expandido posteriormente.

---

# 🏗️ Arquitetura

A arquitetura proposta é composta por:

```text
NYC 311
   │
   ▼
Data Ingestion
   │
   ▼
Raw Layer
   │
   ▼
Python / dbt
   │
   ▼
Data Warehouse
   │
   ├──────────────► Analytics
   │                    │
   │                    ▼
   │                 Power BI
   │
   ├──────────────► Machine Learning
   │                    │
   │                    ├── SLA Prediction
   │                    ├── Anomaly Detection
   │                    └── Explainability
   │
   └──────────────► GenAI
                        │
                        ├── Embeddings
                        ├── RAG
                        └── AI Analyst
```

---

# 🗄️ Data Architecture

O projeto será estruturado em diferentes camadas.

## Raw

Dados originais ingeridos do dataset.

```text
raw_311_requests
```

## Staging

Tratamento inicial e padronização.

```text
stg_311_requests
```

## Intermediate

Transformações intermediárias.

```text
int_request_resolution
int_request_sla
int_request_location
```

## Marts

Modelos preparados para consumo analítico.

```text
fact_service_requests

dim_date
dim_location
dim_agency
dim_complaint

mart_operations
mart_sla
mart_geography
mart_agencies
```

---

# 🔄 Pipeline de Dados

O pipeline será responsável por:

1. ingestão dos dados;
2. validação;
3. limpeza;
4. padronização;
5. tratamento de valores nulos;
6. tratamento de duplicidades;
7. transformação das datas;
8. criação de métricas operacionais;
9. carregamento no Data Warehouse;
10. validação dos modelos analíticos.

Fluxo:

```text
Dataset
   ↓
Python
   ↓
Validation
   ↓
PostgreSQL
   ↓
dbt
   ↓
Data Warehouse
   ↓
Analytics / ML / AI
```

---

# 📈 Analytics

A camada analítica busca responder perguntas como:

### Operação

- Quantas solicitações são abertas diariamente?
- Quais categorias concentram maior volume?
- Quais agências recebem mais solicitações?
- Como o volume evolui ao longo do tempo?

### SLA

- Qual o tempo médio de resolução?
- Quais categorias apresentam maior tempo de resolução?
- Quais agências apresentam maior backlog?
- Qual percentual das solicitações ultrapassa o SLA?

### Geografia

- Quais regiões concentram determinados problemas?
- Existem hotspots?
- Como os problemas se distribuem geograficamente?

---

# 🤖 Machine Learning

## SLA Risk Prediction

Um dos principais modelos do projeto será responsável por estimar o risco de uma solicitação ultrapassar o SLA.

Exemplo:

```text
Solicitação
     ↓
Feature Engineering
     ↓
Machine Learning
     ↓
Risk Score
```

Resultado esperado:

```text
SLA Risk: 83%

Classificação:
HIGH RISK
```

### Features potenciais

- agência;
- categoria;
- bairro;
- horário;
- dia da semana;
- mês;
- volume histórico;
- backlog;
- tempo médio histórico;
- características da solicitação.

---

# 🔍 Explainable AI

O modelo não deverá apenas apresentar uma previsão.

Também deverá explicar quais fatores contribuíram para o resultado.

Exemplo:

```text
SLA Risk: 83%

Principais fatores:

+ Categoria historicamente lenta
+ Alto volume atual
+ Backlog elevado
+ Região com maior tempo médio
```

A explicabilidade será explorada utilizando técnicas como **SHAP**.

---

# 🚨 Anomaly Detection

O projeto também terá um mecanismo para identificar comportamentos fora do padrão.

Exemplo:

```text
Categoria: Water Leak
Região: Brooklyn

Volume esperado: 120
Volume observado: 487

Status:
🚨 ANOMALIA
```

Inicialmente serão avaliadas técnicas como:

- Isolation Forest;
- clustering;
- análise estatística;
- séries temporais.

---

# 🗺️ Geospatial Intelligence

Os dados de latitude e longitude serão utilizados para desenvolver análises geográficas.

Possibilidades:

- distribuição das solicitações;
- mapas de densidade;
- hotspots;
- concentração por categoria;
- evolução temporal dos problemas;
- comparação entre regiões.

A camada geográfica poderá utilizar **PostGIS**.

---

# 🧬 NLP e Embeddings

As descrições das solicitações serão utilizadas para identificar similaridades semânticas.

Exemplo:

```text
"A rua está cheia de água."

        ↕
     similaridade
        ↕

"Existe um vazamento causando alagamento."
```

A solução poderá utilizar embeddings armazenados no **pgvector**.

Isso permitirá:

- busca semântica;
- agrupamento de problemas;
- identificação de solicitações semelhantes;
- recuperação contextual de informações.

---

# 📚 RAG

Será criada uma base documental contendo informações relacionadas aos serviços e responsabilidades operacionais.

Fluxo:

```text
Documentos
    ↓
Chunking
    ↓
Embeddings
    ↓
pgvector
    ↓
Retrieval
    ↓
LLM
```

O objetivo é permitir que a IA responda perguntas utilizando documentos de referência, reduzindo respostas sem fundamentação.

---

# 🧑‍💻 AI Analyst

A plataforma terá uma interface de consulta utilizando linguagem natural.

Exemplo:

> "Quais categorias aumentaram mais nos últimos três meses?"

Pipeline:

```text
Pergunta
   ↓
LLM
   ↓
Intent Detection
   ↓
SQL Generation
   ↓
SQL Validation
   ↓
PostgreSQL
   ↓
Resultado
   ↓
LLM
   ↓
Resposta
```

A camada de segurança deverá permitir somente operações de leitura.

```text
SELECT        ✅
WITH          ✅

INSERT        ❌
UPDATE        ❌
DELETE        ❌
DROP          ❌
ALTER         ❌
```

---

# 💬 Exemplo de interação

**Usuário:**

> Por que aumentaram os chamados relacionados a água em Brooklyn?

**CityOps AI:**

```text
Foram identificadas 3.821 solicitações
relacionadas a água no período analisado.

O volume apresentou aumento de 31%
em relação ao período anterior.

O crescimento está concentrado principalmente
em determinadas regiões de Brooklyn.

Principais categorias associadas:

1. Water Leak
2. Water System
3. Sewer

⚠️ O aumento está acima do comportamento
histórico esperado para o período.
```

Os valores apresentados deverão ser derivados dos dados consultados, e não gerados pelo modelo.

---

# 📊 Dashboards

## Executive Overview

Principais indicadores:

```text
Total Requests
SLA Compliance
Average Resolution Time
Open Backlog
High Risk Requests
Anomalies
```

## Operations

- volume;
- backlog;
- tempo de resolução;
- categorias;
- agências;
- tendências.

## SLA Intelligence

- SLA compliance;
- solicitações em risco;
- solicitações atrasadas;
- previsão;
- fatores de risco.

## Geospatial

- mapa;
- hotspots;
- densidade;
- categorias;
- evolução temporal.

---

# ⚙️ Automação

O **n8n** será utilizado para orquestrar processos operacionais.

Exemplo:

```text
Scheduled Workflow
       ↓
Data Update
       ↓
ETL
       ↓
Model Prediction
       ↓
Anomaly Detection
       ↓
AI Analysis
       ↓
Notification
```

Outro fluxo:

```text
High Risk Request
       ↓
Risk > Threshold
       ↓
Generate AI Summary
       ↓
Operational Alert
```

---

# 🧪 MLOps

Os experimentos de Machine Learning serão acompanhados utilizando **MLflow**.

Serão registrados:

- modelo;
- versão;
- parâmetros;
- dataset;
- métricas;
- artefatos;
- resultados dos experimentos.

Exemplo:

```text
Model v1
F1: 0.71

Model v2
F1: 0.78

Model v3
F1: 0.82
```

O objetivo não é buscar apenas uma métrica alta, mas comparar modelos e documentar as decisões técnicas.

---

# 🛠️ Tecnologias

| Área | Tecnologia |
|---|---|
| Linguagem | Python |
| Banco | PostgreSQL |
| Geospatial | PostGIS |
| Vector Database | pgvector |
| Transformações | dbt |
| ETL | Python |
| ML | Scikit-learn / XGBoost |
| Explainability | SHAP |
| GenAI | OpenAI API |
| RAG | Embeddings + pgvector |
| Backend | FastAPI |
| Frontend | React + TypeScript |
| BI | Power BI |
| Automação | n8n |
| MLOps | MLflow |
| Containers | Docker |
| Versionamento | Git / GitHub |

---

# 📁 Estrutura do projeto

```text
cityops-ai/
│
├── data/
│
├── ingestion/
│
├── warehouse/
│
├── dbt/
│
├── notebooks/
│
├── ml/
│   ├── training/
│   ├── inference/
│   └── evaluation/
│
├── genai/
│   ├── prompts/
│   ├── agents/
│   └── insights/
│
├── rag/
│   ├── ingestion/
│   ├── embeddings/
│   └── retrieval/
│
├── api/
│
├── frontend/
│
├── n8n/
│
├── dashboards/
│
├── tests/
│
├── docs/
│
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

---

# 🔐 Segurança

Informações sensíveis não serão armazenadas no repositório.

Variáveis de ambiente:

```text
DATABASE_URL=
OPENAI_API_KEY=
MLFLOW_TRACKING_URI=
```

O arquivo `.env` deverá estar no `.gitignore`.

Será disponibilizado:

```text
.env.example
```

sem credenciais reais.

---

# 🧪 Qualidade dos dados

O projeto deverá implementar validações para:

- valores nulos;
- duplicidades;
- datas inválidas;
- coordenadas inválidas;
- categorias inesperadas;
- relacionamentos;
- consistência temporal.

Os testes serão executados durante o pipeline de transformação.

---

# 📈 Métricas do projeto

O projeto será avaliado em diferentes dimensões.

### Data Quality

- percentual de registros válidos;
- completude;
- duplicidade;
- consistência.

### Analytics

- SLA;
- backlog;
- tempo médio;
- volume;
- tendência.

### Machine Learning

- Precision;
- Recall;
- F1-score;
- ROC-AUC.

### GenAI

- qualidade das respostas;
- grounding;
- taxa de respostas sem evidência;
- latência;
- custo por consulta.

---

# 🗺️ Roadmap

## Fase 1 — Data Engineering

- [ ] Dataset
- [ ] Ingestion
- [ ] PostgreSQL
- [ ] Raw layer
- [ ] Staging
- [ ] Data Warehouse
- [ ] dbt
- [ ] Data quality

## Fase 2 — Analytics

- [ ] KPIs
- [ ] SLA
- [ ] Backlog
- [ ] Análise temporal
- [ ] Análise por agência
- [ ] Power BI
- [ ] Geospatial

## Fase 3 — Machine Learning

- [ ] Feature engineering
- [ ] Baseline
- [ ] Logistic Regression
- [ ] Random Forest
- [ ] XGBoost
- [ ] Model evaluation
- [ ] SHAP
- [ ] SLA prediction
- [ ] Anomaly detection

## Fase 4 — GenAI

- [ ] LLM
- [ ] Structured outputs
- [ ] Embeddings
- [ ] pgvector
- [ ] Semantic search
- [ ] RAG
- [ ] AI Analyst
- [ ] SQL generation
- [ ] Guardrails

## Fase 5 — Product

- [ ] FastAPI
- [ ] React
- [ ] Authentication
- [ ] Dashboard
- [ ] AI interface
- [ ] Geospatial interface
- [ ] n8n
- [ ] Notifications

## Fase 6 — Production

- [ ] Docker
- [ ] MLflow
- [ ] Logging
- [ ] Monitoring
- [ ] Tests
- [ ] CI/CD
- [ ] Documentation

---

# 🎯 Objetivo de portfólio

O CityOps AI foi concebido para demonstrar a construção de uma solução completa de dados, desde a ingestão até a aplicação final.

O foco está em demonstrar:

```text
Dados
  ↓
Engenharia
  ↓
Modelagem
  ↓
Analytics
  ↓
Machine Learning
  ↓
IA Generativa
  ↓
API
  ↓
Aplicação
  ↓
Automação
```

Mais do que apresentar gráficos, o projeto busca demonstrar como **dados e inteligência artificial podem ser utilizados para identificar problemas, antecipar riscos e apoiar decisões operacionais**.

---

# 👨‍💻 Autor

**Guilherme Mazzoni**

Projeto desenvolvido para fins de estudo, experimentação e portfólio profissional em:

- Data Analytics
- Data Engineering
- Machine Learning
- Artificial Intelligence
- Business Intelligence

---

## 📌 Status

🚧 **Em desenvolvimento**

O projeto será desenvolvido incrementalmente, começando pela camada de dados e evoluindo até a aplicação completa.