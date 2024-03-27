import cv2

# box1 =  ((6.249319076538086, -0.0013999241637066007), (2.052734375, 4.46484375), 0.5660619783215225)
# box2 = ((6.089120388031006, -2.7699127197265625), (2.048828125, 4.53515625), 0.4060735034756362)
box1 =  ((-0.0013999241637066007,6.249319076538086), (2.052734375, 4.46484375), 0.5660619783215225)
box2 = ((-2.7699127197265625,6.089120388031006), (2.048828125, 4.53515625), 0.4060735034756362)
r = cv2.rotatedRectangleIntersection(box1,box2)
print(r[0])