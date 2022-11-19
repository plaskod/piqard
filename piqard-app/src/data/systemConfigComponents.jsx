const systemConfigComponents = {
    "information_retriever": [
        {name: 'GoogleCustomSearch', value: '!GoogleCustomSearch'},
        {name: 'RankingRetriever', value: '!RankingRetriever'},
        {name: 'VectorRetriever', value: '!VectorRetriever'}
    ],
    "prompt_template": [
        {name: 'basic_prompt', value: 'basic_prompt', template: ''},
        {name: 'context_prompt', value: 'context_prompt', template: ''},
        {name: 'custom_prompt', value: 'custom_prompt', template: ''}
    ],
    "context_builder": [
        {name: 'TruncatedContext', value: '!TruncatedContext'},
        {name: 'MergedContext', value: '!MergedContext'},
    ],
    "large_language_model": [
        {name: 'BLOOM 176B API', value: '!BLOOM176bAPI'},
        {name: 'GPT-J6B API', value: '!GPTj6bAPI'},
    ]
}

export default systemConfigComponents;