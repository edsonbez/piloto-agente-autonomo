# base_conhecimento.py

SOLUCOES_CONHECIDAS = [
    # --- SISTEMA LEGISLATIVO (SGP / PROCESSO DIGITAL) ---
    {
        # Adicionado "sgp" para garantir o bônus de autoridade
        "palavras_chave": ["sgp", "token", "certificado", "assinatura", "não reconhece", "pendrive", "assinar", "leitora", "cartão", "safenet", "epass"], 
        "sistema": "SGP", 
        "resposta": "Olá! Identifiquei uma dificuldade com a sua assinatura digital. Geralmente, isso ocorre quando o sistema não detecta o dispositivo. Por favor, verifique se o driver da SafeNet/ePass está atualizado e se o token está bem encaixado na porta USB."
    },
    {
        "palavras_chave": ["anexar", "tamanho", "mb", "limite", "muito grande", "subir arquivo", "pdf pesado", "comprimir"], 
        "sistema": "SGP", 
        "resposta": "Compreendo. O sistema SGP possui um limite de 10MB por arquivo. Utilize a ferramenta 'Otimizador de PDF' ou divida o arquivo original em partes menores."
    },
    {
        "palavras_chave": ["numeração", "projeto", "duplicado", "número", "errado", "sequência", "cronologia"], 
        "sistema": "SGP", 
        "resposta": "Notei um conflito na numeração sequencial. É necessário que o setor de Apoio Legislativo realize um reset manual (ramal 1234)."
    },
    {
        "palavras_chave": ["voto", "relator", "comissão", "parecer", "votação", "pauta", "comissões"], 
        "sistema": "SGP", 
        "resposta": "Para registrar voto ou parecer, o processo precisa estar 'Em Relatoria'. Verifique a designação do relator no sistema."
    },

    # --- RH E PORTAL DO SERVIDOR ---
    {
        "palavras_chave": ["bloqueado", "senha", "acesso", "portal", "entrar", "não consigo logar", "login", "esqueci", "recuperar"], 
        "sistema": "RH", 
        "resposta": "O Portal do Servidor bloqueia o acesso por 30 minutos após três tentativas incorretas. Utilize a função 'Recuperar Senha'."
    },
    {
        "palavras_chave": ["margem", "consignado", "empréstimo", "banco", "parcela", "financeira"], 
        "sistema": "RH", 
        "resposta": "A reserva de margem é atualizada mensalmente. Consulte os valores no extrato dentro do Portal do Servidor."
    },
    {
        "palavras_chave": ["ponto", "justificativa", "atestado", "anexo", "falta", "batida", "esquecimento", "biometria", "frequência"], 
        "sistema": "RH", 
        "resposta": "Justificativas de ponto devem ser digitalizadas em PDF e anexadas no módulo 'Frequência' em até 48 horas."
    },
    {
        "palavras_chave": ["férias", "interromper", "convocação", "marcar férias", "calendário", "agendar", "gozo", "periodo"], 
        "sistema": "RH", 
        "resposta": "O agendamento de férias deve respeitar o cronograma do seu setor e ser validado via Portal do Servidor."
    },
    {
        "palavras_chave": ["contracheque", "holerite", "salário", "pagamento", "recibo", "folha", "rendimentos", "comprovante"], 
        "sistema": "RH", 
        "resposta": "Seu contracheque está disponível no Portal do Servidor. Verifique se o navegador está bloqueando pop-ups."
    },

    # --- FINANCEIRO (SIGEF / DIÁRIAS / EMPENHOS) ---
    {
        "palavras_chave": ["empenho", "nota", "liquidação", "financeiro", "pagar", "fornecedor", "pagamento"], 
        "sistema": "Financeiro", 
        "resposta": "O processo está em fase de liquidação. O prazo médio para o pagamento é de até 5 dias úteis."
    },
    {
        "palavras_chave": ["diária", "prestação de contas", "viagem", "ajuda de custo", "hotel", "reembolso", "deslocamento", "roteiro"], 
        "sistema": "Financeiro", 
        "resposta": "A prestação de contas de viagem deve ser concluída em até 5 dias após o retorno. Anexe todos os comprovantes."
    },
    {
        "palavras_chave": ["sigef", "perfil", "unidade gestora", "ug", "permissão", "módulo", "execução", "gestor"], 
        "sistema": "Financeiro", 
        "resposta": "Erro de permissão no SIGEF. Solicite a liberação para sua Unidade Gestora (UG) ao ordenador de despesas."
    },

    # --- INFRAESTRUTURA E TI GERAL ---
    {
        "palavras_chave": ["outlook", "caixa", "cheia", "limite", "email", "e-mail", "correio", "mensagens", "lotada"], 
        "sistema": "TI", 
        "resposta": "Sua caixa de e-mail atingiu o limite. Mova itens antigos para um arquivo .pst ou limpe a lixeira."
    },
    {
        "palavras_chave": ["impressora", "toner", "papel", "encravado", "imprimir", "cópia", "xerox", "scannear"], 
        "sistema": "TI", 
        "resposta": "Para problemas físicos em impressoras, abra um chamado no ramal 9999 informando o número de série."
    },
    {
        "palavras_chave": ["vpn", "remoto", "casa", "conexão", "acesso externo", "home office", "forticlient"], 
        "sistema": "TI", 
        "resposta": "Utilize o software FortiClient com a VPN da ALESC. Verifique se sua senha de rede expirou."
    },

    # --- OUTROS SERVIÇOS (EVENTOS / SAÚDE / SEGURANÇA) ---
    {
        "palavras_chave": ["reserva", "reservar", "plenarinho", "auditório", "agendar", "sala", "espaço", "eventos"], 
        "sistema": "Eventos", 
        "resposta": "Utilize o Sistema de Agendamento de Espaços no Portal. Se necessário, contate a Coordenadoria de Eventos."
    },
    {
        "palavras_chave": ["unimed", "plano de saúde", "carência", "guia", "médico", "consultas", "carteirinha"], 
        "sistema": "Saúde", 
        "resposta": "Dúvidas sobre o plano Unimed podem ser resolvidas na Coordenadoria de Saúde ou no balcão de atendimento no hall."
    },
    {
        "palavras_chave": ["estacionamento", "vaga", "garagem", "crachá", "tag", "veículo", "entrada"], 
        "sistema": "Segurança", 
        "resposta": "O acesso às garagens é via crachá funcional. Para novas TAGs, procure a Coordenadoria de Segurança."
    }
]