import requests
import json
import hashlib
import schedule 
import time


url = " " #url del server donde esta el .json remoto

# Funcion para normalizar el json
def normalizarJSON(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

#Funcion para hacer que el json sea legible dsp
def reescribir(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, separators=(',', ':'))

def fetchJson():
        # Normalizamos los json
        
    dataLocal = normalizarJSON(" /data.json")   # Atento a buscar el .json local
    # Fetcheamos los datos del JSON remoto
    response = requests.get(url)
    # si encontraron el archivin da codigo 200 (encontrado)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        data = response.json()
        dataServer = json.dumps(data, sort_keys=True, separators=(',', ':'))
        
        hash_local = hashlib.md5(dataLocal.encode('utf-8')).hexdigest()
        hash_server = hashlib.md5(dataServer.encode('utf-8')).hexdigest()

        print(hash_local)
        print(hash_server)

        if hash_local == hash_server:
            # el JSON local y el JSON del server son iguales
            print("El JSON local y el JSON del servidor son iguales.")
        else:
            # los JSON son diferentes
            print("Los JSON son diferentes.")
            reescribir("C:/Users/David/Desktop/thiago/python/fetch tiritas/data.json", data)  # Reescribe el JSON en un formato legible, porque sino lo toma horrible
            
    else:
        print("No se pudo acceder al JSON en el servidor.")
    
    
schedule.every(10).minutes.do(fetchJson)


while True:
    schedule.run_pending()
    time.sleep(60)


