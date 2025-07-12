import logging

class BaseScrapper:
    """
    Base class for scrappers.
    """
    def __init__(self, name):
        self.logger = logging.getLogger(self.__class__.__module__)
        self.name = name

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def error(self, message):
        self.logger.error(f"{self.name}: {message}")

    def info(self, message):
        self.logger.info(f"{self.name}: {message}")
    
    def debug(self, message):
        self.logger.debug(f"{self.name}: {message}")
    
    def warning(self, message):
        self.logger.warning(f"{self.name}: {message}")