import sqlite3

conn = sqlite3.connect('rss-aggregator.db')
c = conn.cursor

c.execute('CREATE TABLE history (id)')

conn.commit()
conn.close()
