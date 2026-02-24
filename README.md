# 🛡️ Agente Autônomo de Suporte ALESC (V1.5)
**Ecossistema de Inteligência Artificial para Automação de Suporte Nível 1**

Este projeto é uma solução de **Inteligência Operacional** desenvolvida para a Assembleia Legislativa de Santa Catarina (ALESC). Ele atua como uma primeira camada de suporte inteligente, capaz de interpretar dúvidas dos servidores e fornecer soluções técnicas instantâneas para sistemas críticos (SGP, Tokens, Assinatura Digital).

---

## 1. Visão Estratégica e Modelo de Negócio
O Agente Autônomo não "chuta" respostas; ele utiliza a técnica avançada **RAG (Retrieval-Augmented Generation)** para consultar manuais oficiais antes de interagir.

### 🚀 Performance e Eficiência
- **Tempo Médio de Resposta:** ~5.5 segundos.
- **Protocolo:** Modo REST para máxima estabilidade em redes corporativas.
- **Limite de Resposta:** 800 tokens (respostas diretas e sem "enrolação").
- **Modelo Core:** Google Gemini Flash Latest (Versão 2026).

---

## 2. Arquitetura do Sistema (Componentes)

O sistema é sustentado por três pilares tecnológicos que garantem inteligência e rastreabilidade:

1. **O Cérebro (Google Gemini Flash):** Responsável por processar a linguagem natural e transformar manuais técnicos em conversas amigáveis e organizadas.
2. **A Biblioteca Digital (FAISS - Busca Semântica):** Converte manuais em "vetores" (coordenadas numéricas). Isso permite que o sistema entenda o **sentido** da pergunta, mesmo que o usuário use palavras diferentes das do manual.
3. **O Cartório de Registros (Google Firebase):** Cada interação é gravada em nuvem, permitindo auditoria, monitoramento de desempenho e geração de dados para a gestão de TI.



---

## 3. Fluxo de Funcionamento e Casos de Uso

### Ciclo de Atendimento
1. **Pergunta:** O servidor relata o problema (ex: "SGP não reconhece meu certificado").
2. **Recuperação:** O sistema busca na base local a solução técnica específica.
3. **Síntese:** A IA recebe o dado bruto e o organiza em um passo a passo.
4. **Resposta:** O usuário recebe a solução e valida a eficácia.
5. **Registro:** O log é salvo no Firebase com status (✅/❌) e tempo de processamento.



### Atores e Governança
- **Servidor:** O solicitante que busca autonomia.
- **Técnico N2:** Intervém apenas quando o Agente gera um protocolo de transbordo.
- **Gestor de TI:** Utiliza o Dashboard para identificar lacunas de conhecimento e gargalos nos sistemas.



---

## 4. Segurança e Governança
- **Privacidade:** O sistema não envia dados sensíveis ou pessoais para treinamento da IA. Apenas a dúvida técnica é processada.
- **Independência:** A base de conhecimento é local. Alterações em manuais são refletidas instantaneamente sem necessidade de novo treinamento do modelo.

### Modelo de Dados (Schema Firestore)
| Campo | Descrição | Importância |
| :--- | :--- | :--- |
| `usuario` | Nome do Servidor | Rastreabilidade. |
| `relato` | Dúvida original | Análise de tendências de suporte. |
| `resposta` | Solução da IA | Auditoria de qualidade. |
| `sistema` | Tag de Software | Mapeamento de gargalos (ex: SGP). |
| `resolvido` | Status ✅/❌ | KPI de eficiência da automação. |

---

## 5. Glossário para Gestores
- **LLM:** O motor de inteligência que permite a conversa fluida.
- **Token:** Unidade de medida de texto (aproximadamente uma sílaba).
- **Prompt:** Comando dado à IA para definir seu comportamento e limites.
- **Interface Streamlit:** A página web onde ocorre a interação com o servidor.

---

## ⚙️ Instalação e Manutenção Ágil
1. Clone o repositório.
2. Configure o arquivo `.env` com a `GOOGLE_API_KEY`.
3. Adicione as credenciais do Firebase na raiz.
4. Execute: `pip install -r requirements.txt`.
5. Inicie: `streamlit run app.py`.

**Nota de Manutenção:** Para atualizar a IA, basta editar o arquivo `base_conhecimento.py`. O sistema utiliza Metodologias Ágeis para garantir que a atualização seja instantânea.