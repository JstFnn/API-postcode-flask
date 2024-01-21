import pymysql

# DATABASE
conn = pymysql.connect(
    host='8q3.h.filess.io',
    database='01_watchfelt',
    user='01_watchfelt',
    port=3307,
    password='ab6d54fdeb02aa940012874a8001925645e3e51f',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql_query = """CREATE TABLE IF NOT EXISTS kodePos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Provinsi VARCHAR(30) NOT NULL,
    Kabupaten VARCHAR(30) NOT NULL,
    Kecamatan VARCHAR(30) NOT NULL,
    Desa VARCHAR(30) NOT NULL,
    Kode_pos VARCHAR(10) NOT NULL
) 
"""

cursor.execute(sql_query)

conn.close()
