import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not video.isOpened():
        print("Error opening video file")
        return

    # Get the frame rate of the video
    fps = video.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)

    frame_count = 0
    while True:
        # Read a frame
        success, frame = video.read()
        if not success:
            break

        # Save the frame as an image
        if frame_count % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    video.release()
    print(f"Extracted {frame_count // interval} frames.")

if __name__ == "__main__":
    video_path = r"data\video\grulla\grulla.mp4"
    output_folder = r"data\video\grulla\frames"
    extract_frames(video_path, output_folder)
