import detectFaces
import requests
from Crypto.PublicKey import RSA

if __name__ == "__main__":
    idul = 'pisne'
    url = 'http://127.0.0.1:8000/connection-pisne/'
    client = requests.session()
    client.get(url)
    csrf_token = client.cookies['csrftoken']
    # detectFaces.detectWebcam.takeref.takepicture()
    photo = {'photo': (idul+'.png',
                       open('./detectFaces/faces/etudiant.png', 'rb').read())}
    payload = {'idul': idul, 'csrfmiddlewaretoken': csrf_token}
    r = client.post(url, data=payload, files=photo)
    # detectFaces.detectWebcam.detectStudent()
