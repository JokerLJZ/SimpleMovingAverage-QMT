from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import pandas as pd


class MySQLConnection:
    """
    Docstring for MySQLConnection
    
    :var symbol: Description
    :vartype symbol: Any
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.engine = None

    def connect(self):
        """
        Docstring for connect
        
        :param self: Description
        """
        try:
            connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}"
            self.engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True
            )
            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Connected to MySQL successfully")
        except Exception as e:
            print(f"Error: {e}")
    
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
    
    def fetch_price_data(self, symbol, days=100):
        query = text("""
            SELECT date, close FROM prices 
            WHERE symbol = :symbol AND date >= DATE_SUB(NOW(), INTERVAL :days DAY)
            ORDER BY date ASC
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"symbol": symbol, "days": days})
            data = result.fetchall()
        return pd.DataFrame(data, columns=['date', 'close'])
