# Set up virtual environment
cd /home/ec2-user/app

# Debugging: List directory contents to verify file presence
echo "Listing contents of /home/ec2-user/app directory:"
ls -l /home/ec2-user/app

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found, creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found in /home/ec2-user/app"
    exit 1
fi

echo "Dependencies installed successfully!"