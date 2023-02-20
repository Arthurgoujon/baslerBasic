import cv2
import time
from pypylon import pylon

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()
fps_avg_frame_count = 10

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
#camera.Open()
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

cv2.namedWindow("baslerTest", cv2.WINDOW_NORMAL)
cv2.resizeWindow("baslerTest", 950, 600)  

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        counter += 1
        image = converter.Convert(grabResult)
        frame = image.GetArray()
        #frame = grabResult.GetArray()

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
        font_size, text_color, font_thickness)
        print(fps_text)

        cv2.imshow('baslerTest', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grabResult.Release()

cv2.destroyAllWindows()


