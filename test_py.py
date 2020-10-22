import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
import cv2

ctype_uint8 = ct.c_uint8
c_uint8p = ct.POINTER(ctype_uint8)  
ctype_float = ct.c_float
videoPath = "challenge.mp4"

# Import module
pyModule = npct.load_library('libpymodule.so', '.')
module = pyModule.frameProcessing_new()
def inputPointTest(cv_frame,  height, width):
    out = np.copy(cv_frame)
    
    # in C++ side, only allows 3 channel input
    if len(out.shape) == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    pyModule.frameProcessing_startPoint(module, out.ctypes.data_as(c_uint8p), height, width)
    return out

#print(inputPointTest())
def Video(openpath, savepath = None):
    cap = cv2.VideoCapture(openpath)
    if cap.isOpened():
        print("Video Opened")
    else:
        print("Video Not Opened")
        print("Program Abort")
        exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = None
    if savepath is not None:
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        out = cv2.VideoWriter(savepath, fourcc, fps, (width, height), True)
    cv2.namedWindow("Frame", cv2.WINDOW_GUI_EXPANDED)
    cv2.namedWindow("output", cv2.WINDOW_GUI_EXPANDED)
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Our operations on the frame come here
            output = inputPointTest(frame,  height, width)
            
            #output = OpenCV_Functions.imageProcessing(frame)
            if out is not None:
                # Write frame-by-frame
                out.write(output)
            # Display the resulting frame
            cv2.imshow("Frame", frame)
            cv2.imshow("output", output)
            #cv2.waitKey()
        else:
            break
        # waitKey(int(1000.0/fps)) for matching fps of video
        
        if cv2.waitKey(int(1000.0/fps)) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    return
Video(videoPath, None)