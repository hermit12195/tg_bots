import logging
import aiosqlite



async def db_conn():
    """
    Connect to SQLite database.
    """
    try:
        async with aiosqlite.connect("tg_bot.db") as conn:
            await conn.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY,"
                     "name TEXT NOT NULL,"
                     "phone TEXT NOT NULL,"
                     "subscribed TEXT DEFAULT 'no')")
            await conn.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "client_id INTEGER NOT NULL,"
                    "social_network TEXT NOT NULL,"
                    "niche TEXT NOT NULL,"
                    "expectation TEXT,"
                    "service_type TEXT,"
                    "FOREIGN KEY (client_id) REFERENCES clients(id))")
            await conn.commit()
    except Exception as error:
        logging.error(f"Error during connection to DB - {error}")


async def client_check(tg_id):
    """
    Retrieve user information by Telegram ID.
    """
    try:
        conn = await aiosqlite.connect("tg_bot.db")
        async with conn.execute("SELECT id, name, phone, subscribed FROM clients WHERE id=?", (tg_id,)) as cursor:
            client_details = await cursor.fetchall()
        await conn.close()
        return client_details[0]
    except Exception as error:
        logging.error(f"Error during getting client data from DB - {error}")


async def create_client(tg_id, name, phone):
    """
    Create new client record
    """
    try:
        conn = await aiosqlite.connect("tg_bot.db")
        await conn.execute(
            "INSERT INTO clients (id, name, phone) VALUES (?,?,?)", (tg_id, name, phone))
        await conn.commit()
        await conn.close()
    except Exception as error:
        logging.error(f"Error during client creation in DB - {error}")


async def create_order(tg_id, social_network, niche, expectation, service_type):
    """
    Create new order record
    """
    try:
        conn = await aiosqlite.connect("tg_bot.db")
        await conn.execute(
            "INSERT INTO orders (client_id, social_network, niche, expectation, service_type) VALUES (?,?,?,?,?)",
            (tg_id, social_network, niche, expectation, service_type))
        await conn.commit()
        await conn.close()
    except Exception as error:
        logging.error(f"Error during order creation in DB - {error}")


async def subscribe_client(tg_id):
    """
    Add flag 'subscribed' to the client record
    """
    try:
        conn = await aiosqlite.connect("tg_bot.db")
        await conn.execute(
            "UPDATE clients SET subscribed = 'yes' WHERE id = ?",
            (tg_id,))
        await conn.commit()
        await conn.close()
    except Exception as error:
        logging.error(f"Error during subscription submission in DB - {error}")

async def client_list():
    """
    List all clients` IDs
    """
    try:
        conn = await aiosqlite.connect("tg_bot.db")
        async with conn.execute("SELECT id FROM clients") as cursor:
            client_list = await cursor.fetchall()
        await conn.close()
        return client_list
    except Exception as error:
        logging.error(f"Error with getting client list in DB - {error}")
