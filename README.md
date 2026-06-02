# Integration Hub

## Visão Arquitetural e Tecnologias

A arquitetura garante o isolamento do domínio de negócio das dependências de infraestrutura, facilitando a manutenção e a escalabilidade.


---
| **Aspecto** | **Tecnologia/Prática** |
| :---: | :--- | 
|**Padrões de Projeto:**  |Clean Architecture, DDD, Princípio Aberto-Fechado (OCP), ProviderFactory. |
|**Web Framework:**  |FastAPI (I/O assíncrono nativo). |
| **Banco de Dados:** |PostgreSQL (Conformidade ACID). |
| **ORM:** |SQLAlchemy (Isolado na camada de infraestrutura/repositórios). |
----



## Justificativas Técnicas:

* **Isolamento do Domínio:** 
    - As regras de negócio (validação, estados) são desenvolvidas em Python puro, garantindo alta testabilidade sem acoplamento ao FastAPI ou SQLAlchemy.
* **Extensibilidade (OCP):** 
    - Novos provedores (ERP, CRM) são integrados via novos Adapters de infraestrutura que implementam interfaces do domínio, preservando a camada de Casos de Uso intacta.
* **Processamento:** 
    - Operações assíncronas via `httpx` para requisições externas não bloqueantes. O modelo suporta evolução para filas (Celery/RabbitMQ) em cargas pesadas.


## Requisitos do Sistema

### Requisitos Funcionais (RF)
* **RF01:** Gerenciar usuários, papéis (Roles) e permissões de acesso.
* **RF02:** Cadastrar e gerenciar conexões com provedores externos (ERP, CRM, APIs).
* **RF03:** Configurar fluxos de integração (origem, destino, regras de roteamento).
* **RF04:** Suportar transformação de **payloads** entre os formatos de origem e destino.
* **RF05:** Executar integrações sob demanda ou de forma agendada.
* **RF06:** Registrar o histórico completo das execuções (sucesso, falha, tempo de processamento).
* **RF07:** Executar mecanismo de retry automático configurável para falhas transientes.
* **RF08:** Manter trilha de auditoria para alterações em configurações sensíveis.

---
### Requisitos Não Funcionais (RNF)

| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| **RNF01** | Desempenho | A API REST deve responder em < 200ms para operações CRUD e configurações. |
| **RNF02** | Escalabilidade | Processamento assíncrono com suporte nativo a escalabilidade horizontal. |
| **RNF03** | Segurança | Credenciais criptografadas (ex: AES-256) por design; Autenticação via JWT. |
| **RNF04** | Extensibilidade | Implementação de novos provedores baseada em contratos (OCP). |
| **RNF05** | Observabilidade | Exportação de métricas (Health Check) e rastreabilidade via Structured Logging. |
---

### Atores e Casos de Uso

| Ator | Descrição | Casos de Uso Vinculados |
| :--- | :--- | :--- |
| **Administrador** | Gerencia usuários, permissões e configurações globais. | UC04, UC05 |
| **Engenheiro de Integração** | Configura conexões, mapeamentos e fluxos de roteamento. | UC01, UC02, UC04 |
| **Sistema Externo** | Entidades de origem/destino que trafegam dados no Hub. | UC03 |

**Principais Casos de Uso (UC):**
* **UC01:** Configurar Nova Conexão (Provider).
* **UC02:** Definir Fluxo de Roteamento e Transformação.
* **UC03:** Disparar Execução de Integração.
* **UC04:** Consultar Histórico e Logs de Execução.
* **UC05:** Gerenciar Credenciais Criptografadas.

---

## Modelo de Domínio (DDD)

### Agregados e Raízes de Agregação (Aggregate Roots)
* **IntegrationFlow (Raiz):** Configuração da rota entre ponto A e B. Agrupa `TransformationRule` e `RetryPolicy`.
* **Connection (Raiz):** Vínculo com sistema externo. Agrupa `ConnectionCredentials`.
* **Execution (Raiz):** Instância ativa de um `IntegrationFlow`. Agrupa `ExecutionLogs`.

### Entidades e Objetos de Valor (Value Objects)
* **Entidades:** `User` (Identidade), `Role` (Permissões), `AuditLog` (Registro imutável).
* **Value Objects:** `Payload` (Estrutura imutável de dados em trânsito), `IntegrationStatus` (PENDING, PROCESSING, SUCCESS, FAILED, RETRYING), `ConnectionCredentials` (Dados de autenticação mascarados/criptografados).

### Regras de Negócio Core
1.  Uma `Execution` não pode transitar dos estados SUCCESS/FAILED para PENDING.
2.  Um `IntegrationFlow` só é ativado com conexões de origem e destino validadas por Health Check.
3.  A transformação do `Payload` é estritamente agnóstica à sua origem, orientada a contratos.

---

## Modelo de Dados (PostgreSQL)

### Tabelas de Acesso
* `users`, `roles`, `user_roles`

### Tabelas de Integração
* `connections` (id, name, provider_type, encrypted_config, created_at)
* `integration_flows` (id, name, source_connection_id, target_connection_id, transformation_schema, is_active)

### Tabelas de Operação
* `executions` (id, flow_id, status, started_at, finished_at, retry_count)
* `execution_logs` (id, execution_id, log_level, message, timestamp)
* `audit_logs` (id, user_id, action, resource, timestamp)

---


## Diagramas UML

Arquitetura da Solução e Justificativas Técnicas
A arquitetura escolhida é fundamentada na Clean Architecture combinada com Domain-Driven Design (DDD).

## casos de uso
<img src="img_arq_readme/use_cases.png" alt="Diagrama de Arquitetura"  align="center" width="390"/>

## Diagrama de Classes
<img src="img_arq_readme/classes_diagram.png" alt="Diagrama de Arquitetura"  align="center" width="390"/>

## Diagrama de Componentes
<img src="img_arq_readme/components_diagram.png" alt="Diagrama de Arquitetura"  align="center" width="390"/>

---

## Justificativas:

* **Isolamento do Domínio**: As regras de negócio (validação de fluxo, controle de estado de execução) são escritas em Python puro, sem dependência do FastAPI ou do SQLAlchemy. Isso garante testabilidade e manutenção a longo prazo.

* **Princípio Aberto-Fechado (OCP)**: O roteamento e o consumo de APIs externas serão baseados em um `ProviderFactory`. Para adicionar um novo ERP ou CRM, criaremos um novo Adapter na camada de infraestrutura que implementa a interface de provedor do domínio, sem alterar os Casos de Uso.

* **Processamento e Desempenho**: FastAPI permite `I/O assíncrono nativo`. Para integrações pesadas, a camada de aplicação delegará o trabalho para filas (pode ser introduzido um Celery/RabbitMQ no futuro, mas inicialmente a modelagem suporta async via HTTPX para as requisições externas de forma não bloqueante).

* **Gestão de Estado**: O uso do `PostgreSQL` com `SQLAlchemy` como ORM será restrito à camada de Repositórios (Infrastructure Layer). A camada de domínio não conhecerá modelos do SQLAlchemy, apenas Entidades e Pydantic models.


## Estrutura esperada do projeto


```
integration_hub/
├── alembic/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   ├── value_objects/
│   │   └── interfaces/
│   ├── application/
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   └── services/
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   ├── repositories/
│   │   ├── providers/
│   │   └── logging/
│   └── presentation/
│       ├── __init__.py
│       ├── api/
│       ├── middlewares/
│       └── schemas/
├── tests/
├── alembic.ini
├── main.py
└── requirements.txt
```

## Definição da Estrutura de Diretórios:

A arquitetura é dividida em quatro camadas principais independentes: 
- **Domain** ------- (núcleo agnóstico), 
- **Application** --- (casos de uso e orquestração), 
- **Infrastructure** - (adaptadores, banco de dados, clientes HTTP) 
- **Presentation**  -- (roteamento FastAPI e schemas de entrada/saída).


## Contratos do Domínio e Estratégia de Extensibilidade

### Definição de Interfaces do Provedor e Factory
 - A estratégia de extensibilidade baseia-se no Princípio Aberto-Fechado (OCP). O domínio define o contrato que qualquer provedor externo deve implementar e a assinatura do Factory Pattern. Novos provedores são adicionados à infraestrutura sem modificar as regras de negócio core.
