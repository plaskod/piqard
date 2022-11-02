class FewShowPrompt:
    def __init__(self):
        self.prompt = """Answer the following question given the passage and possible answers
                        An anonymous bidder recently paid a record-breaking sum for a private lunch with legendary investor Warren Buffett. How much did the bidder pay? 
                        Passage: The anonymous bidder paid $19 million for a steak lunch with Warren Buffett at Smith &amp; Wollensky Steakhouse in New York City. The sale was part of an annual auction to benefit an organization combating poverty, hunger, and homelessness. 
                        Answer: $19 million 
                        
                        Which city has been named the most 'liveable' city in the world, according to a report compiled by The Economist? 
                        Passage: The Austrian capital grabbed the top spot from Auckland, which sank to 34th place due to New Zealand’s pandemic restrictions. The report praised Vienna for its stability and good infrastructure as well as good healthcare and culture. 
                        Answer: Vienna 
                        
                        Which wildly popular show was recently green lit for a new season? 
                        Passage: Netflix announced the hit South Korean show is officially coming back for a second season. 
                        Answer: Squid Game
                        
                        What percentage of children in lone parent families now live in poverty, according to analysis by The Guardian? 
                        Passage: Relative poverty, defined as having an income of less than 60% of the national median, rose for single parents by nine percentage points between 2013-14 and 2019-20 to reach 49%. 
                        Answer: 49% 
                        
                        {}
                        Passage: {}
                        Answer: """

    def generate(self, question: str, context: str) -> str:
        first_512_words = " ".join(context.split()[:100])
        return self.prompt.format(question, first_512_words)