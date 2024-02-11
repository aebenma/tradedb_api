from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
import pandas as pd
import random
from fastapi.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates
import sqlalchemy as sa

app = FastAPI() 

main_server_name = "Bebis"
main_DB = "TRADEDB"
source_engine = sa.create_engine(f"mssql+pyodbc://@{main_server_name}/{main_DB}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server",fast_executemany=True)
connection = source_engine.raw_connection()
cursor = connection.cursor()

'''
Root: Display all of the trade information as the homepage
'''
@app.get("/")
def root():
    table_name = '[TRADEDB].[dbo].[Trades]'
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query,source_engine)
    return HTMLResponse(content=df.to_html(),status_code=200)

'''
Stored Procedure 1:
    Create endpoint to add a new trader with stored procedure
'''
@app.post("/traders/new/{name}")
def new_trader(name):
    table_name = '[TRADEDB].[dbo].[Traders]'

    # Insert the value into df 
    cursor.execute("INSERT INTO [TRADEDB].[dbo].[Traders] VALUES (?)",(name))
    connection.commit() 

    # Reread df with new value
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, source_engine)

    # Output new df
    return df.to_string() 

'''
Stored Procedure 2:
    Create endpoint to add a new trade with stored procedure
'''
@app.post("/trades/new/{cur}/{amt}/{price}/{trader}")
def new_trade(cur,amt,price,trader):
    # Get rest of values 
    cur_clock = datetime.now() # set clock as now, assume trade is being done now

    # get trader_id from trader table
    table_name = '[TRADEDB].[dbo].[Traders]'
    query = f"SELECT * FROM {table_name} where name='{trader}'"
    df = pd.read_sql(query, source_engine)
    trader_id = df.values[0][0]
    
    # random number for identifier
    identifier = ''.join([str(random.randint(0,9)) for _ in range(10)])

    # string query with trade information
    query = "INSERT INTO [TRADEDB].[dbo].[Trades] (currency_pair, amount, price, trade_date, trader_name, identifier, trader_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    trade_info = (cur,amt,price,cur_clock,trader,identifier,trader_id)

    # push new trade
    cursor.execute(query,trade_info)
    connection.commit()

    # reread db with new value
    table_name = '[TRADEDB].[dbo].[Trades]'
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, source_engine)

    return df.to_string()


'''
Stored Procedure 3:
    Create endpoint to query traders with stored procedure
'''
@app.get("/traders/{name}")
def get_trader_info(name):
    table_name = '[TRADEDB].[dbo].[Traders]'
    query = f"SELECT * FROM {table_name} where name='{name}'"
    df = pd.read_sql(query, source_engine)
    return HTMLResponse(content=df.to_html(),status_code=200)

'''
Stored Procedure 4:
    Create endpoint to query trades with stored procedure 
'''
@app.get("/trades/{id}")
def get_trade_info(id):
    table_name = '[TRADEDB].[dbo].[Trades]'
    query = f"SELECT * FROM {table_name} where trade_id={id}"
    df = pd.read_sql(query, source_engine)
    return HTMLResponse(content=df.to_html(),status_code=200)

