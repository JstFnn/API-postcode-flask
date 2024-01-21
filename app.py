from flask import Flask, jsonify, request
from db import pymysql
import os


app = Flask(__name__)


# TRIGER DATABASE 
def db_postCode():
    conn = None
    try:
        conn = pymysql.connect(
            host='8q3.h.filess.io',
            database='01_watchfelt',
            user='01_watchfelt',
            port=3307,
            password='ab6d54fdeb02aa940012874a8001925645e3e51f',
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Connection successful:", conn)  # Debug line
    except pymysql.Error as e:
        print(f"SQL Error: {e}")
    return conn


port = int(os.environ.get('PORT', 5000))

# MAIN
@app.route("/")
def welcome():
    return 'Halo dunia! KUKUH NURCAHYO@IF 10 O '


# GET, POST, UPDATE, DELETE KODE POS
@app.route("/kodePos", methods=['GET', 'POST', 'PUT', 'DELETE'])
def kode():
    conn = db_postCode()

    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                cursor.execute("SELECT * FROM kodePos")
                kodePos = cursor.fetchall()
                if kodePos:
                    return jsonify(kodePos)
                else:
                    return jsonify({'message': 'Data tidak ditemukan'}), 404

            elif request.method == 'POST':
                # Check for missing parameters
                required_params = ['Provinsi', 'Kabupaten', 'Kecamatan', 'Desa', 'Kode pos']
                missing_params = [param for param in required_params if request.form.get(param) is None]

                if missing_params:
                    return jsonify({'error': f'Missing parameter: {", ".join(missing_params)}'}), 400

                add_Provinsi = request.form.get('Provinsi')
                add_Kabupaten = request.form.get('Kabupaten')
                add_Kecamatan = request.form.get('Kecamatan')
                add_Desa = request.form.get('Desa')
                add_Kode_pos = request.form.get('Kode pos')

                query_insert = """INSERT INTO kodePos (Provinsi, Kabupaten, Kecamatan, Desa, Kode_pos) VALUES (%s, %s, %s, %s, %s)"""

                cursor.execute(query_insert, (add_Provinsi, add_Kabupaten, add_Kecamatan, add_Desa, add_Kode_pos))
                conn.commit()

                return jsonify({'message': 'Sukses! Data berhasil ditambahkan.'}), 201

            elif request.method == 'PUT':
                # Check for missing parameters
                required_params = ['id', 'Provinsi', 'Kabupaten', 'Kecamatan', 'Desa', 'Kode pos']
                missing_params = [param for param in required_params if request.json.get(param) is None]

                if missing_params:
                    return jsonify({'error': f'Missing parameters: {", ".join(missing_params)}'}), 400

                update_id = request.json.get('id')
                update_Provinsi = request.json.get('Provinsi')
                update_Kabupaten = request.json.get('Kabupaten')
                update_Kecamatan = request.json.get('Kecamatan')
                update_Desa = request.json.get('Desa')
                update_Kode_pos = request.json.get('Kode pos')

                query_update = """UPDATE kodePos SET Provinsi=%s, Kabupaten=%s, Kecamatan=%s, Desa=%s, Kode_pos=%s WHERE id=%s"""

                cursor.execute(query_update, (update_Provinsi, update_Kabupaten, update_Kecamatan, update_Desa, update_Kode_pos, update_id))
                conn.commit()

                return jsonify({'message': 'Update sukses! Data berhasil diperbarui.'}), 200

            elif request.method == 'DELETE':

                delete_id = request.form.get('id')

                if delete_id is None:
                    return jsonify({'message': 'Missing parameters'}), 400              

                query_delete = """DELETE FROM kodePos WHERE id=%s"""

                cursor.execute(query_delete, (delete_id,))
                conn.commit()

                return jsonify({'message': 'Delete sukses! Data berhasil dihapus.'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        # Always close the connection in the finally block
        if conn:
            conn.close()



#  GET DATAS POS BY ID
@app.route("/kodePos/id", methods=['GET', 'PUT', 'DELETE'])
def kode_by_id():
    conn = db_postCode()

    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                id_param = request.args.get('id')

                if id_param is None:
                    return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

                id_value = int(id_param)

                cursor.execute("SELECT * FROM kodePos WHERE id=%s", (id_value,))
                kodePos = cursor.fetchone()

                if kodePos:
                    return jsonify(kodePos)
                else:
                    return jsonify({'message': 'Data tidak ditemukan'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500           
            

# GET DATAS BY NAMA DESA   
@app.route("/kodePos/namaDesa", methods=['GET'])
def kode_by_nama_desa():
    conn = db_postCode()

    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                nama_desa = request.args.get('Desa')

                if not nama_desa:
                    return jsonify({'error': 'Parameter nama_desa tidak ditemukan'}), 400

                # Menggunakan LIKE untuk pencarian yang lebih fleksibel
                cursor.execute("SELECT * FROM kodePos WHERE `Desa` LIKE %s", ('%' + nama_desa + '%',))
                kodePos = cursor.fetchall()

                if kodePos:
                    return jsonify(kodePos)
                else:
                    return jsonify({'message': 'Data tidak ditemukan'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# GET DATAS BY KODE POS
@app.route("/kodePos/kode", methods=['GET'])
def kode_by_kode_pos():
    conn = db_postCode()

    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                kode_pos = request.args.get('Kode_pos')

                if not kode_pos:
                    return jsonify({'error': 'Parameter Kode_pos tidak ditemukan'}), 400

                cursor.execute("SELECT * FROM kodePos WHERE `Kode_pos`=%s", (kode_pos,))
                kodePos = cursor.fetchall()

                if kodePos:
                    return jsonify(kodePos)
                else:
                    return jsonify({'message': 'Data tidak ditemukan'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# CLOSE CURSOR

    finally:
        # Always close the connection in the finally block
        if conn:
            conn.close()

# MAIN
if __name__ == '__main__':
    # Menjalankan aplikasi Flask pada host 0.0.0.0 dan port yang sudah ditentukan
    app.run(debug=True, host='0.0.0.0', port=port)
