"""
Address Diary — сохраняет историю транзакций адреса в локальную SQLite-базу.
"""

import requests
import sys
import sqlite3
import os
from datetime import datetime

DB_NAME = "address_diary.db"

def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tx_log (
            address TEXT,
            txid TEXT,
            timestamp INTEGER,
            block_time TEXT,
            PRIMARY KEY(address, txid)
        )
    """)
    conn.commit()
    return conn

def fetch_transactions(address):
    url = f"https://blockstream.info/api/address/{address}/txs"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def store_transactions(conn, address, txs):
    c = conn.cursor()
    for tx in txs:
        txid = tx["txid"]
        timestamp = tx["status"]["block_time"]
        block_time = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        try:
            c.execute("""
                INSERT INTO tx_log (address, txid, timestamp, block_time)
                VALUES (?, ?, ?, ?)
            """, (address, txid, timestamp, block_time))
        except sqlite3.IntegrityError:
            continue
    conn.commit()

def show_summary(conn, address):
    c = conn.cursor()
    c.execute("SELECT COUNT(*), MIN(block_time), MAX(block_time) FROM tx_log WHERE address = ?", (address,))
    count, first, last = c.fetchone()
    print(f"📘 История по адресу: {address}")
    print(f"🔢 Транзакций в базе: {count}")
    if first and last:
        print(f"⏱️ С первой: {first}")
        print(f"⏱️ До последней: {last}")
    print("✅ Готово.")

def main(address):
    print(f"📥 Загрузка истории по адресу {address}")
    try:
        txs = fetch_transactions(address)
    except Exception as e:
        print("❌ Ошибка при получении данных:", e)
        return

    conn = setup_db()
    store_transactions(conn, address, txs)
    show_summary(conn, address)
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python address_diary.py <bitcoin_address>")
        sys.exit(1)
    main(sys.argv[1])
