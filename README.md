# 🛡️ Agente Autônomo de Suporte ALESC (V1.5)
**Ecossistema de Inteligência Artificial para Automação de Suporte Nível 1**

Este projeto representa uma solução de **Inteligência Operacional** desenhada especificamente para a Assembleia Legislativa de Santa Catarina. Ele utiliza uma arquitetura de ponta para converter a base de conhecimento técnica em um agente autônomo, garantindo que o suporte seja ágil, organizado e auditável.

## 🚀 Performance e Métricas de Sucesso
- **Latência de Resposta:** Média de **~5.5 segundos**.
- **Confiabilidade:** Arquitetura RAG que elimina "alucinações" ao restringir a IA à base de conhecimento oficial.
- **Modelo Core:** Google Gemini Flash Latest (`models/gemini-flash-latest`).
- **Disponibilidade:** Operação 24/7 com transbordo inteligente para suporte humano.

---

## 🏗️ Arquitetura de Engenharia de Software
O sistema é fundamentado no padrão **RAG (Retrieval-Augmented Generation)**, separando a lógica de processamento da base de dados para garantir escalabilidade e manutenção simplificada.

### 1. Fluxo de Interação e Sequência
O fluxo detalha a jornada da informação: desde a entrada do dado pelo servidor até a persistência final no Firebase para auditoria e gestão.



### 2. Pipeline de Inteligência (Engine RAG)
O motor utiliza **Embeddings** para busca semântica, permitindo que o Agente compreenda a intenção do usuário em vez de apenas comparar palavras isoladas.
1. **Extração de Contexto:** Uso de **FAISS** para localização ultrarrápida de soluções.
2. **Aumentação de Contexto:** Injeção das regras de negócio no prompt da LLM.
3. **Persistência de Dados:** Registro imutável de cada interação para governança técnica.



---

## 📋 Modelo de Negócio e Casos de Uso
O projeto foi estruturado para atender aos requisitos de governança pública, com atores e processos claramente definidos.

### Atores e Matriz de Responsabilidade
* **Servidor (Usuário):** Busca autonomia para resolver incidentes técnicos (SGP, Senhas, Drivers).
* **Agente IA (Nível 1):** Orquestra a resposta técnica baseada na base de conhecimento.
* **Técnico N2 (Suporte Humano):** Intervém via protocolo quando a complexidade excede a base da IA.
* **Gestor de TI (Auditor):** Monitora KPIs de resolução e identifica lacunas de conhecimento no Dashboard.



### Casos de Uso Críticos
- **UC01 - Resolução Autônoma:** O servidor encontra a solução e valida o sucesso (✅).
- **UC02 - Escalabilidade Técnica:** A IA falha, gera um protocolo de atendimento e salva o log contextual para o técnico humano.
- **UC03 - Auditoria de Business Intelligence:** O Gestor mapeia sistemas com maior índice de erros para melhorias preventivas.

---

## 🛠️ Tecnologias e Modelo de Dados
A persistência foi desenhada para ser compatível com ferramentas de Analytics e auditoria forense de chamados.

### Modelo de Dados (Schema Firestore)
| Campo | Descrição Técnica | Função no BI |
| :--- | :--- | :--- |
| **usuario** | Nome/ID do Servidor | Rastreabilidade do solicitante. |
| **relato** | Input bruto do problema | Análise de tendências e falhas comuns. |
| **resposta** | Solução gerada pela IA | Auditoria de qualidade e precisão. |
| **sistema** | Classificador automático | Identificação de gargalos por software. |
| **resolvido** | Indicador binário (KPI) | Métrica principal de eficácia da IA. |
| **protocolo** | Chave única de transbordo | Integração com sistema de chamados. |



---

## ⚙️ Instalação e Manutenção
1. **Configuração Inicial:**
   - Clone o repositório.
   - Crie um arquivo `.env` com sua `GOOGLE_API_KEY`.
   - Adicione o arquivo JSON de credenciais do Firebase na raiz do projeto.
2. **Dependências:** Execute `pip install -r requirements.txt` (Ambiente Python 3.9 recomendado).
3. **Execução:** Utilize o comando `streamlit run app.py`.

### Ciclo de Manutenção Ágil
Para evoluir o conhecimento da IA, não é necessário alterar o código-fonte. Basta atualizar o arquivo `base_conhecimento.py` com os novos procedimentos técnicos. O Agente reindexará as informações automaticamente no próximo carregamento, seguindo os princípios de **metodologia ágil**.