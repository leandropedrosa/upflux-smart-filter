from langchain.schema import Document

docs = [
    Document(
        page_content="Representa um momento específico no tempo, identificado por dia, mês e ano.",
        metadata={
            "key": "DATE",
            "values": [
                "em abril de 2023",
                "em maio de 2023",
                "de janeiro de 2023 até junho de 2023",
                "de fevereiro de 2023 até junho de 2023"
            ],
            "example_answer": [
                {"DATE": "01/01/2023-30/06/2023"}
            ]
        }
    ),
    Document(
        page_content="A frequência de tempo denota a regularidade de eventos em um período específico.",
        metadata={
            "key": "FREQUENCY",
            "values": [
                "mensal"
            ],
            "example_answer": [
                {"FREQUENCY": "mensal"}
            ]
        }
    ),
    Document(
        page_content="É a organização de itens com características comuns, diferenciando elementos dentro de um sistema.",
        metadata={
            "key": "CATEGORY",
            "values": [
                "canal de distribuição",
                "grupo de clientes",
                "organização de vendas",
                "Tipo de material",
                "Clientes",
                "Tipo de transporte"
            ],
            "example_answer": [
                {"CATEGORY": "Tipo de transporte"}
            ]
        }
    ),
    Document(
        page_content="Documento que formaliza acordo entre vendedor e comprador para produtos/serviços.",
        metadata={
            "key": "SALESORDER",
            "values": [
                "itens de ordens de vendas",
                "ordens",
                "pedidos",
                "OV"
            ],
            "example_answer": [
                {"SALESORDER": "OV"}
            ]
        }
    ),
    Document(
        page_content="Conjunto interconectado de componentes para automação comercial, melhorando eficiência e gestão.",
        metadata={
            "key": "SYSTEM",
            "values": [
                "automação"
            ],
            "example_answer": [
                {"SYSTEM": "automação"}
            ]
        }
    ),
    Document(
        page_content="A quantidade acumulada de bens/materiais mantida pela empresa para atender futuras demandas.",
        metadata={
            "key": "STOCK",
            "values": [
                "itens"
            ],
            "example_answer": [
                {"STOCK": "itens"}
            ]
        }
    ),
    Document(
        page_content="Registro financeiro, como uma fatura, que detalha transações e auxilia na contabilidade e decisões financeiras.",
        metadata={
            "key": "FINANCIALDOCUMENT",
            "values": [
                "itens pagos",
                "faturas"
            ],
            "example_answer": [
                {"FINANCIALDOCUMENT": "faturas"}
            ]
        }
    ),
    Document(
        page_content="Indica o status de transações financeiras, como 'pago', 'pendente', 'atrasado', 'em aberto', ou 'em disputa'.",
        metadata={
            "key": "PAYMENTSTATUS",
            "values": [
                "a receber",
                "em atraso"
            ],
            "example_answer": [
                {"PAYMENTSTATUS": "em atraso"}
            ]
        }
    ),
    Document(
        page_content="Eventos de logística na gestão da cadeia de suprimentos, como recebimento de remessas e rastreamento, essenciais para eficiência e entregas.",
        metadata={
            "key": "LOGISTICSEVENT",
            "values": [
                "envios"
            ],
            "example_answer": [
                {"LOGISTICSEVENT": "envios"}
            ]
        }
    ),
    Document(
        page_content="Unidades de medida de tempo, como segundo, minuto, hora, dia, semana, mês e ano, para quantificar a duração de eventos ou intervalos em diferentes escalas.",
        metadata={
            "key": "TIMEUNIT",
            "values": [
                "horas"
            ],
            "example_answer": [
                {"TIMEUNIT": "horas"}
            ]
        }
    ),
    Document(
        page_content="Indicador financeiro, como o DSO (Dias de Vendas em Aberto), que mede o tempo médio para receber pagamentos após vendas, crucial na gestão financeira e análise de desempenho.",
        metadata={
            "key": "FINANCIALMETRIC",
            "values": [
                "DSO"
            ],
            "example_answer": [
                {"FINANCIALMETRIC": "DSO"}
            ]
        }
    ),
    Document(
        page_content="Métricas usadas para avaliar o desempenho em relação a metas, essenciais para medir progresso e tomar decisões baseadas em dados, como o Order Cycle Time.",
        metadata={
            "key": "KPI",
            "values": [
                "receita",
                "Order Cycle Time"
            ],
            "example_answer": [
                {"KPI": "Order Cycle Time"}
            ]
        }
    ),
    Document(
        page_content="Métricas quantitativas avaliam eficiência e eficácia de processos, como taxa de retrabalho, para identificar melhorias.",
        metadata={
            "key": "PROCESSQUALITYMETRIC",
            "values": [
                "Order Cycle Time",
                "retrabalho"
            ],
            "example_answer": [
                {"PROCESSQUALITYMETRIC": "retrabalho"}
            ]
        }
    ),
    Document(
        page_content="Categorias que organizam eventos com base na frequência, como 'mais frequentes', 'frequentes', 'raros', para compreensão e organização.",
        metadata={
            "key": "TYPESOFCASEOCCURRENCE",
            "values": [
                "casos"
            ],
            "example_answer": [
                {"TYPESOFCASEOCCURRENCE": "casos"}
            ]
        }
    ),
    Document(
        page_content="Método de entrega de produtos/serviços aos consumidores, como varejo, distribuição, e-commerce; exemplo: vender eletrônicos em lojas de eletrônicos.",
        metadata={
            "key": "MARKETINGCHANNEL",
            "values": [
                "Canal de distribuição"
            ],
            "example_answer": [
                {"MARKETINGCHANNEL": "Canal de distribuição"}
            ]
        }
    ),
    Document(
        page_content="Consequências de uma ação ou evento que podem abranger aspectos financeiros, operacionais e sociais.",
        metadata={
            "key": "IMPACT",
            "values": [
                "impacto financeiro",
                "impacto"
            ],
            "example_answer": [
                {"IMPACT": "impacto financeiro"}
            ]
        }
    ),
    Document(
        page_content="Atividades de marketing, como a taxa de conversão, que avaliam a eficácia em transformar prospects em clientes.",
        metadata={
            "key": "MARKETINGACTIVITY",
            "values": [
                "conversão"
            ],
            "example_answer": [
                {"MARKETINGACTIVITY": "conversão"}
            ]
        }
    ),
    Document(
        page_content="Um conceito amplo que se refere a algo identificável e manipulável, podendo ser tangível ou intangível em diversos contextos.",
        metadata={
            "key": "OBJECT",
            "values": [
                "a receber",
                "faturas",
                "OV",
                "status",
                "envios",
                "itens",
                "impacto",
                "horas",
                "em atraso"
            ],
            "example_answer": [
                {"OBJECT": "em atraso"}
            ]
        }
    ),
    Document(
        page_content="Estado de entrega de mercadorias em relação à data planejada, descrevendo a fase do processo de entrega.",
        metadata={
            "key": "SHIPPINGSTATUS",
            "values": [
                "no dia solicitado de entrega",
                "atrasado ao dia solicitado de entrega",
                "antecipado ao dia solicitado de entrega"
            ],
            "example_answer": [
                {"SHIPPINGSTATUS": "antecipado ao dia solicitado de entrega"}
            ]
        }
    ),
    Document(
        page_content="Estado de recebimento de pagamento em relação à data planejada, descrevendo a fase do processo financeiro.",
        metadata={
            "key": "RECEIPTSTATUS",
            "values": [
                "recebimento atrasado",
                "recebimento no prazo",
                "recebimento antecipado"
            ],
            "example_answer": [
                {"RECEIPTSTATUS": "recebimento antecipado"}
            ]
        }
    ),
    Document(
        page_content="Meio ou rota para disponibilizar produtos/serviços aos clientes, como Hospital e Farmácia, essenciais na distribuição de uma empresa.",
        metadata={
            "key": "CANAL",
            "values": [
                "Ferro",
                "Matéria Prima Geral"
            ],
            "example_answer": [
                {"CANAL": "Matéria Prima Geral"}
            ]
        }
    ),
    Document(
        page_content="Ação ou tarefa realizada para alcançar um objetivo.",
        metadata={
            "key": "ACTIVITY",
            "values": [
                "Alterar Data de Cobrança do Item de Entrega",
                "Alterar Preço do Item OV"
            ],
            "example_answer": [
                {"ACTIVITY": "Alterar Preço do Item OV"}
            ]
        }
    ),
    Document(
        page_content="Pessoa ou entidade que adquire produtos ou serviços em troca de pagamento.",
        metadata={
            "key": "CUSTOMER",
            "values": [
                "Raia Drogasil",
                "Americanas"
            ],
            "example_answer": [
                {"CUSTOMER": "Raia Drogasil"}
            ]
        }
    ),
    Document(
        page_content="Produto não processado, intercambiável e globalmente negociado, com preços influenciados pela oferta e demanda.",
        metadata={
            "key": "COMMODITY",
            "values": [
                "Ferro",
                "Matéria Prima Geral"
            ],
            "example_answer": [
                {"COMMODITY": "Ferro"}
            ]
        }
    ),
    Document(
        page_content="Avaliação do estado atual de algo, como pedidos, por meio da coleta e interpretação de informações relevantes, permitindo tomar decisões informadas.",
        metadata={
            "key": "ANALYSISSTATUS",
            "values": [
                "Cancelados",
                "Devolvidos",
                "Rejeitados"
            ],
            "example_answer": [
                {"ANALYSISSTATUS": "Devolvidos"}
            ]
        }
    ),
    Document(
        page_content="Segmentação de clientes em grupos com características semelhantes, permitindo estratégias personalizadas.",
        metadata={
            "key": "CUSTOMERGROUP",
            "values": [
                "Distr. Industrial",
                "Dist. Varejo",
                "Órgão Público"
            ],
            "example_answer": [
                {"CUSTOMERGROUP": "Órgão Público"}
            ]
        }
    ),
    Document(
        page_content="É uma estrutura dentro de uma empresa que se concentra na gestão e execução das atividades de vendas.",
        metadata={
            "key": "SALESORGANIZATION",
            "values": [
                "Indústria",
                "Indústria do Aço",
                "Exportação"
            ],
            "example_answer": [
                {"SALESORGANIZATION": "Indústria"}
            ]
        }
    ),
    Document(
        page_content="É o contexto da conversa",
        metadata={
            "key": "CONTEXT",
            "values": [
                "Visão Geral",
                "Análise do Ciclo da Ordem de Venda",
                "Análise de Recebimento de pagamentos",
                "Ordem de Venda Perfeita (Perfect SO)",
                "Envios no prazo (\"on-time shipment\")",
                "Operação contas a receber",
                "Análise de automação",
                "Impacto na Receita"
            ],
            "example_answer": [
                {"CONTEXT": "Visão Geral"}
            ]
        }
    )
]