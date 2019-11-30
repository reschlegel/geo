from flask import Flask, json, jsonify, request, g
import psycopg2, requests, time

app = Flask(__name__)


def get_conn():
    print("getting conn")
    if not hasattr(g, 'postgres_db'):
        RETRIES=12

        while RETRIES >= 0:
            try:
                conn = psycopg2.connect("dbname='gis' user='geo' host='172.17.0.1' password='geo'")
                RETRIES=-1
                g.postgres_db = conn
            except Exception as e:
                print(f"Unable to connect to database. Retries remaining: {RETRIES}")
                print(e)
                RETRIES -= 1
                time.sleep(10)
        return g.postgres_db
    return g.postgres_db

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        jsdata = request.get_json(force=True)
        try:
            address = jsdata['address']
            key = jsdata['key']
        except:
            return jsonify(error="address and key are required for POST request")
    if request.method == 'GET':
        try:
            address = request.values.get('address')
            key = request.values.get('key') 
        except:
            return jsonify(error="address and key are required for GET request")

    payload = {'address': address, 'key': key}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
    j = r.json()
    
    try:
        lat = j['results'][0]['geometry']['location']['lat']
        lng = j['results'][0]['geometry']['location']['lng']
    except:
        return jsonify(error="Invalid address or key")

    try:
        cur = get_conn().cursor()
        cur.execute(f"select name from (select name, ST_Contains(geom, ST_Transform(ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326), 4269)) as contains from state) a where contains = 't'")
        rows = cur.fetchall()
        return jsonify(state=rows[0][0])
    except Exception as e:
        print(e)
        return jsonify(error="address error, please check that the address is actually in the U.S.")
