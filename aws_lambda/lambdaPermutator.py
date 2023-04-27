from permutator import Paraphrase
import json


def paraphrase(event, context):
    """
    Takes as input a syntactic tree of English text and returns its paraphrased versions.

    """
    tree = """
        (S
        (NP
        (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter))
        (, ,)
        (CC or)
        (NP (NNP Barri) (NNP Gòtic)))
        (, ,)
        (VP
        (VBZ has)
        (NP
        (NP (JJ narrow) (JJ medieval) (NNS streets))
        (VP
        (VBN filled)
        (PP
        (IN with)
        (NP
        (NP (JJ trendy) (NNS bars))
        (, ,)
        (NP (NNS clubs))
        (CC and)
        (NP (JJ Catalan) (NNS restaurants))))))))
        """
    limit = 2

    if "queryStringParameters" in event and event["queryStringParameters"] is not None:
        if "tree" in event["queryStringParameters"]:
            tree = event["queryStringParameters"]["tree"]
        if "limit" in event["queryStringParameters"]:
            limit = int(event["queryStringParameters"]["limit"])

    p = Paraphrase(tree)
    p.find_rephrase()
    p.make_random_permutations()
    body = {"paraphrases": p.get_phrases(limit=limit)}

    return {'statusCode': 200,
            'body': json.dumps(body)
            }
