# 📄 Documentação Técnica: Piloto Agente Autônomo ALESC

## 1. Visão Geral (O que é o sistema?)
O **Agente Autônomo de Helpdesk** é uma solução de inteligência artificial desenvolvida para a Assembleia Legislativa de Santa Catarina (ALESC). Ele atua como uma primeira camada de suporte, capaz de interpretar dúvidas dos servidores e fornecer soluções técnicas instantâneas para problemas comuns, como dificuldades no sistema SGP ou no uso de tokens de assinatura digital.

---

## 2. Arquitetura do Sistema (Como ele funciona?)

Para ser inteligente e rápido ao mesmo tempo, o sistema utiliza uma técnica avançada chamada **RAG (Geração Aumentada de Recuperação)**. Isso significa que a IA não "chuta" as respostas; ela primeiro consulta os manuais da ALESC e depois explica o conteúdo para o usuário.

### Os Três Componentes Principais:
1.  **O Cérebro (Google Gemini Flash Latest):** - Utilizamos o modelo mais moderno e rápido do Google (versão 2026). Ele é responsável por ler a dúvida do usuário e transformar os manuais técnicos em uma conversa amigável e fácil de entender.
    
2.  **A Biblioteca Digital (FAISS - Busca Semântica):** - Em vez de uma busca simples por palavras-chave, o sistema entende o *sentido* da pergunta. Ele converte os manuais em "vetores" (coordenadas numéricas), permitindo encontrar a solução correta mesmo que o usuário use palavras diferentes das do manual.

3.  **O Cartório de Registros (Google Firebase):** - Cada interação é gravada em um banco de dados em nuvem. Isso permite monitorar o tempo de resposta e quais problemas são mais frequentes, gerando dados para a gestão da TI.

---

## 3. Fluxo de Funcionamento

1.  **Pergunta:** O servidor digita o problema (ex: "SGP não reconhece meu certificado").
2.  **Recuperação:** O sistema busca na base de conhecimento local a solução técnica para "SGP" e "Token".
3.  **Síntese:** A IA recebe a solução técnica bruta e a transforma em um passo a passo organizado.
4.  **Resposta:** O usuário recebe a solução na tela.
5.  **Registro:** O sistema salva o log do atendimento no Firebase, incluindo o tempo de processamento.



---

## 4. Performance e Eficiência
O sistema foi calibrado para priorizar a agilidade no atendimento:
- **Tempo Médio de Resposta:** ~5.5 segundos.
- **Protocolo de Comunicação:** Modo REST (garante estabilidade em redes corporativas).
- **Limite de Resposta:** Configurado para 800 tokens, garantindo respostas diretas e sem "enrolação".

---

## 5. Segurança e Governança
- **Privacidade:** O sistema não envia dados sensíveis ou pessoais para treinamento da IA. Apenas a dúvida técnica é processada.
- **Independência:** A base de conhecimento é local. Se uma regra de suporte mudar, basta alterar um arquivo interno e a IA se atualiza imediatamente, sem necessidade de novo treinamento.

---

## 6. Glossário Simples para Gestores
- **LLM:** O motor de linguagem (IA) que permite a conversa.
- **Token:** Unidade de medida de texto para a IA (como se fossem sílabas).
- **Prompt:** A instrução ou comando dado à IA para definir seu comportamento.
- **Interface Streamlit:** A página web amigável onde o usuário interage com o sistema.