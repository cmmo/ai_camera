import uvc
import logging
logging.basicConfig(level=logging.INFO)

dev_list =  uvc.device_list()
print("devices: ", dev_list)
cap = uvc.Capture(dev_list[0]['uid'])
print(dir(cap))

frame = None
cap.frame_mode = (1920, 1080, 30)

with open("out.mjpg","wb+") as fd:
  for i in range(300):
    print("frame ", i)
    frame = cap.get_frame_robust() 
    fd.write(frame.jpeg_buffer)
    frame = None
  fd.close()

print("done writing")

cap = None