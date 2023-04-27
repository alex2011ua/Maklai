from fastapi import FastAPI
from permutator import Paraphrase


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/paraphrase/")
async def paraphrase(tree: str, limit: int = 20):
    """
    Takes as input a syntactic tree of English text and returns its paraphrased versions.

    :param tree: A syntactic tree of English in the form of a string.
    :type tree: str
    :param limit: The maximum number of paraphrased texts to be returned.
    :rtype limit: int
    :return: a list of paraphrased trees in JSON format.
    """
    p = Paraphrase(tree)
    p.find_rephrase()
    p.make_random_permutations()
    return p.get_phrases(limit=limit)
