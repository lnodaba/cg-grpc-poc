from contextlib import asynccontextmanager
from sql_alchemy.connection import get_session
from custom_logger import logger


class ConnectionManager:
    def __init__(self):
        self.current_session = None
        self.transaction_started = False

    async def start_transaction(self, session):
        self.current_session = session
        self.transaction_started = True
        logger.debug("Transaction started")

    async def end_transaction(self, commit=True):
        if self.current_session and self.transaction_started:
            try:
                if commit:
                    await self.current_session.commit()
                else:
                    await self.current_session.rollback()
            finally:
                self.transaction_started = False
                self.current_session = None
                logger.debug("Transaction ended")

    @asynccontextmanager
    async def get_session(self):
        if self.transaction_started:
            logger.debug("Using transaction session")
            yield self.transaction
        else:
            async with get_session() as session:
                yield session