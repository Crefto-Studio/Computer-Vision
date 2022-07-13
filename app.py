from flask import Flask, render_template, Response
import cv2 as cv
import numpy as np
import win32api


app = Flask(__name__)
camera = cv.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)



def gen_frames():  # generate frame by frame from camera
    def nothing(x):
        pass

    # colors
    white = (255,255,255)
    black = (0,0,0)

    #RGBY
    colors = [(255,0,0) , (0,255,0) , (0,0,255) , (0,255,255)]

    #paint window initialization
    paint_window = np.zeros((471 , 636,3) ) + 255
    paint_window = cv.rectangle(paint_window, (40,1), (140,65), black,2)
    cv.putText(paint_window, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, black,2)
    points=[]
    
    #for disjoint of drawing
    flag =0

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            
            frame = cv.flip(frame, 1)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # assign values to lh ,ls,  lv ... etc
            l_h = 130
            l_s = 110
            l_v = 15
            u_h = 277
            u_s = 277
            u_v = 277

            upper_hsv = np.array([u_h ,u_s, u_v])
            lower_hsv = np.array([l_h , l_s, l_v])

            # button
            frame = cv.rectangle(frame, (40,1), (140,65), black,-1)
            cv.putText(frame, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, white,2)

            # Mask
            kernel = np.ones((5,5),np.uint8)
            mask = cv.inRange(hsv, lower_hsv, upper_hsv)

            #Key Event (Space)
            space = win32api.GetKeyState(32)

            #Countour Line and Drawing
            if flag ==1 and space >= 0:
                flag=0
            
            if space < 0:
                mask = cv.erode(mask, kernel, iterations=1)
                mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
                mask = cv.dilate(mask, kernel, iterations=1)
                cnts, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2:]
                center = None
                if len(cnts) > 0 :
                    cnt = sorted(cnts,key= cv.contourArea, reverse=True)[0]
                    ((x,y),raduis) = cv.minEnclosingCircle(cnt)


                    M= cv.moments(cnt)
                    center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']) )
                    
                    if center[1] <= 65 : #CLEAR
                        if  40<= center[0] <= 140 :
                            points = []
                            paint_window [: , : , :]  = 255

                    points.insert(0, center)

                    if flag==0 :
                        flag=1
                        for i in range(1,len(points)):
                            points[i] = points[0]

                    else :
                        for i in range(1,len(points)):
                            cv.line(frame, points[i-1], points[i], colors[0] ,2)
                            cv.line(paint_window, points[i-1], points[i], colors[0] ,2)
            else :
                    flag=0
                    for i in range(1,len(points)):
                        points[i] = points[0]

            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_paint():  # generate paint_window after being edited in frame function
    def nothing(x):
        pass

    # colors
    white = (255,255,255)
    black = (0,0,0)

    #RGBY
    colors = [(255,0,0) , (0,255,0) , (0,0,255) , (0,255,255)] 

    #paint window initialization
    paint_window = np.zeros((471 , 636,3) ) + 255
    paint_window = cv.rectangle(paint_window, (40,1), (140,65), black,2)
    cv.putText(paint_window, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, black,2)
    points=[]

    #for disjoint of drawing
    flag =0 

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            
            frame = cv.flip(frame, 1)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # assign values to lh ,ls,  lv ... etc
            l_h = 130
            l_s = 110
            l_v = 15
            u_h = 277
            u_s = 277
            u_v = 277

            upper_hsv = np.array([u_h ,u_s, u_v])
            lower_hsv = np.array([l_h , l_s, l_v])

            # button
            frame = cv.rectangle(frame, (40,1), (140,65), black,-1)
            cv.putText(frame, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, white,2)

            # Mask
            kernel = np.ones((5,5),np.uint8)
            mask = cv.inRange(hsv, lower_hsv, upper_hsv)

            #Key Event (Space)
            space = win32api.GetKeyState(32)

            #Countour Line and Drawing
            if flag ==1 and space >= 0:
                flag=0
            
            if space < 0:
                mask = cv.erode(mask, kernel, iterations=1)
                mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
                mask = cv.dilate(mask, kernel, iterations=1)
                cnts, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2:]
                center = None
                if len(cnts) > 0 :
                    cnt = sorted(cnts,key= cv.contourArea, reverse=True)[0]
                    ((x,y),raduis) = cv.minEnclosingCircle(cnt)


                    M= cv.moments(cnt)
                    center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']) )
                    
                    if center[1] <= 65 : #CLEAR
                        if  40<= center[0] <= 140 :
                            points = []
                            paint_window [: , : , :]  = 255

                    points.insert(0, center)

                    if flag==0 :
                        flag=1
                        for i in range(1,len(points)):
                            points[i] = points[0]

                    else :
                        for i in range(1,len(points)):
                            cv.line(frame, points[i-1], points[i], colors[0] ,2)
                            cv.line(paint_window, points[i-1], points[i], colors[0] ,2)
            else :
                    flag=0
                    for i in range(1,len(points)):
                        points[i] = points[0]
            
            ret, buffer = cv.imencode('.jpg', paint_window)
            paint = buffer.tobytes()
            yield (b'--paint\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + paint + b'\r\n')  # concat frame one by one and show result

            
            

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_paint')
def video_paint():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_paint(), mimetype='multipart/x-mixed-replace; boundary=paint')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)