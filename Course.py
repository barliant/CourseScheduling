class Course:
    # let self to be course v

    def __init__(self, name: str, units: int,
                 quarter_codes: set, prereq: list, is_upper_only=False):
        self.name = name
        self.units = units  # Total units v requires.
        self.quarterCodes = quarter_codes  # In what quarters the department offers this course
        self.isUpperOnly = is_upper_only  # true if it is an upper only course
        self.prereq = prereq  # in conjunctive normal form, AND of ORs
        self.prereqBool = [None] * len(prereq)  # bool info for satisfied prereqs
        self.successors = set()  # a set of successors of course v
        self.label = None  # label of a course
        self.dependentIndex = 0  # The largest layer index of v's dependent schedule.
        self.requirements = set()  # A set of requirements that v can satisfy.

    @property
    def courseValue(self):
        return -len(self.requirements)

    def __str__(self):
        return " label={label}\n units={units}\n quarterCodes={qc}\n " \
               "isUpperOnly={iuo}\n prereq={prereq}\n prereqBool={pb}\n" \
               " successors={successors}\n dependentIndex={di}\n " \
               "requirements={req}\n".format(label=self.label, units=self.units,
                                             qc=self.quarterCodes, iuo=self.isUpperOnly,
                                             prereq=self.prereq, pb=self.prereqBool,
                                             successors=self.successors,
                                             di=self.dependentIndex,
                                             req=self.requirements)

    def prereq_list(self):
        return [c for OR in self.prereq for c in OR]

    def unsatisfied_prereq(self):
        """
        :return: a set of (still require) courses in v's prereq
        """
        result = set()
        for index, OR in enumerate(self.prereq):
            if not self.prereqBool[index]:
                result.union(OR)
        return result

    def has_dependent(self, L_i):
        """
        check if layer with index L_i is a layer lower than v's dependent index
        if true, L_i is not a valid layer for course v.

        :param L_i: layer index
        :return: true if the layer is lower than v's dependent index
        """
        return L_i < self.dependentIndex
    #
    # def add_prereq(self, OR):
    #     """
    #     OR is in the following format:
    #         {"I&C SCI 45C", "I&C SCI 45J"}
    #
    #     :param OR: add an OR set to the AND (self.prereq)
    #
    #     :return:
    #     """
    #     self.prereq.append(OR)
    #     self.prereqBool.append(None)

    def tag_prereq(self, Bi, cid):
        """
        tag that course with id 'cid' satisfy v's prereq OR set with index Bi

        :param Bi: B^i, the index of the OR set in v.prereq
        :param cid: the id of a course (the key for course in graph)
        """
        if Bi >= len(self.prereq) or cid not in self.prereq[Bi]:
            raise Exception(
                "Course {cid} not exists in OR set with index {Bi}".format(cid=cid, Bi=Bi))
        self.prereqBool[Bi] = cid

