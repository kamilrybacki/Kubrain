import enum
import logging

GLOBAL_LOGGING_LEVEL = logging.INFO
GLOBAL_LOGGING_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
GLOBAL_LOGGING_MESSAGE_FORMAT = '[%(name)s] %(asctime)s - %(levelname)s - %(message)s'


class KubrainLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name[0], level)
        handler = logging.StreamHandler()
        handler.setLevel(GLOBAL_LOGGING_LEVEL)
        formatter = logging.Formatter(
            fmt=GLOBAL_LOGGING_MESSAGE_FORMAT,
            datefmt=GLOBAL_LOGGING_TIME_FORMAT
        )
        handler.setFormatter(formatter)

        self._apply_to_root(handler)

        self.setLevel(GLOBAL_LOGGING_LEVEL)
        self.addHandler(handler)
        self.propagate = False

    # pylint: disable=protected-access, no-member
    def _apply_to_root(self, handler: logging.Handler):
        try:
            getattr(logging.root, '_patched')
            return
        except AttributeError:
            setattr(logging.root, '_patched', True)
            logging.root.handlers.clear()
            logging.root.addHandler(handler)
            logging.root.setLevel(GLOBAL_LOGGING_LEVEL)


class KubrainLoggers(enum.Enum):
    VALIDATION = KubrainLogger('VALIDATION')
    PARSING = KubrainLogger('PARSING')
    MANAGER = KubrainLogger('MANAGER')

    def __call__(self, message: str, level: int = logging.INFO):
        self.value.log(
            level=level,
            msg=message
        )
