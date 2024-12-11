import cv2
import os
import subprocess
from fpdf import FPDF
from skimage.metrics import structural_similarity as ssim
import numpy as np

def download_video(youtube_url, output_path="downloads_v2"):
    # Download YouTube video using yt-dlp
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    output_file = os.path.join(output_path, "video.mp4")
    command = [
        "yt-dlp",
        "-o", output_file,
        youtube_url
    ]
    subprocess.run(command, check=True)
    print(f"Video downloaded to: {output_file}")
    return output_file

def extract_screenshots(video_path, interval=5, output_path="screenshots_v2", similarity_threshold=0.95):
    # Extracts frames from the video at the specified time interval (in seconds),
    # saving only those that are sufficiently different from the last saved frame.
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))  
    frame_interval = int(fps * interval)  

    frame_count = 0
    screenshot_count = 0
    last_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if last_frame is not None:
                score, _ = ssim(last_frame, gray_frame, full=True)
                if score >= similarity_threshold:
                    print(f"Skipped similar frame at count: {frame_count}, similarity: {score:.2f}")
                    frame_count += 1
                    continue
            
            screenshot_file = os.path.join(output_path, f"screenshot_{screenshot_count:03d}.jpg")
            cv2.imwrite(screenshot_file, frame)
            print(f"Saved screenshot: {screenshot_file}")
            screenshot_count += 1
            last_frame = gray_frame
        
        frame_count += 1

    cap.release()
    print(f"Total screenshots saved: {screenshot_count}")
    return output_path

def create_pdf_from_images(image_folder, output_pdf):
    # Combines all images into PDF [3 images per page].
    pdf = FPDF()
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])

    if not image_files:
        print("No image to add in pdf!")
        return

    images_per_page = 3  
    image_height = 80    
    margin = 10          

    for i, image_file in enumerate(image_files):
        if i % images_per_page == 0:
            pdf.add_page()

        x = margin
        y = margin + (i % images_per_page) * (image_height + margin)
        
        image_path = os.path.join(image_folder, image_file)
        pdf.image(image_path, x=x, y=y, w=190, h=image_height)

    pdf.output(output_pdf)
    print(f"PDF created: {output_pdf}")


def clean_up_folder(folder_path):
    # Delete all files from folder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(folder_path)
    print(f"Cleaned up folder: {folder_path}")


if __name__ == "__main__":
    
    youtube_url = input("Enter YouTube video URL: ")
    video_path = download_video(youtube_url)
    screenshots_folder = extract_screenshots(video_path, interval=12)  

    os.remove(video_path)
    print(f"Deleted downloaded video: {video_path}")
        
    pdf_name = input("Enter the name for the PDF: ") 
    create_pdf_from_images(screenshots_folder, pdf_name)
    clean_up_folder(screenshots_folder)
    
    # path('../../../sem7/aiml/theory_AIML_Lecture1-8/yt/')
