from flask import Flask, request
import socket, pickle, json, cv2, math
from imgReg import run
import tensorflow as tf
from cnn import CNN
import matplotlib.pyplot as plt

img_count = 0 # to assign image name
cnn = CNN()
graph = tf.get_default_graph()
app = Flask(__name__)

# Endpoint to receive image data then localizes and classifies images
@app.route('/', methods=['POST'])
def receiveImage():
    global img_count, graph, predictions, images
    content = request.data
    frame = pickle.loads(content) # get serialized data
    cv2.imwrite("../raw/img"+str(img_count)+".jpg", frame)
    img_count += 1
    pred, img = run(frame, graph, cnn, img_count)
    predictions.append(pred)
    if img is not None:
        images.append(img)
    return ('', 204) # return a no content response

# Endpoint to send classification results to algo team
@app.route('/end', methods=['GET'])
def finished():
    global predictions
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(content, f, ensure_ascii=False, indent=4)
    # print("done")
    #data = {303: [[1, 0, 0, 50, 50]], 400: [[1, 0, 0, 50, 50], [2, 50,50,50,50]]}
    # return ('', 204) # return a no content response
    return json.dumps(predictions)

# for debug
def forDebug():
    global img_count, graph, predictions, images
    import os
    for f in os.listdir("../old-mdp/newImages/raw8")[:5]:
        frame = cv2.imread("../old-mdp/newImages/raw8/"+f)
        pred, img = run(frame, graph, cnn, img_count)
        img_count+=1
        predictions.append(pred)
        if img is not None:
            images.append(img)

# for debug
def debugEnd():
    global predictions, images
    print(json.dumps(predictions))
    _, axs = plt.subplots(math.ceil(len(images)/3), 3, gridspec_kw = {'wspace':0, 'hspace':0}, figsize=(100,100))
    for img, ax in zip(images, axs.flatten()):
        ax.imshow(img)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    plt.show()

if __name__ == '__main__':
    RPI = "192.168.16.16"
    TEMP_PORT = 8125
    predictions = []
    images = []

    # MY_IP = socket.gethostbyname(socket.getfqdn()) # get my IP address
    # print(MY_IP)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # while True:
    #     try:
    #         s.connect((RPI, TEMP_PORT)) # to establish connection with RPI
    #         break
    #     except ConnectionRefusedError:
    #         print("Connection failed. Retrying...")
    #         continue
    # s.close() # close socket
    # app.run(host='0.0.0.0', port=8123)
    forDebug()
    debugEnd()