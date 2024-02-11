# tradedb_api
 
## API Integration

The API has four endpoints. Assuming we are hosted on `127.0.0.1`:

| Method | Call  | Action |
| --- | --- | --- |
| POST | 127.0.0.1/traders/new/name | Add a new entry to the Traders table with given name. The trader_id is generated from the counter.   |
| POST | 127.0.0.1/trades/new/cur/amt/price/trader | Add a new entry to Trades table. You must supply the currency_pair, amount, price, and trader_name. It will create a new trade with the current time. Using the trader_name, it will locate the trader_id from the Traders table. It generates a random 10-digit number for the identifier. Finally, the trade_id is generated from the counter.  |
| GET | 127.0.0.1/traders/name | Yields an HTML page with the trader’s information given the name |
| GET | 127.0.0.1/trades/id | Yields an HTML page with all of the table information for a trade with id |

The root `127.0.0.1/` displays all of the trades made. Run the code with

`python -m uvicorn main:app --reload`

**Discussion:** 

The current implementation is a starter version of the database API. This should not be used in practice because:

- It assumes valid input, so there is no checking that the inputs for the endpoints are correct.
- The implementation uses SQL injections in the code, which leaves the server vulnerable to hackers.