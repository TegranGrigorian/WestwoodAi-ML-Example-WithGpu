# This is a script to install the necessary components.
#!/bin/bash
# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Update package list
sudo apt-get update -y
sudo apt-get upgrade -y
# Install necessary packages
sudo apt install -y virtualenv python3-pip python3-dev build-essential unzip wget git

# Install NVIDIA GPU drivers and CUDA toolkit if requested
echo "Do you want this script to install GPU drivers and CUDA toolkit? (y/n)"
read install_gpu_drivers
if [ "$install_gpu_drivers" == "y" ]; then
    echo "Installing GPU drivers and CUDA toolkit..."
    sudo apt-get install -y nvidia-driver-525 nvidia-cuda-toolkit
    # Optionally install cuDNN (for advanced users, uncomment below)
    # wget https://developer.download.nvidia.com/compute/redist/cudnn/v8.9.2/cudnn-linux-x86_64-8.9.2.26_cuda11-archive.tar.xz
    # tar -xvf cudnn-linux-x86_64-8.9.2.26_cuda11-archive.tar.xz
    # sudo cp cudnn-*-archive/include/* /usr/local/cuda/include/
    # sudo cp cudnn-*-archive/lib/* /usr/local/cuda/lib64/
    echo "GPU drivers and CUDA toolkit installed successfully."
else
    echo "Skipping GPU driver installation."
fi

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    virtualenv .venv --python=python3
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install PyTorch with CUDA support (default: CUDA 11.8, change as needed)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install Ultralytics YOLOv8
pip install ultralytics

# Install other common dependencies
pip install boto3

# Test CUDA installation
echo "Testing GPU drivers and CUDA with PyTorch..."
python src/test_cuda.py
if [ $? -ne 0 ]; then
    echo "GPU test failed. Please check your GPU drivers and CUDA installation."
    exit 1
else
    echo "GPU test passed successfully."
fi

#they now need to set the configuration options in the config.py file!
echo "Configuration complete. Please edit the main.py file to set your configuration options."
echo "Do you understand that you need to edit the main.py file to set your configuration options? (y/n)"
read edit_config
if [ "$edit_config" == "y" ]; then
    echo "You can now edit the main.py file to set your configuration options."
else
    echo "You need to edit the main.py file to set your configuration options. Exiting."
    exit 1
fi