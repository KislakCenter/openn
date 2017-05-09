class CountLogger(object):
    def __init__(self, logger, countable):
        self._logger = logger
        self._total  = len(countable)
        self._count  = 0
        self._width  = len(str(self._total))

    def count_string(self, msg=None):
        return u'{count:0{width}d}/{total} {msg}'.format(
            count=self._count, width=self._width, total=self._total, msg=msg)

    def count(self, msg=None,inc=True):
        """Increment and display count with message `msg`; don't increment if
        `inc` is non-True.

        """
        if inc: self._count += 1
        self._logger.info(self.count_string(msg))
