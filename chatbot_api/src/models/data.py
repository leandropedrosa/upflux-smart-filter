import json

# Defina o JSON fornecido
data_structure = [
    {
        'key': 'type',
        'description': 'Define o tipo de análise ou dado',
        'values': [
            {
                'name': 'agci',
                'description': 'Análise de gestão do ciclo de pedido'
            },
            {
                'name': 'tempo',
                'description': 'Análise de tempo'
            }
        ]
    },
    {
        'key': 'context_name',
        'description': 'Nome do contexto',
        'values': [
            {
                'name': 'O2C',
                'description': 'Order to Cash'
            }
        ]
    },
    {
        'key': 'dashboard',
        'description': 'Representa a forma de visualização dos dados',
        'values': [
            {
                'name': 'Generic',
                'description': 'Dados a partir de perguntas mais genéricas e amplas'
            },
            {
                'name': 'Visão Geral',
                'description': 'Dados a partir de perguntas que remete ao todo'
            },
            {
                'name': 'Análise do Ciclo da Ordem de Venda',
                'description': 'Dados a partir de perguntas similares a Análise do Ciclo da Ordem de Venda'
            },
            {
                'name': 'Análise de Recebimento de pagamentos',
                'description': 'Dados a partir de perguntas similares a Análise de Recebimento de pagamentos'
            },
            {
                'name': 'Ordem de Venda Perfeita (Perfect SO)',
                'description': 'Dados a partir de perguntas similares a Ordem de Venda Perfeita (Perfect SO)'
            },
            {
                'name': 'Envios no prazo (on-time shipment)',
                'description': 'Dados a partir de perguntas similares a Envios no prazo (on-time shipment)'
            },
            {
                'name': 'Operação contas a receber',
                'description': 'Dados a partir de perguntas similares a Operação contas a receber'
            },
            {
                'name': 'Análise de automação',
                'description': 'Dados a partir de perguntas similares a Análise de automação'
            },
            {
                'name': 'Impacto na Receita',
                'description': 'Dados a partir de perguntas similares a Impacto na Receita'
            }
        ]
    },
    {
        'key': 'user_requested_unit',
        'description': 'Unidade solicitada pelo usuário',
        'values': [
            {
                'name': 'porcentagem',
                'description': 'Representação em porcentagem'
            },
            {
                'name': 'tempo',
                'description': 'Representação em unidades de tempo'
            }
        ]
    },
    {
        'key': 'mode',
        'description': 'Modo de análise',
        'values': [
            {
                'name': 'casos interligados',
                'description': 'Análise de casos interligados'
            }
        ]
    },
    {
        'key': 'DATE',
        'description': 'Intervalo de datas',
        'values': [
            {
                'name': '01/01/2023-30/06/2023',
                'description': 'Período de análise de janeiro a junho de 2023'
            }
        ]
    },
    {
        'key': 'start_date',
        'description': 'Data de início do período',
        'values': [
            {
                'name': '2023-01-01',
                'description': 'Data inicial para a análise'
            }
        ]
    },
    {
        'key': 'end_date',
        'description': 'Data de fim do período',
        'values': [
            {
                'name': '2023-06-30',
                'description': 'Data final para a análise'
            }
        ]
    }
]

data_structure = json.dumps(data_structure, ensure_ascii=False)

data_out = [
    {
        "type": "",
        "context_name": "",
        "dashboard": "",
        "main_keywords": [
            ""
        ],
        "user_requested_unit": ""
    },
    {
        "type": "",
        "mode": "",
        "DATE": "DD/MM/YYYY-DD/MM/YYYY",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }
]

# Converta o JSON para uma string
data_output = json.dumps(data_out, ensure_ascii=False)