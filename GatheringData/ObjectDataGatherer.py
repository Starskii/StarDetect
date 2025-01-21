from PIL import ImageGrab
import time

image_count = 100
start = time.time()
print(start)
for image_index in range(image_count):
    image = ImageGrab.grab()
    image.save('data/img' + str(image_index) + '.png')
    image.close()
end = time.time()
print("Started at: " + str(start))
print("Ended at: " + str(end))
print("Process took: " + str(end - start) + " seconds")
print("Captured " + str(image_count / (end - start)) + " per second.")
