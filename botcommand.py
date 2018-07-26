class BotCommand(object):
  def __init__(self, command, response, count = 0):
    self.command = command
    self.response = response
    self.count = count 