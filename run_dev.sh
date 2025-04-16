#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up development environment...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Backend setup
echo -e "${BLUE}📦 Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "fastapienv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv fastapienv
fi

# Activate virtual environment
source fastapienv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create or clear the log file
echo "Initializing backend.log..."
echo "Backend server started at $(date)" > backend.log

# Start backend server in the background with logging
echo -e "${GREEN}Starting backend server...${NC}"
uvicorn main:app --reload --port 8000 >> backend.log 2>&1 &
BACKEND_PID=$!

# Display backend URL prominently
echo -e "\n${YELLOW}🔗 Backend API is running at: http://127.0.0.1:8000${NC}"
echo -e "${YELLOW}📝 API Documentation: http://127.0.0.1:8000/docs${NC}\n"

# Return to root directory
cd ..

# Frontend setup
echo -e "${BLUE}📦 Setting up frontend...${NC}"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Start frontend development server
echo -e "${GREEN}Starting frontend development server...${NC}"
npm run dev

# Cleanup function
cleanup() {
    echo -e "${BLUE}Cleaning up...${NC}"
    kill $BACKEND_PID
    deactivate
    exit 0
}

# Set up trap to catch script termination
trap cleanup SIGINT SIGTERM

# Keep script running
wait 