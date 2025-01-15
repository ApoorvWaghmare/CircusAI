import logging
from mongoengine import connect, disconnect

#----------#
from .config import Config
#----------#

logger = logging.getLogger(__name__)

#======================================================================================================================#
# StartUpService
#======================================================================================================================#

class StartUpService:

    @staticmethod
    def global_init():
        """
        Initializes the MongoDB client using mongoengine.
        """
        try:
            # Disconnecting any existing connections
            disconnect()
            # Connect to MongoDB using mongoengine
            connect(
                alias = 'default',  # Telling mongoengine which connection to use by default
                db = Config.MONGODB_SETTINGS['db'],
                host = Config.MONGODB_SETTINGS['host']
            )
            logger.info("MongoDB connected successfully using mongoengine")
            print("MongoDB connected successfully using mongoengine")
        except Exception as e:
            logger.exception("An error occurred while initializing MongoDB connection")
            print(e)
            raise e

#======================================================================================================================#
# End of StartUpService
#======================================================================================================================#
