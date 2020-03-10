import cv2
import numpy as np

img_bound = 240
class_mapping = {'up':1, 'down':2, 'right':3, 'left':4, 'circle':5, 'one':6, 'two':7,
                'three':8, 'four':9, 'five':10, 'a':11, 'b':12, 'c':13, 'd':14, 'e':15} # mapping for class id

def getPredictions(frame, processor, box, color, graph, model):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    x, y, w, h = box
    cropped = frame[y:y+h, x:x+w] 
    cropped = processor.resizeNormalize(cropped, model.channels) 
    if color == 'yellow':
        return model.yellowPredict(graph, cropped)
    elif color == 'red':
        return model.redPredict(graph, cropped)
    elif color == 'green':
        return model.greenPredict(graph, cropped)
    elif color == 'blue':
        return model.bluePredict(graph, cropped)
    else:
        return model.whitePredict(graph, cropped)

def getBoundingBoxes(contours):
    boxes = []
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        area = cv2.contourArea(contour)
        if area < 800:
            break
        elif area > 15000:
            continue
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        if w < 20 or h < 20: # too small, ignore
            break
        if w > 2*h: # width too big, unlikely our target
            continue
        boxes.append(np.array(rect))
    return np.array(boxes)

def run(frame, graph, model, count):
    THRESHOLD = 0.999
    cropped = frame[img_bound:, :]
    gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    thresh0 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 0)
    contours, _ = cv2.findContours(thresh0, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    boxes = getBoundingBoxes(contours)
    predictions = []
    if len(boxes) > 0:
        for box in boxes:
            x, y, w, h = box
            target = blurred[y:y+h, x:x+w] # crop out the bounding box image
            resized = cv2.resize(target, dsize=(model.dim, model.dim), interpolation=cv2.INTER_CUBIC)
            normed = resized/255 # normalize before pass through CNN
            predictions.append((model.predict(graph, normed), box))

    if len(predictions) == 0:
        return [-1], None

    results = []
    #return predictions
    for pred in predictions:
        prob = pred[0][1].item()
        if prob > THRESHOLD:
            x, y, w, h = pred[1]
            y = y+img_bound
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            text = "{}: {:.4f}%".format(pred[0][0].upper(), prob*100)
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            results.append(class_mapping.get(pred[0][0]))
                
    #cv2.imwrite('./processed/p_img'+str(count)+'.jpg', frame)
    if len(results) == 0:
        return [-1], None
    return results, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)