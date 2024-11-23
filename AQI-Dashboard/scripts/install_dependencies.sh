#!/bin/bash
# install_dependencies.sh

# Update and install pip and virtualenv if needed
echo "Updating system and installing dependencies..."
sudo yum update -y
sudo yum install -y python3-pip python3
sudo yum install -y nc

# Ensure virtualenv is installed
pip3 install --upgrade virtualenv

# Check Python version
echo "Python version: $(python3 --version)"
