from contextlib import asynccontextmanager
from sql_alchemy.connection import get_session


class ConnectionManager:
    def __init__(self):
        self.current_session = None
        self.transaction_started = False

    async def start_transaction(self, connection=get_session()):
        self.current_session = connection
        self.transaction = await self.current_session.__aenter__()
        self.transaction_started = True

    async def end_transaction(self, commit=True):
        if self.current_session and self.transaction_started:
            try:
                if commit:
                    await self.transaction.commit()
                else:
                    await self.transaction.rollback()
            finally:
                await self.current_session.__aexit__(None, None, None)
                self.transaction_started = False
                self.current_session = None

    @asynccontextmanager
    async def get_session(self):
        if self.transaction_started:
            async with self.current_session as session:
                yield session
        else:
            async with get_session() as session:
                yield session