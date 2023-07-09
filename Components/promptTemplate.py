from kor.nodes import Object, Text, Number

class llmTemplates():

    def __init__(self, log):
        self.log = log

    def cat_int_sent_template(self):

        schema = Object(
            id="sentence_info",
            description="Extract the information for the input query.",
            attributes=[
                Text(
                    id="category",
                    description="Identify the category of the text.",
                    examples=[("I do not want the order", "ORDER")],
                ),
                Text(
                    id="intent",
                    description="Identify the intent of the text.",
                    examples=[("I have problems with the termination of a user account", "DELETE_ACCOUNT")],
                ),
                Text(
                    id="sentiment",
                    description="Identify the sentiment of the text.",
                    examples=[("how can I find my invoice?", "NEUTRAL"),
                              ("I was deeply disappointed with the poor customer service", "NEGATIVE"),
                              ("I had an amazing time at the concert","POSITIVE")],
                ),
            ],
            examples=[
                (
                    "I would appreciate your recommendation for my travel",
                    [
                        {"category": "TRAVEL", "intent": "RECOMMENDATION", "sentiment": "POSITIVE"}
                    ]
                ),
                (
                    "I disappointed with his advice on health and fitness",
                    [
                        {"category": "HEALTH AND FITNESS", "intent": "ADVICE", "sentiment": "NEGATIVE"}
                    ]
                )
            ],
            many=True,
        )

        return schema