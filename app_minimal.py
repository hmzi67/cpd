"""
Streamlit Cloud - Minimal Working Version
Cervical Pose Detection System with simplified imports
"""
import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import tempfile
import os
from pathlib import Path

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Cervical Pose Detection System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def process_frame_simple(image):
    """Simple pose processing without complex imports"""
    # Initialize pose detection
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = pose.process(rgb_image)
        
        # Draw pose landmarks
        annotated_image = image.copy()
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Simple exercise detection based on key landmarks
            landmarks = results.pose_landmarks.landmark
            
            # Get key points
            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            # Simple detection logic
            exercise_status = {
                "Pose Detected": True,
                "Head Position": f"X: {nose.x:.2f}, Y: {nose.y:.2f}",
                "Shoulder Level": abs(left_shoulder.y - right_shoulder.y) < 0.1
            }
        else:
            exercise_status = {"Pose Detected": False}
        
        return annotated_image, exercise_status

def process_uploaded_video(uploaded_file):
    """Process uploaded video file"""
    if uploaded_file is None:
        return
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    try:
        # Open video file
        cap = cv2.VideoCapture(tmp_path)
        
        if not cap.isOpened():
            st.error("❌ Could not open video file")
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        st.info(f"📹 Processing video: {total_frames} frames at {fps:.1f} FPS")
        
        # Create display containers
        video_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        frame_count = 0
        pose_detected_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 10th frame to speed up processing
            if frame_count % 10 == 0:
                processed_frame, status = process_frame_simple(frame)
                
                # Display frame
                video_placeholder.image(
                    cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_column_width=True,
                    caption=f"Frame {frame_count}/{total_frames}"
                )
                
                # Display status
                with status_placeholder.container():
                    if status.get("Pose Detected", False):
                        st.success("✅ Pose Detected")
                        pose_detected_frames += 1
                        for key, value in status.items():
                            if key != "Pose Detected":
                                st.write(f"**{key}:** {value}")
                    else:
                        st.warning("⚠️ No pose detected")
                
                progress_bar.progress(frame_count / total_frames)
            
            frame_count += 1
        
        cap.release()
        os.unlink(tmp_path)
        
        # Final summary
        detection_rate = (pose_detected_frames * 10) / total_frames * 100
        st.success(f"✅ Processing complete! Pose detected in {detection_rate:.1f}% of frames")
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def process_uploaded_image(uploaded_file):
    """Process uploaded image file"""
    try:
        # Read image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            st.error("❌ Could not read image")
            return
        
        # Process image
        processed_image, status = process_frame_simple(image)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        with col2:
            st.subheader("🔍 Processed Image")
            st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        # Show results
        st.subheader("📋 Detection Results")
        if status.get("Pose Detected", False):
            st.success("✅ Pose Successfully Detected!")
            for key, value in status.items():
                if key != "Pose Detected":
                    st.write(f"**{key}:** {value}")
        else:
            st.warning("⚠️ No pose detected in image")
        
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")

def main():
    """Main application"""
    configure_page()
    
    # Header
    st.title("🏥 Cervical Pose Detection System")
    st.markdown("### Simplified Cloud Version - Upload videos or images for pose analysis")
    
    # Input method selection
    input_method = st.radio(
        "📁 Choose Input Method:",
        ["Upload Video", "Upload Image"],
        horizontal=True
    )
    
    if input_method == "Upload Video":
        st.subheader("📹 Upload Video File")
        uploaded_video = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a video file to analyze poses"
        )
        
        if uploaded_video is not None:
            with st.spinner("🔄 Processing video..."):
                process_uploaded_video(uploaded_video)
    
    else:  # Upload Image
        st.subheader("📷 Upload Image File")
        uploaded_image = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload an image to analyze pose"
        )
        
        if uploaded_image is not None:
            with st.spinner("🔄 Processing image..."):
                process_uploaded_image(uploaded_image)
    
    # Sidebar info
    with st.sidebar:
        st.subheader("ℹ️ About")
        st.markdown("""
        This is a simplified version optimized for Streamlit Cloud deployment.
        
        **Features:**
        - MediaPipe pose detection
        - Video/image upload support
        - Real-time pose visualization
        - Basic pose analysis
        
        **Usage:**
        1. Upload a video or image
        2. View pose detection results
        3. Check detection statistics
        """)
        
        st.subheader("🔧 Technical Info")
        st.json({
            "MediaPipe": "✅ Loaded",
            "OpenCV": "✅ Loaded", 
            "Streamlit": "✅ Ready",
            "Cloud Optimized": "✅ Yes"
        })

if __name__ == "__main__":
    main()
