class Opt:
    """
    Opt class defines each individual option, its dependencies, its conflicts,
    and what other options require it
    """
    def __init__(self, a):
        """
        initializing Opt
        :param a: the option we are defining
        """
        self.opt = a
        self.dependencies = []
        self.conflicts = []
        self.requiredBy = []

    def newDep(self, b):
        """
        newDep adds an Opt identifier to to the list of dependencies
        :param b: a new dependency of this particular Opt
        :return: void
        """
        self.dependencies.append(b)

    def newConflict(self, c):
        """
        newConflict adds an Opt identifier to the list of conflicts
        :param c: a new conflict of this particular Opt
        :return: void
        """
        self.conflicts.append(c)

    def newReq(self, d):
        """
        newReq adds an Opt identifier to the list of Opt identifiers that
        require this particular Opt
        :param d: an identifier for the Opt that requires this one
        :return: void
        """
        self.requiredBy.append(d)


class RuleSet:
    """
    The Rule set class holds the methods for defining Options (Opt), their
    dependencies, their conflicts, and a method to check to see if the rules
    between options is coherent or non coherent
    """
    def __init__(self):
        """
        Initializing the ruleset
        self.options is initially defined here as an empty dictionary, the key
        of each item in the dictionary is the Opt identifier
        """
        self.options = dict()

    def addDep(self, dependent, dependency):
        """
        addDep creates the dependency relationship
        :param dependent: the Opt that is dependent on another
        :param dependency: the Opt that is required by another
        :return: void
        """
        if dependent not in self.options:
            dep = Opt(dependent)
            dep.newDep(dependency)
            self.options[dependent] = dep
        else:
            self.options[dependent].newDep(dependency)

        if dependency not in self.options:
            depcy = Opt(dependency)
            depcy.newReq(dependent)
            self.options[dependency] = depcy
        else:
            self.options[dependency].newReq(dependent)

        if self.options[dependent].requiredBy:
            for j in self.options[dependent].requiredBy:
                self.options[j].newDep(dependency)

    def addConflict(self, ifSelected, cannotBeSelected):
        """
        addConflict creates the conflicting relationship
        :param ifSelected: first conflicting option
        :param cannotBeSelected: second conflicting option
        :return: void
        """
        if ifSelected not in self.options:
            selected = Opt(ifSelected)
            selected.newConflict(cannotBeSelected)
            self.options[ifSelected] = selected
        else:
            self.options[ifSelected].newConflict(cannotBeSelected)

        if cannotBeSelected not in self.options:
            conflict = Opt(cannotBeSelected)
            conflict.newConflict(ifSelected)
            self.options[cannotBeSelected] = conflict
        else:
            self.options[cannotBeSelected].newConflict(ifSelected)

        if self.options[ifSelected].requiredBy:
            for i in self.options[ifSelected].requiredBy:
                self.options[i].newConflict(cannotBeSelected)

        if self.options[cannotBeSelected].requiredBy:
            for z in self.options[cannotBeSelected].requiredBy:
                self.options[z].newConflict(ifSelected)

    def isCoherent(self):
        """
        isCoherent is the method that checks to see if there are any conflicting
        rules as far as dependencies and conflicts
        :return: Boolean
        """
        for k, v in self.options.items():
            for dep in v.dependencies:
                v.dependencies = v.dependencies + self.options[dep].dependencies
                v.conflicts = v.conflicts + self.options[dep].conflicts
            if set(v.dependencies) & set(v.conflicts) or \
                            set(v.requiredBy) & set(v.conflicts):
                return False
            for e in v.requiredBy:
                if set(self.options[e].conflicts) & set(v.requiredBy):
                    return False
        return True


class Options:
    """
    Options Class contains the method for creating a list of selected options
    in accordance to the ruleset defined
    """
    def __init__(self, rs):
        """
        initializing the options class,
        self.collection contains the collection of currently selected options
        :param rs: the Ruleset class used to define relationship between options
        """
        self.ruleset = rs
        self.collection = []

    def toggle(self, option):
        """
        toggle is a method for selecting or deselection an option and any
        option that may need to be selected or deselected in the process
        :param option: the option selected or deselected
        :return: void
        """
        self.collection = list(set(self.collection))
        optionDep = list(set(self.ruleset.options[option].dependencies))
        optionCon = list(set(self.ruleset.options[option].conflicts))
        optionReq = list(set(self.ruleset.options[option].requiredBy))
        if option in self.collection:
            self.collection.remove(option)
            try:
                for r in optionReq:
                    self.collection.remove(r)
                    for dr in self.ruleset.options[r].requiredBy:
                        self.collection.remove(dr)
            except ValueError:
                pass
        else:
            self.collection.append(option)
            for z in optionDep:
                self.collection.append(z)
            for j in optionCon:
                try:
                    self.collection.remove(j)
                except ValueError:
                    pass
                try:
                    for req in self.ruleset.options[j].requiredBy:
                        self.collection.remove(req)
                        try:
                           for d in self.ruleset.options[req].requiredBy:
                               self.collection.remove(d)
                        except ValueError:
                            pass
                except ValueError:
                    pass
                try:
                    for i in optionDep:
                        if j in self.ruleset.options[i].conflicts:
                            self.collection.remove(j)
                except ValueError:
                    pass

            for a in optionDep:
                try:
                    for z in self.ruleset.options[a].conflicts:
                        if z in self.collection:
                            self.collection.remove(z)
                except ValueError:
                    pass

    def selection(self):
        """
        selection returns the current options selected
        :return: set(self.collection)
        """
        return set(self.collection)
