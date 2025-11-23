# Documentação Visual do Banco de Dados - ktt-diarios-lambda

Este documento apresenta a estrutura e o fluxo de uso das tabelas do sistema ktt-diarios-lambda usando diagramas Mermaid.

## 1. Diagrama Entidade-Relacionamento (ER)

```mermaid
erDiagram
    PESQUISAS ||--o{ RESULTADOS_EXECUCAO : "possui"
    PESQUISAS ||--o{ PUBLICACOES : "gera"
    PROCESSO ||--o{ PUBLICACOES : "referenciado_em"
    PROCESSO ||--o{ PROCESSO_ADVOGADOS : "possui"
    ADVOGADOS ||--o{ PROCESSO_ADVOGADOS : "representa"
    PUBLICACOES ||--o{ PUBLICACAO_DESTINATARIOS : "tem"

    PESQUISAS {
        bigserial id PK
        text termo_pesquisa "termo para buscar nos diários"
        text numero_processo "número CNJ do processo"
        text termo_nome_parte "nome de parte para buscar"
        text[] tribunais "array de tribunais (vazio = ALL)"
        date data_inicio "início do intervalo de busca"
        date data_fim "fim do intervalo de busca"
        text status "pendente | em_andamento | concluido"
        timestamp inserted_at
        timestamp updated_at
        text observacoes
    }

    RESULTADOS_EXECUCAO {
        bigserial id PK
        bigint pesquisa_id FK "referência à pesquisa"
        text tribunal "código do tribunal (TJSP, TRF1, PROCESSO)"
        date data_execucao "dia executado"
        int pagina "número da página processada"
        text status "em_andamento | concluido | erro | pendente_retry"
        int tentativa "tentativa atual (1-3)"
        int max_tentativas "máximo de tentativas (3)"
        int total_itens "itens encontrados na página"
        text erro_msg "mensagem de erro se falhou"
        timestamp inserted_at
        timestamp updated_at
        bigint resultado_tribunal_id "DEPRECATED"
    }

    PROCESSO {
        bigserial processo_id PK
        text numero_processo UK "número CNJ único"
        text tribunal "código do tribunal"
        text vara "vara/juízo"
        text nome_classe "classe processual"
        text codigo_classe "código da classe"
        timestamp inserted_at
        timestamp updated_at
    }

    PUBLICACOES {
        bigserial publicacao_id PK
        bigint indice UK "ID único da API ComunicaPJE"
        bigint processo_id FK "referência ao processo"
        bigint[] pesquisas_ids "array de IDs das pesquisas que encontraram"
        date data_disponibilizacao "data de disponibilização"
        date data_publicacao "data de publicação"
        text inteiro_teor "texto completo da publicação"
        text link "link para documento"
        timestamp inserted_at
        timestamp updated_at
    }

    ADVOGADOS {
        bigserial advogado_id PK
        text nome "nome do advogado"
        text numero_oab "número OAB"
        text uf_oab "UF da OAB"
        timestamp inserted_at
        timestamp updated_at
    }

    PROCESSO_ADVOGADOS {
        bigserial id PK
        bigint processo_id FK
        bigint advogado_id FK
        timestamp inserted_at
    }

    PUBLICACAO_DESTINATARIOS {
        bigserial id PK
        bigint publicacao_id FK
        text nome "nome do destinatário"
        text polo "polo processual (ativo/passivo)"
        timestamp inserted_at
    }
```

## 2. Fluxo de Estados da Pesquisa

```mermaid
stateDiagram-v2
    [*] --> pendente: INSERT na tabela pesquisas

    pendente --> em_andamento: Manager Lambda<br/>envia tasks para DetectorQueue

    em_andamento --> em_andamento: Executor Lambda<br/>processa páginas

    em_andamento --> concluido: Finalizer Lambda<br/>todas execuções OK ou<br/>erros esgotaram tentativas

    concluido --> [*]

    note right of pendente
        status='pendente'
        Aguardando Manager Lambda
    end note

    note right of em_andamento
        status='em_andamento'
        Possui execuções ativas
        Verificado a cada 15 min
    end note

    note right of concluido
        status='concluido'
        Todas páginas processadas
        ou erros permanentes
    end note
```

## 3. Fluxo de Estados da Execução (resultados_execucao)

```mermaid
stateDiagram-v2
    [*] --> em_andamento: Executor cria registro<br/>tentativa=1

    em_andamento --> concluido: API retorna sucesso<br/>página salva no DB

    em_andamento --> pendente_retry: Erro na API<br/>tentativa < max_tentativas<br/>incrementa tentativa

    em_andamento --> erro: Erro na API<br/>tentativa >= max_tentativas

    em_andamento --> erro: Finalizer detecta stale<br/>(sem update por 15+ min)

    pendente_retry --> em_andamento: Executor retry<br/>nova tentativa

    pendente_retry --> erro: Erro persistente<br/>tentativa >= max_tentativas

    concluido --> [*]
    erro --> [*]

    note right of em_andamento
        status='em_andamento'
        tentativa: 1-3
        Processando página
    end note

    note right of pendente_retry
        status='pendente_retry'
        Aguarda nova tentativa
        Executor faz retry interno
    end note

    note right of concluido
        status='concluido'
        total_itens registrado
        Página salva com sucesso
    end note

    note right of erro
        status='erro'
        tentativa >= max_tentativas
        ou timeout/crash detectado
    end note
```

## 4. Fluxo Completo do Sistema

```mermaid
flowchart TD
    Start([Usuário insere pesquisa]) --> DB1[(diario.pesquisas<br/>status=pendente)]

    DB1 --> Manager[Manager Lambda<br/>Every 20 min]

    Manager --> Split{Tipo de<br/>pesquisa?}

    Split -->|numero_processo| NP[Sem split por tribunal<br/>Um task por período]
    Split -->|termo_pesquisa| TP[Split por tribunal<br/>Um task por dia+tribunal]

    NP --> DetectorQ[DetectorQueue SQS]
    TP --> DetectorQ

    Manager --> UpdateStatus1[(UPDATE pesquisas<br/>status=em_andamento)]

    DetectorQ --> Detector[PageBatchDetector Lambda<br/>Max 200 concurrent]

    Detector --> API1{API Call<br/>Page 1}

    API1 -->|totalElements=0| NoBatch[Retorna batches=empty<br/>Não envia ao Executor]
    API1 -->|pages <= 15| SingleBatch[Retorna task original<br/>1 batch]
    API1 -->|pages > 15| MultiBatch[Split em batches<br/>15 páginas cada]

    SingleBatch --> ExecutorQ[ExecutorQueue SQS]
    MultiBatch --> ExecutorQ

    ExecutorQ --> Executor[Executor Lambda<br/>Max 500 concurrent]

    Executor --> CreateExec[(INSERT resultados_execucao<br/>status=em_andamento<br/>tentativa=1)]

    CreateExec --> PageLoop{Para cada<br/>página}

    PageLoop --> APICall[API Call com retry<br/>max 3 tentativas]

    APICall -->|Sucesso| SaveResults[(UPSERT processo<br/>UPSERT publicacoes<br/>INSERT destinatarios)]

    SaveResults --> UpdateExecOK[(UPDATE resultados_execucao<br/>status=concluido<br/>total_itens=N)]

    UpdateExecOK --> HasMore{Tem mais<br/>páginas?}

    APICall -->|Erro tentativa < 3| Retry[(UPDATE resultados_execucao<br/>status=pendente_retry<br/>tentativa++)]

    Retry --> APICall

    APICall -->|Erro tentativa = 3| UpdateExecErr[(UPDATE resultados_execucao<br/>status=erro<br/>erro_msg)]

    UpdateExecErr --> HasMore

    HasMore -->|Sim| PageLoop
    HasMore -->|Não| End1([Fim da execução])

    End1 --> Finalizer[Finalizer Lambda<br/>Every 15 min]

    Finalizer --> CheckStale{Executações stale?<br/>sem update 15+ min}

    CheckStale -->|Sim| MarkStale[(UPDATE resultados_execucao<br/>status=erro<br/>erro_msg=timeout)]

    MarkStale --> CheckComplete
    CheckStale -->|Não| CheckComplete{Todas execuções<br/>concluído ou erro?}

    CheckComplete -->|Sim| MarkComplete[(UPDATE pesquisas<br/>status=concluido)]
    CheckComplete -->|Não| KeepRunning[(Mantém em_andamento<br/>tem pendências)]

    MarkComplete --> EndFlow([Pesquisa finalizada])
    KeepRunning --> WaitNext([Aguarda próximo<br/>Finalizer])

    style DB1 fill:#e1f5ff
    style UpdateStatus1 fill:#e1f5ff
    style CreateExec fill:#e1f5ff
    style SaveResults fill:#e1f5ff
    style UpdateExecOK fill:#e1f5ff
    style UpdateExecErr fill:#e1f5ff
    style Retry fill:#fff4e1
    style MarkStale fill:#ffe1e1
    style MarkComplete fill:#e1ffe1
```

## 5. Uso dos Campos de Controle

### 5.1. Tabela `diario.pesquisas`

```mermaid
graph LR
    A[status] --> B{Valores}
    B -->|pendente| C[Aguardando Manager Lambda<br/>processamento ainda não iniciado]
    B -->|em_andamento| D[Manager enviou tasks<br/>execuções em progresso<br/>verificado pelo Finalizer]
    B -->|concluido| E[Todas execuções finalizadas<br/>ou erros permanentes]

    F[tribunais array] --> G{Valores}
    G -->|empty array| H[ALL_TRIBUNALS<br/>busca em 56 tribunais]
    G -->|array com valores| I[Tribunais específicos<br/>ex: TJSP, TJRJ]

    J[updated_at] --> K[Timestamp da última<br/>atualização de status<br/>usado para tracking]
```

### 5.2. Tabela `diario.resultados_execucao`

```mermaid
graph TD
    A[Campo: status] --> B{Valores}
    B -->|em_andamento| C[Executor processando<br/>tentativa atual ativa]
    B -->|concluido| D[Página processada<br/>resultados salvos<br/>total_itens registrado]
    B -->|erro| E[Todas tentativas falharam<br/>tentativa >= max_tentativas<br/>ou timeout detectado]
    B -->|pendente_retry| F[Aguarda retry interno<br/>Executor tentará novamente<br/>tentativa < max_tentativas]

    G[Campo: tentativa] --> H{Controle de Retry}
    H --> I[Valor: 1-3]
    I --> J[Incrementado a cada erro]
    J --> K{tentativa >= max_tentativas?}
    K -->|Sim| L[status = erro]
    K -->|Não| M[status = pendente_retry]

    N[Campo: updated_at] --> O{Usado por}
    O --> P[Finalizer: detecta stale<br/>NOW - updated_at > 15 min]
    O --> Q[Monitoring: identifica<br/>execuções travadas]

    R[Campo: tribunal] --> S{Valores especiais}
    S --> T[PROCESSO: busca por<br/>numero_processo<br/>sem split por tribunal]
    S --> U[TJSP, TRF1, etc:<br/>tribunal específico]
    S --> V[ALL_TRIBUNALS: label<br/>quando tribunais=empty array]
```

### 5.3. Campos de Controle de Paginação (task parameters)

```mermaid
graph LR
    A[page_start] --> B[Página inicial do batch<br/>default: 1<br/>usado quando > 15 páginas]
    C[page_end] --> D[Página final do batch<br/>default: 100<br/>evita timeout Lambda]

    E[PageBatchDetector] --> F{totalElements?}
    F -->|0| G[batches = empty<br/>não executa]
    F -->|pages <= 15| H[batches = task original<br/>page_start=1, page_end=None]
    F -->|pages > 15| I[batches = múltiplos tasks<br/>15 páginas cada]

    I --> J[Batch 1:<br/>page_start=1<br/>page_end=15]
    I --> K[Batch 2:<br/>page_start=16<br/>page_end=30]
    I --> L[Batch N:<br/>page_start=91<br/>page_end=100]
```

## 6. Padrões de Query Importantes

### 6.1. Verificar status de uma pesquisa

```sql
-- Resumo de execuções por status
SELECT
    status,
    COUNT(*) as count,
    SUM(total_itens) as total_items
FROM diario.resultados_execucao
WHERE pesquisa_id = :search_id
GROUP BY status;

-- Identificar execuções com problemas
SELECT
    tribunal,
    data_execucao,
    pagina,
    tentativa,
    erro_msg,
    EXTRACT(EPOCH FROM (NOW() - updated_at)) / 60 as minutes_since_update
FROM diario.resultados_execucao
WHERE pesquisa_id = :search_id
  AND status IN ('erro', 'em_andamento', 'pendente_retry')
ORDER BY tentativa DESC, updated_at DESC;
```

### 6.2. Detectar execuções stale (Finalizer)

```sql
-- Execuções travadas há mais de 15 minutos
SELECT
    id,
    tribunal,
    data_execucao,
    pagina,
    EXTRACT(EPOCH FROM (NOW() - updated_at)) / 60 as minutes_stale
FROM diario.resultados_execucao
WHERE pesquisa_id = :search_id
  AND status IN ('em_andamento', 'pendente_retry')
  AND updated_at < NOW() - INTERVAL '15 minutes';
```

### 6.3. Constraint único de execução

```sql
-- Constraint: unique_execucao_new
-- Garante uma execução por (pesquisa_id, tribunal, data_execucao, pagina)
-- Permite ON CONFLICT para upsert de execuções
UNIQUE (pesquisa_id, tribunal, data_execucao, pagina)
```

### 6.4. Upsert de publicações com pesquisas_ids

```sql
-- Adiciona pesquisa_id ao array se não existir
INSERT INTO diario.publicacoes
    (indice, pesquisas_ids, ...)
VALUES (:indice, ARRAY[:pesquisa_id]::BIGINT[], ...)
ON CONFLICT (indice) DO UPDATE SET
    pesquisas_ids = CASE
        WHEN :pesquisa_id = ANY(diario.publicacoes.pesquisas_ids)
        THEN diario.publicacoes.pesquisas_ids
        ELSE array_append(diario.publicacoes.pesquisas_ids, :pesquisa_id)
    END;
```

## 7. Características do Sistema de Controle

### 7.1. Retry Logic (3 tentativas)

```mermaid
sequenceDiagram
    participant E as Executor Lambda
    participant DB as resultados_execucao
    participant API as ComunicaPJE API

    E->>DB: INSERT (status=em_andamento, tentativa=1)

    loop Tentativa 1-3
        E->>API: GET /comunicacao
        alt Sucesso
            API-->>E: 200 OK + items
            E->>DB: UPDATE (status=concluido, total_itens=N)
        else Erro e tentativa < 3
            API-->>E: Error
            E->>DB: UPDATE (status=pendente_retry, tentativa++)
            Note over E,API: Retry interno imediato
        else Erro e tentativa = 3
            API-->>E: Error
            E->>DB: UPDATE (status=erro, erro_msg)
            Note over E,DB: Erro permanente
        end
    end
```

### 7.2. Stale Detection (Finalizer)

```mermaid
sequenceDiagram
    participant F as Finalizer Lambda
    participant DB as Database
    participant P as diario.pesquisas

    Note over F: Executa a cada 15 min

    F->>P: SELECT WHERE status=em_andamento

    loop Para cada pesquisa
        F->>DB: SELECT execuções WHERE<br/>status IN (em_andamento, pendente_retry)<br/>AND updated_at < NOW() - 15min

        alt Tem execuções stale
            F->>DB: UPDATE status=erro<br/>erro_msg="timeout detected"
        end

        F->>DB: SELECT COUNT(*) GROUP BY status

        alt Todas concluído ou erro
            F->>P: UPDATE status=concluido
        else Tem pendências
            Note over F,P: Mantém em_andamento
        end
    end
```

### 7.3. Rate Limiting via SQS

```mermaid
graph TD
    A[Manager Lambda] -->|Max 10 concurrent| B[DetectorQueue SQS]
    B -->|MaxConcurrency: 200| C[PageBatchDetector Lambda]
    C -->|Batches| D[ExecutorQueue SQS]
    D -->|MaxConcurrency: 500| E[Executor Lambda]

    style B fill:#fff4e1
    style D fill:#fff4e1

    Note1[Evita Lambda throttling<br/>Account limit: 1250] -.-> E
    Note2[Evita API rate limiting<br/>ComunicaPJE] -.-> E
```

## 8. Exemplo de Execução Completa

### Cenário: Pesquisa ALL_TRIBUNALS por 1 mês

```mermaid
gantt
    title Timeline de Execução - Pesquisa 20151 (ALL_TRIBUNALS, 30 dias)
    dateFormat HH:mm
    axisFormat %H:%M

    section Manager
    Busca pesquisas pendentes    :00:00, 1m
    Split 56 tribunais x 30 dias  :00:01, 2m
    Envia 1680 tasks (DetectorQ)  :00:03, 5m
    UPDATE status=em_andamento    :00:08, 1m

    section Detector (200 concurrent)
    Processa tasks do DetectorQ   :00:09, 30m
    Chama API page 1 por task     :00:10, 29m
    Envia batches ao ExecutorQ    :00:15, 24m

    section Executor (500 concurrent)
    Processa batches do ExecutorQ :00:20, 120m
    Salva resultados página a página :00:25, 115m
    Cria/atualiza resultados_execucao :00:25, 115m

    section Finalizer
    1ª verificação (15 min)       :00:15, 1m
    Mantém em_andamento           :00:16, 1m
    2ª verificação (30 min)       :00:30, 1m
    Mantém em_andamento           :00:31, 1m
    3ª verificação (após Executor):02:25, 1m
    Marca concluido               :02:26, 1m
```

**Estatísticas do exemplo:**
- **Pesquisa:** termo_pesquisa="precatório", tribunais=[], 30 dias
- **Tasks gerados:** 56 tribunais × 30 dias = 1,680 tasks
- **Tempo total:** ~2.5 horas (processamento paralelo)
- **Execuções criadas:** 1,680 × média de 3 páginas/dia = ~5,000 execuções
- **Resultados:** ~50,000 publicações encontradas
