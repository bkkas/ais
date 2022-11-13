import pytest
import logging
from src.ais_analyzer.logger.log_class import AisLogger
from src.ais_analyzer.logger.log_init import log_init


def pytest_configure(config):
    logging.setLoggerClass(AisLogger)
    print("Set logger successfully")
    