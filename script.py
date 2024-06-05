import cv2
import pytesseract
import pandas as pd
import matplotlib.pyplot as plt

# Initialize video capture
video_path = 'trimmed-falcon-launch.mp4'
cap = cv2.VideoCapture(video_path)


fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

# Define start and end times in seconds
start_time = 3  # 3 seconds
end_time = 23   # 527 (original value for this video)


# Calculate start and end frames
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

total_frames = end_frame - start_frame 


# print(f"FPS: {fps}")
# print(f"Width: {width}")
# print(f"Height: {height}")
# print(f"Frame Count: {frame_count}")
# print(f"Duration (seconds): {duration}")


# Define the coordinates of the region of interest (ROI)
# (x, y, width, height)
# Stage 1 Speed Bounding Box Co-ordinates
x, y, w, h = 105, 960, 125, 48 

# Stage 1 Altitude Bounding Box Co-ordinates
x2, y2, w2, h2 = 265, 960, 125, 48  

# Perform OCR on the cropped image
# custom_config = r'--oem 3 --psm 6'
custom_config = r'-c tessedit_char_whitelist=0123456789. --psm 6'

current_frame = 0; 

img = []

speed_data = [] 
altitude_data = [] 
frame_data = []
gray_speed_data = [] 
gray_altitude_data = []

print(f"Total Frames to process: {total_frames}")

while current_frame < end_frame:

    if current_frame % 100 == 0:
        print(f"{current_frame}/{end_frame}")

    if current_frame < start_frame:
        ret = cap.grab()
        current_frame += 1
        continue

    ret, frame = cap.read()


    if not ret: # ret = false => means the frames have ended
        printf("No more frames present in the image")
        break




    if (current_frame - start_frame) % 15 == 0: 

        s1_speed = frame[y:y+h, x:x+w]
        s1_altitude = frame[y2:y2+h2, x2:x2+w2]


        s1_speed_gray = cv2.cvtColor(s1_speed, cv2.COLOR_RGB2GRAY)
        s1_altitude_gray = cv2.cvtColor(s1_altitude, cv2.COLOR_RGB2GRAY)



        speed_output_path = f"run-3/speed-{current_frame}.jpg"
        altitude_output_path = f"run-3/altitude-{current_frame}.jpg"

        speed_output_path_gray = f"run-3-gray/speed-{current_frame}-gray.jpg"
        altitude_output_path_gray = f"run-3-gray/altitude-{current_frame}-gray.jpg"


        cv2.imwrite(speed_output_path, s1_speed)
        cv2.imwrite(altitude_output_path, s1_altitude)

        cv2.imwrite(speed_output_path_gray, s1_speed_gray)
        cv2.imwrite(altitude_output_path_gray, s1_altitude_gray)

        s1_speed_text = pytesseract.image_to_string(s1_speed, config=custom_config)
        s1_altitude_text = pytesseract.image_to_string(s1_altitude, config=custom_config)


        s1_speed_text_gray = pytesseract.image_to_string(s1_speed_gray, config=custom_config)
        s1_altitude_text_gray = pytesseract.image_to_string(s1_altitude_gray, config=custom_config)

        speed_data.append(s1_speed_text)
        altitude_data.append(s1_altitude_text) 

        gray_speed_data.append(s1_speed_text_gray)
        gray_altitude_data.append(s1_altitude_text_gray) 

        frame_data.append(current_frame)



    current_frame += 1



print("speed data")
print(speed_data)

print("altitude data")
print(altitude_data)

print("frame data")
print(frame_data)

print("gray speed data")
print(gray_speed_data)

print("gray altitude data")
print(gray_altitude_data)




# while True:
#     cap.open(0)

### -

# # Initialize data storage
# data = {'time': [], 'altitude': [], 'speed': []}

# # Function to extract telemetry data from frame
# def extract_telemetry(frame):
#     # Convert frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     # Use pytesseract to do OCR on the frame
#     text = pytesseract.image_to_string(gray)
    
#     # Extract altitude and speed from the text
#     # This part depends on the format of the telemetry data in the video
#     # Assuming the text contains lines like "Altitude: 1000m" and "Speed: 2000m/s"
#     altitude = None
#     speed = None
#     for line in text.split('\n'):
#         if 'Altitude' in line:
#             altitude = float(line.split(':')[1].strip().replace('m', ''))
#         if 'Speed' in line:
#             speed = float(line.split(':')[1].strip().replace('m/s', ''))
    
#     return altitude, speed

# # Process video frames
# frame_rate = cap.get(cv2.CAP_PROP_FPS)
# frame_count = 0

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Extract telemetry data every second
#     if frame_count % int(frame_rate) == 0:
#         time = frame_count / frame_rate
#         altitude, speed = extract_telemetry(frame)
#         if altitude is not None and speed is not None:
#             data['time'].append(time)
#             data['altitude'].append(altitude)
#             data['speed'].append(speed)
    
#     frame_count += 1

# cap.release()

# # Convert data to DataFrame
# df = pd.DataFrame(data)

# # Plot the data
# plt.figure(figsize=(12, 6))

# # Plot altitude
# plt.subplot(2, 1, 1)
# plt.plot(df['time'], df['altitude'], label='Altitude')
# plt.xlabel('Time (s)')
# plt.ylabel('Altitude (m)')
# plt.title('Altitude vs Time')
# plt.legend()

# # Plot speed
# plt.subplot(2, 1, 2)
# plt.plot(df['time'], df['speed'], label='Speed', color='red')
# plt.xlabel('Time (s)')
# plt.ylabel('Speed (m/s)')
# plt.title('Speed vs Time')
# plt.legend()

# plt.tight_layout()
# plt.show()