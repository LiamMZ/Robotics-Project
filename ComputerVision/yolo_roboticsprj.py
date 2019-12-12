import cv2
import argparse
import numpy as np

class ComputerVision:
    def __init__(self, args):
        with open(args.classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        #build net using weights argument and net conficuration argument
        self.net = cv2.dnn.readNet(args.weights, args.config)
    
    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        #gets layer names of unconnected output layers
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        return output_layers
    
    def findTarget(self, image, target):
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        #convert image to 4 dimensional blob, scale by scale-factor
        blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
        #set new input values
        self.net.setInput(blob)
        #computes output layer values based on names of output layers
        outs = self.net.forward(self.get_output_layers())

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        #loop through output layer values
        for out in outs:
            #loops through detections
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        indices = [i[0] for i in indices]
        class_ids = [class_ids[i] for i in indices]
        center = [-1,-1]
        if self.classes.index(target) in class_ids:
            index = class_ids.index(self.classes.index(target))
            center = [round((boxes[index][0]+boxes[index][2])/2), round((boxes[index][1]+boxes[index][3]))]
        return center
