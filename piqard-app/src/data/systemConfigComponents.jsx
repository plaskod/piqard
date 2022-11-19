const systemConfigComponents = {
    "information_retriever": ['GoogleCustomSearch', 'RankingRetriever', 'VectorRetriever', 'None'],
    "prompt_template": ['basic_prompt', 'context_prompt', 'custom_prompt'],
    "context_builder": ['TruncatedContext', 'MergedContext'],
    "large_language_model": ['BLOOM 176B API', 'GPT-J6B API'],
}

export default systemConfigComponents;