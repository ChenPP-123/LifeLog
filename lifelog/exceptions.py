class LifeLogError(Exception):
    pass


class EmptyTextError(LifeLogError):
    pass


class InvalidIndexError(LifeLogError):
    pass


class TaskNotFoundError(LifeLogError):
    pass
