class WorkflowType(type):
    """
    WDK Workflow type class
    """

    pass


class Workflow(metaclass=WorkflowType):
    """
    Base class for user defined WKD Workflows
    """

    DIGRAPH = None

    @classmethod
    def _get_steps_classes(cls):
        """
        Function returning Step classes

        :return:
        """

        step_cls = []

        if cls.DIGRAPH is None:
            return step_cls

        # append defined node classes
        step_cls += cls.DIGRAPH.keys()
        # append edge classes
        step_cls += [cls for sublist in cls.DIGRAPH.values() for cls in sublist]

        # remove duplicates and return
        return list(dict.fromkeys(step_cls))
