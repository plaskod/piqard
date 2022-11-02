from typing import Optional
from prompting.prompt import Prompt

prompt = """Answer the question given the passage.

Passage: A recent study showed Chick-fil-A had the slowest drive-thru among major fast-food chains – but only because it’s so popular and there are so many cars in line."
Question : Which fast food chain has the slowest drive-thru, according to a new study?
Answer : Chick-fil-A

Passage: The Eiffel Tower in Paris is reportedly in serious need of repairs. However, the iconic landmark is instead being given a paint job costing 60 million euros in preparation for the 2024 Olympics, Reuters reports, according to a confidential analysis cited by French magazine Marianne.
Question : Which iconic landmark is reportedly riddled with rust and badly in need of repairs?
Answer : The Eiffel Tower

Passage: Charlie Nunn said the lender saw customers with persistent debt problems increase by a third in the first six months of this year. But he added many customers are in a healthier financial position than they were before the pandemic.
Question : What percentage of Lloyds customers have savings of less than £500, according to the bank’s chief executive?
Answer : 80%

Passage: The hot dog champ won the competition after eating an astounding 63 hot dogs and buns in 10 minutes on Monday. Chestnut has won the long-running Independence Day contest seven consecutive times and in 15 of the last 16 years.
Question : How many hot dogs did competitive eater Joey Chestnut devour to win the Nathan’s Famous International Hot Dog Eating Contest this week?
Answer :  63

Passage: Twitter locked Kanye West for violating the company’s policies over an antisemitic tweet.
Question : Which high-profile individual’s Twitter account was locked this week for posting an offensive message?
Answer : Kanye West

Passage: {passage}
Question : {question}
Answer : """


class FewShowPrompt(Prompt):
    def __init__(self):
        super().__init__(prompt)

    def generate(self, question: str, documents: Optional[list]) -> str:
        first_100_words = " ".join(documents[0]['text'].split()[:100])
        return self.prompt.format(question=question, passage=first_100_words)

    def __str__(self):
        return "4-shot question - passage - answer"
