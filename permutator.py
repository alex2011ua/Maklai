from itertools import permutations
from nltk import ParentedTree


class Paraphrase:
    def __init__(self, sentence):
        self.sentence = sentence
        self.ptree = ParentedTree.fromstring(sentence)
        self.paraphrases = []
        self._np = []

    def __str__(self):
        str(self.ptree.leaves())

    def find_rephrase(self) -> None:
        """
        Find in the text all NP (noun phrase) - noun phrases consisting of
        several NPs separated by tags (comma) or SS (conjunctive inflection, e.g. "and").

        :return: None
        """

        for subtree in self.ptree.subtrees():
            if subtree.label() == "NP":
                check_rules = self._count_np(subtree)  # check that children consist of "NP", "CC" and ",".   "NP" >= 2
                if check_rules:
                    index_of_np, list_of_np = check_rules
                    self._np.append((index_of_np, list_of_np))  # add found np

    @staticmethod
    def _count_np(trees: ParentedTree) -> None | tuple:
        """
        Check that children consist of "NP", "CC" and ",".   "NP" >= 2.

        :param trees: NP tree.
        :type trees: ParentedTree
        :return: False - if children don't satisfy requirements,
        tuple with two params: list of positions "NP" and list of "NP" on this positions
        """

        index_np: list = []
        list_np: list = []
        for tree in trees:
            if tree.label() == "NP":
                index_np.append(tree.treeposition())
                list_np.append(tree)
            elif tree.label() == "," or tree.label() == "CC":
                pass
            else:
                return
        return (index_np, list_np) if len(index_np) > 1 else False

    def make_random_permutations(self) -> None:
        """
        Generate options for permuting the found NPs with each other.

        :return:
        """

        for index_np, list_np in self._np:
            for permutation in list(permutations(list_np))[1:]:  # run for every permutation without original position
                new_ptree: ParentedTree = self.ptree.copy(deep=True)
                for position in range(len(index_np)):
                    part_of_tree = permutation[position]
                    new_ptree[index_np[position]] = ParentedTree.fromstring(str(part_of_tree))  # replace old NP to new
                self.paraphrases.append(new_ptree)

    def get_phrases(self, limit=20) -> list:
        """
        Returns paraphrased versions of the syntax tree.

        :param limit: The maximum number of paraphrased texts.
        :type limit: int
        :return: A list of paraphrased trees.
        :rtype: list
        """
        return [
            {"tree": paraphrase.pformat(margin=10000000)}
            for paraphrase in self.paraphrases[:limit]
        ]


TEST_STRING = """
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


if __name__ == "__main__":
    p = Paraphrase(TEST_STRING)
    p.find_rephrase()
    p.make_random_permutations()
    list_trees = p.get_phrases()
    print(list_trees)
