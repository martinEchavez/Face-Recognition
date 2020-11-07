from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
import cv2
import os

app = Flask(__name__)

CORS(app)

app.config['MONGO_URI']='mongodb://localhost/Recognizer'
mongo = PyMongo(app)

db = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
 full_name = request.json['name'] + ' ' + request.json['lastName']
 create_images(full_name)
 #print(nombre_completo)
 id = db.insert({
  'name': request.json['name'],
  'lastName': request.json['lastName'],
  'tipeUser': request.json['tipeUser'],
  'idNumber': request.json['idNumber'],
  'cellPhone': request.json['cellPhone'],
  'email': request.json['email']
 })
 return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
 users = []
 for doc in db.find():
  users.append({
   '_id': str(ObjectId(doc['_id'])),
   'name': doc['name'],
   'lastName': doc['lastName'],
   'tipeUser': doc['tipeUser'],
   'idNumber': doc['idNumber'],
   'cellPhone': doc['cellPhone'],
   'email': doc['email']
  })
 return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
 user = db.find_one({'_id': ObjectId(id)})
 return jsonify({
  '_id': str(ObjectId(user['_id'])),
  'name': user['name'],
  'lastName': user['lastName'],
  'tipeUser': user['tipeUser'],
  'idNumber': user['idNumber'],
  'cellPhone': user['cellPhone'],
  'email': user['email']
 })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
 db.delete_one({'_id': ObjectId(id)})
 return jsonify({'msg': 'Usuario eliminado'})

@app.route('/users/<id>', methods=['PUT'])
def apdateUser(id):
 db.update_one({'_id': ObjectId(id)}, {'$set': {
  'name': request.json['name'],
  'lastName': request.json['lastName'],
  'tipeUser': request.json['tipeUser'],
  'idNumber': request.json['idNumber'],
  'cellPhone': request.json['cellPhone'],
  'email': request.json['email'],
 }})
 return jsonify({'msg': 'Usuario actualizado'})

def create_images(full_name):
 #Método cascade
 faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

 def generate_dataset(img, full_name, img_id):
  print(full_name)
  if not os.path.isdir("knn_examples/train/"+str(full_name)):
   os.mkdir("knn_examples/train/"+str(full_name))
  else:
   cv2.imwrite("knn_examples/train/"+str(full_name)+"/"+str(img_id)+".jpg", img)

 #Funcion para pintar el cuadro
 def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, full_name):
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
  coords = []
  for (x, y, w, h) in features:
   cv2.rectangle(img, (x,y), (x+w, y+h), color, 1)#Dibujamos el rectangulo
   cv2.putText(img, full_name, (x, y-2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1, cv2.LINE_AA)
   coords = [x, y, w, h]#Coordenadas
  return coords

 def detect(img, faceCascade, img_id):
  color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0)}
  coords = draw_boundary(img, faceCascade, 1.1, 10, color['green'], full_name)
  if len(coords)==4:
   roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
   generate_dataset(roi_img, full_name, img_id)
  return img

 #Capture video
 video_capture = cv2.VideoCapture(0)

 img_id = 0

 while True:
  _, video = video_capture.read()
  #Rotamos el video
  video = cv2.flip(video, 1)
  video = detect(video, faceCascade, img_id)
  #Mostramos el video
  cv2.imshow('Frame', video)
  img_id +=1
  #Cerramos el Frame pulsando q
  if cv2.waitKey(1) & 0xFF == ord('q'):
   break
  elif img_id == 50:
   break

 #Destruimos la sesión
 video_capture.release()
 cv2.destroyAllWindows()

@app.route('/start', methods=['POST'])
def iniciar():
  start = request.json['start']
  if start:
   print('Iniciando...')
   os.system("python facerec_ipcamera_knn.py")
  return jsonify({'msg': 'Finalizado'})

if __name__ == "__main__":
 app.run(debug=True)