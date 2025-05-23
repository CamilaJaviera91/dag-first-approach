import pandas as pd
from .connection import get_connection
from airflow.utils.log.logging_mixin import LoggingMixin

logger = LoggingMixin().log

def extract_data(_=None):
    conn, cur = get_connection()
    if not conn:
        return None

    query = """ with resume as 
                (select 
                    o.order_date as date,
                    concat(s.city,'-',s.store_id) as store,
                    p."name",
                    p.category,
                    p.price,
                    o.quantity,
                    (p.price * o.quantity) as total,
                    sm."name" as salesman,
                    c."name" as client
                from test.orders o 
                join test.store s  on o.store_id  = s.store_id 
                join test.product p on o.product_id = p.product_id
                join test.salesman sm on o.salesman_id = sm.salesman_id
                join test.client c on o.client_id = c.client_id
                order by o.order_date desc)
                select 
                    extract(year from date(date)) as year,
                    store,
                    sum(total) as total
                from resume
                group by year, store
                order by year, total asc
            """
    try:
        cur.execute(query)
        records = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(records, columns=columns)
        return df.to_dict(orient='records')  
    
    except Exception as e:
        logger.error(f"❌ Error executing query: {e}")
        return None
    finally:
        cur.close()
        conn.close()
        logger.info("🔒 PostgreSQL connection closed.")