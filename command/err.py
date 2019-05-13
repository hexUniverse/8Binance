def error(self, bot, update, error):
    self.logger.warning('Update "%s" caused error "%s"', update, error)
