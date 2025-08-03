#!/bin/bash

# Streamlit Deployment Script
# Run this script to prepare and deploy your cervical posture detection app

echo "🚀 Cervical Pose Detection - Streamlit Deployment Helper"
echo "======================================================"

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a Git repository. Please initialize git first:"
    echo "   git init"
    echo "   git remote add origin https://github.com/hmzi67/cervical-posture-detection.git"
    exit 1
fi

echo "✅ Git repository detected"

# Check current status
echo "📋 Current repository status:"
git status --porcelain

# Ask user which version to deploy
echo ""
echo "🎯 Choose deployment version:"
echo "1. Original version (main.py) - For local deployment with live camera"
echo "2. Cloud-optimized version (app_cloud.py) - For Streamlit Community Cloud"
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo "📝 Using original version (main.py)"
        MAIN_FILE="main.py"
        ;;
    2)
        echo "📝 Using cloud-optimized version (app_cloud.py)"
        # Copy cloud version to main.py for deployment
        cp app_cloud.py main.py
        MAIN_FILE="main.py"
        echo "✅ Cloud-optimized version copied to main.py"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

# Add and commit changes
echo ""
echo "💾 Preparing repository for deployment..."

# Add all files
git add .

# Commit changes
read -p "📝 Enter commit message (default: 'Prepare for Streamlit deployment'): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Prepare for Streamlit deployment"
fi

git commit -m "$commit_msg"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Ready for Streamlit Cloud Deployment!"
    echo "======================================"
    echo ""
    echo "Next steps:"
    echo "1. Visit: https://share.streamlit.io"
    echo "2. Sign in with your GitHub account"
    echo "3. Click 'New app'"
    echo "4. Select repository: hmzi67/cervical-posture-detection"
    echo "5. Branch: main"
    echo "6. Main file path: main.py"
    echo "7. Click 'Deploy!'"
    echo ""
    echo "📱 Your app will be available at:"
    echo "   https://cervical-posture-detection-[random-string].streamlit.app"
    echo ""
    echo "🔧 Additional configurations:"
    echo "   - .streamlit/config.toml has been created for optimal settings"
    echo "   - requirements.txt updated for cloud compatibility"
    echo "   - Documentation available in docs/STREAMLIT_DEPLOYMENT.md"
    echo ""
else
    echo "❌ Failed to push to GitHub. Please check your Git configuration."
    echo "💡 Make sure you have proper access to the repository."
fi

echo ""
echo "📚 For detailed deployment instructions, see:"
echo "   docs/STREAMLIT_DEPLOYMENT.md"
