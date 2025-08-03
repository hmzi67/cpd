"""
Cloud-optimized Streamlit application for cervical pose detection system.
Supports both file upload and live camera (when available).
"""
import streamlit as st
import cv2
import time
import sys
import os
import tempfile
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.models import SystemConfig
from src.core.video_processor import VideoProcessor
from src.ui.components import UIComponents, SessionManager


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Cervical Pose Detection System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/hmzi67/cervical-posture-detection.git',
            'Report a bug': 'https://github.com/hmzi67/cervical-posture-detection/issues',
            'About': """
            # Cervical Pose Detection System
            
            A real-time system for detecting and providing feedback on cervical exercises
            using computer vision and pose estimation.
            
            **Features:**
            - Real-time pose detection
            - 5 cervical exercise types
            - Automatic calibration
            - Performance feedback
            """
        }
    )


def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Exercise status indicators */
    .exercise-active {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .exercise-inactive {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    
    /* Video container */
    .video-container {
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 10px;
        background-color: #f8f9fa;
    }
    
    /* Performance stats */
    .stats-container {
        background-color: #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def process_uploaded_video(uploaded_file, video_processor, config):
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
            st.error("❌ Could not open video file. Please check the format.")
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        st.info(f"📹 Video loaded: {duration:.1f}s, {total_frames} frames, {fps:.1f} FPS")
        
        # Create containers for display
        video_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        # Process video frame by frame
        frame_count = 0
        results_history = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            try:
                processed_frame, exercise_results = video_processor.process_frame(frame)
                results_history.append(exercise_results)
                
                # Convert BGR to RGB for display
                display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Update display every 10 frames to avoid too many updates
                if frame_count % 10 == 0:
                    video_placeholder.image(
                        display_frame,
                        channels="RGB",
                        use_column_width=True,
                        caption=f"Frame {frame_count}/{total_frames}"
                    )
                    
                    with status_placeholder.container():
                        UIComponents.render_exercise_status_panel(exercise_results, None)
                    
                    progress_bar.progress(frame_count / total_frames)
                
                frame_count += 1
                
            except Exception as e:
                st.error(f"❌ Error processing frame {frame_count}: {str(e)}")
                break
        
        cap.release()
        os.unlink(tmp_path)  # Clean up temporary file
        
        # Show final results
        if results_history:
            st.success(f"✅ Video processing complete! Processed {len(results_history)} frames.")
            
            # Calculate summary statistics
            exercise_counts = {}
            for results in results_history:
                for exercise_name, is_active in results.items():
                    if is_active:
                        exercise_counts[exercise_name] = exercise_counts.get(exercise_name, 0) + 1
            
            if exercise_counts:
                st.subheader("📊 Exercise Summary")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Detected Exercises:**")
                    for exercise, count in exercise_counts.items():
                        percentage = (count / len(results_history)) * 100
                        st.write(f"- {exercise}: {count} frames ({percentage:.1f}%)")
                
                with col2:
                    # Simple visualization
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(8, 6))
                    exercises = list(exercise_counts.keys())
                    counts = list(exercise_counts.values())
                    ax.bar(exercises, counts)
                    ax.set_title("Exercise Detection Frequency")
                    ax.set_ylabel("Frame Count")
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
        
    except Exception as e:
        st.error(f"❌ Video processing failed: {str(e)}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def process_uploaded_image(uploaded_file, video_processor):
    """Process uploaded image file"""
    if uploaded_file is None:
        return
    
    try:
        # Read image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            st.error("❌ Could not read image file. Please check the format.")
            return
        
        # Process image
        processed_image, exercise_results = video_processor.process_frame(image)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        with col2:
            st.subheader("🔍 Processed Image")
            st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        # Show exercise results
        st.subheader("📋 Exercise Detection Results")
        UIComponents.render_exercise_status_panel(exercise_results, None)
        
    except Exception as e:
        st.error(f"❌ Image processing failed: {str(e)}")


def main():
    """Main application entry point"""
    configure_page()
    apply_custom_styles()
    
    # Initialize session state
    SessionManager.initialize_session_state()
    
    # Application header
    st.title("🏥 Cervical Pose Detection System")
    st.markdown("### Real-time cervical exercise detection and feedback system")
    
    # Deployment mode info
    st.info("🌐 **Cloud Deployment Mode**: Upload videos or images for analysis. Live camera requires local deployment.")
    
    # Create main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input method selection
        input_method = st.radio(
            "📁 Choose Input Method:",
            ["Upload Video", "Upload Image", "Live Camera (if available)"],
            horizontal=True
        )
        
        # Initialize video processor
        config = SystemConfig()
        video_processor = VideoProcessor(config)
        
        if input_method == "Upload Video":
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            st.subheader("📹 Upload Video File")
            uploaded_video = st.file_uploader(
                "Choose a video file",
                type=['mp4', 'avi', 'mov', 'mkv'],
                help="Upload a video file to analyze cervical exercises"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_video is not None:
                with st.spinner("🔄 Processing video..."):
                    process_uploaded_video(uploaded_video, video_processor, config)
        
        elif input_method == "Upload Image":
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            st.subheader("📷 Upload Image File")
            uploaded_image = st.file_uploader(
                "Choose an image file",
                type=['jpg', 'jpeg', 'png', 'bmp'],
                help="Upload an image to analyze cervical pose"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded_image is not None:
                with st.spinner("🔄 Processing image..."):
                    process_uploaded_image(uploaded_image, video_processor)
        
        else:  # Live Camera
            st.warning("📷 **Live Camera Mode**: This requires local deployment or browser camera access.")
            st.info("💡 For live camera functionality, run this app locally using: `streamlit run main.py`")
            
            # Check if we can access camera (will fail in cloud)
            if st.button("🔄 Try Camera Access"):
                try:
                    cap = cv2.VideoCapture(0)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            st.success("✅ Camera access successful!")
                            # Here you could implement the live camera logic from original main.py
                        cap.release()
                    else:
                        st.error("❌ Could not access camera. Please use file upload instead.")
                except Exception as e:
                    st.error(f"❌ Camera access failed: {str(e)}")
                    st.info("💡 Use file upload method for cloud deployment.")
    
    with col2:
        # Sidebar content
        st.subheader("🎯 Exercise Types")
        st.markdown("""
        **Supported Exercises:**
        - 🔽 Cervical Flexion
        - 🔼 Cervical Extension  
        - ↔️ Lateral Neck Tilt (L/R)
        - 🔄 Cervical Rotation (L/R)
        """)
        
        st.subheader("ℹ️ Instructions")
        st.markdown("""
        1. **Upload a video** of cervical exercises
        2. **Or upload an image** for single pose analysis
        3. **View real-time feedback** and results
        4. **Check exercise summary** after processing
        """)
        
        st.subheader("📊 System Info")
        stats = video_processor.get_system_stats()
        st.json({
            "MediaPipe Model": "Pose Landmarker",
            "Processing Mode": "Cloud Optimized",
            "Supported Formats": ["MP4", "AVI", "MOV", "JPG", "PNG"],
            "Max File Size": "200MB"
        })
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔬 Cervical Pose Detection System | Built with Streamlit & MediaPipe</p>
        <p>📧 For support: <a href='https://github.com/hmzi67/cervical-posture-detection'>GitHub Repository</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
