import logging

#
# Copyright (c) SIOS Technology, Inc. All rights reserved.
# 
# MIT License
# 

LOG_LEVEL = logging.DEBUG

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)s %(funcName)s %(message)s"

logging.basicConfig(
  level=LOG_LEVEL,
  format=LOG_FORMAT,
  datefmt="[%X]"
)

# logger = logging.getLogger(__name__)

class CommonLogger:
  # logger = None

  def __init__(self, name):
    self.logger = logging.getLogger(name)

  def error(self, obj):
    self.logger.error(obj)

  def info(self, obj):
    self.logger.info(obj)

  def debug(self, obj):
    self.logger.debug(obj)
