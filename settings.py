DEBUG = False

TOKEN = "nY0wsXlRUdT2FmvlMpWBMJLN"

SQLALCHEMY_DATABASE_URI = "postgresql:///udacians.db"

WEBHOOK_URL = "https://hooks.slack.com/services/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"

HELP_TEXT = """ Help for /workingfrom command.

        Use /workingfrom to let your coworkers know where you are. 

        It's pretty simple! Enter /workingfrom [location] to set where you're working from, where [location] can be any text, up to 500 characters. For instance, you can just say /workingfrom SF, or /workingfrom MTV. You can also write something longer: /workingfrom Out of office until January 14th.

        You can check someone's location with /workingfrom @[user].

        To set your default location, use the '-default' option: /workingfrom SF -default. This will let people know where you are if you haven't used /workingfrom recently.

        """