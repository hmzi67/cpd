"""
Example script to create sample data for testing the Streamlit app
"""
import cv2
import numpy as np
import os

def create_sample_video():
    """Create a simple sample video for testing"""
    
    # Video properties
    width, height = 640, 480
    fps = 30
    duration = 10  # seconds
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('sample_exercise_video.mp4', fourcc, fps, (width, height))
    
    print(f"Creating sample video: {total_frames} frames at {fps} FPS")
    
    for frame_num in range(total_frames):
        # Create a simple animated frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add background
        frame[:] = (50, 50, 50)
        
        # Add moving elements to simulate a person
        center_x = width // 2
        center_y = height // 2
        
        # Simulate head movement (neck exercises)
        time_factor = frame_num / total_frames
        
        # Head position (simulating neck movement)
        head_offset_x = int(30 * np.sin(time_factor * 4 * np.pi))
        head_offset_y = int(20 * np.cos(time_factor * 2 * np.pi))
        
        head_x = center_x + head_offset_x
        head_y = center_y - 100 + head_offset_y
        
        # Draw simple stick figure
        # Body
        cv2.line(frame, (center_x, center_y), (center_x, center_y + 100), (255, 255, 255), 3)
        
        # Head
        cv2.circle(frame, (head_x, head_y), 25, (255, 255, 255), 2)
        
        # Shoulders
        shoulder_y = center_y - 50
        cv2.line(frame, (center_x - 40, shoulder_y), (center_x + 40, shoulder_y), (255, 255, 255), 3)
        
        # Neck
        cv2.line(frame, (center_x, shoulder_y), (head_x, head_y + 25), (255, 255, 255), 3)
        
        # Add text overlay
        exercise_name = "Cervical Exercise Simulation"
        cv2.putText(frame, exercise_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_num + 1}/{total_frames}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        out.write(frame)
        
        if frame_num % 30 == 0:
            print(f"Progress: {frame_num}/{total_frames} frames")
    
    out.release()
    print("✅ Sample video created: sample_exercise_video.mp4")
    print("📁 You can use this video to test the Streamlit app")

def create_sample_image():
    """Create a sample image for testing"""
    width, height = 640, 480
    
    # Create image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (50, 50, 50)
    
    # Draw simple person pose
    center_x = width // 2
    center_y = height // 2
    
    # Head
    cv2.circle(image, (center_x, center_y - 100), 25, (255, 255, 255), 2)
    
    # Body
    cv2.line(image, (center_x, center_y - 75), (center_x, center_y + 100), (255, 255, 255), 3)
    
    # Shoulders
    cv2.line(image, (center_x - 40, center_y - 50), (center_x + 40, center_y - 50), (255, 255, 255), 3)
    
    # Arms
    cv2.line(image, (center_x - 40, center_y - 50), (center_x - 60, center_y), (255, 255, 255), 3)
    cv2.line(image, (center_x + 40, center_y - 50), (center_x + 60, center_y), (255, 255, 255), 3)
    
    # Text
    cv2.putText(image, "Sample Cervical Pose", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Save image
    cv2.imwrite('sample_exercise_image.jpg', image)
    print("✅ Sample image created: sample_exercise_image.jpg")
    print("📁 You can use this image to test the Streamlit app")

if __name__ == "__main__":
    print("🎬 Creating sample data for Streamlit app testing...")
    print("=" * 50)
    
    create_sample_video()
    print()
    create_sample_image()
    
    print("\n🎯 Testing Instructions:")
    print("1. Run the Streamlit app: streamlit run app_cloud.py")
    print("2. Choose 'Upload Video' and select 'sample_exercise_video.mp4'")
    print("3. Or choose 'Upload Image' and select 'sample_exercise_image.jpg'")
    print("4. View the pose detection results!")
