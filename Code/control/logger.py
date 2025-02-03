from loguru import logger # https://github.com/Delgan/loguru/blob/master/loguru/_logger.py

# .. |logger.trace| replace:: :meth:`logger.trace()<Logger.trace()>`
# .. |logger.debug| replace:: :meth:`logger.debug()<Logger.debug()>`
# .. |logger.info| replace:: :meth:`logger.info()<Logger.info()>`
# .. |logger.success| replace:: :meth:`logger.success()<Logger.success()>`
# .. |logger.warning| replace:: :meth:`logger.warning()<Logger.warning()>`
# .. |logger.error| replace:: :meth:`logger.error()<Logger.error()>`
# .. |logger.critical| replace:: :meth:`logger.critical()<Logger.critical()>`


class LoggerFactory:
    @staticmethod
    def get_logger(name, levels=None):
        logger.remove()

        if levels is None:
            levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


        logger.add(
            sink=lambda msg: print(msg, end=""),
            level="DEBUG",
            filter=lambda record: record["level"].name in levels,
            colorize=True,
            format="{name}: <level>{level}</level>: {message}"
        )

        return logger.bind(name=name)


