# XPERT AD-TARGETING

Automated POS monitoring and OCR processing application.

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install xpert-ad-targeting
```

### Option 2: Install in Development Mode

```bash
# Clone the repository
git clone <repository-url>
cd Project_Xpert

# Install the package in development mode
python install.py

# Or manually:
pip install -e .
```

## Configuration

**Important**: The package does not include any `.env` files for security reasons. You must create your own configuration file.

### Setting up Environment Variables

#### Method 1: Using the Setup Script (Recommended)

After installation, run the setup script to create your `.env` file:

```bash
python setup_env.py
```

This will:
- Copy `env.example` to `.env`
- Guide you through the configuration process
- Provide security reminders

#### Method 2: Manual Setup

1. **Copy the example configuration:**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file** with your actual credentials:
   ```env
   # AWS Configuration
   AWS_ACCESS_KEY_ID=your_actual_access_key
   AWS_SECRET_ACCESS_KEY=your_actual_secret_key
   AWS_REGION=ap-south-1
   S3_BUCKET_NAME=your_actual_bucket_name

   # MongoDB Configuration
   MONGO_URI=mongodb://localhost:27017/xpert_db
   # For production MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/xpert_db

   # Application Settings
   SSIM_THRESHOLD=0.85
   CLEANUP_HOURS=24
   OUTPUT_DIR=/app/AllJsons
   UPLOAD_INTERVAL_MINUTES=5

   # Tesseract Configuration (automatically detected when installed via pip)
   TESSERACT_PATH=/usr/bin/tesseract

   # Logo Path (optional)
   LOGO_PATH=./xpert_ad_targeting_logo.jpeg

   # Development Settings (optional)
   DEBUG=0
   PYTHONPATH=/app
   ```

3. **Security Notes:**
   - Never commit your `.env` file to version control
   - Keep your AWS credentials and MongoDB connection strings secure
   - The `.env` file is automatically excluded from the published package

## Usage

After installation and configuration, you can run the application in several ways:

### 1. Command Line (Recommended)

```bash
xpert-ad-targeting
```

### 2. Python Module

```bash
python -m Project_Xpert
```

### 3. Direct Python Execution

```bash
python -c "from Project_Xpert import run; run()"
```

### 4. From Your Code

```python
from Project_Xpert import XpertPOSApp

# Create and run the application
app = XpertPOSApp()
app.window.mainloop()
```

## Features

- **POS Monitoring**: Automated monitoring of POS windows
- **OCR Processing**: Text extraction from screenshots using Tesseract (included)
- **S3 Upload**: Automatic file upload to AWS S3
- **GUI Interface**: Modern GUI built with CustomTkinter
- **Background Processing**: Non-intrusive background monitoring
- **Phone Number Detection**: Automatic phone number capture

## Requirements

- Python 3.8 or higher
- Tesseract OCR (automatically included in the package)
- Required Python packages (automatically installed):
  - customtkinter
  - Pillow
  - pytesseract
  - opencv-python
  - pymongo
  - boto3
  - python-dotenv
  - keyboard
  - pyautogui
  - pygetwindow
  - requests
  - numpy
  - scikit-image
  - scipy

## Development

### Project Structure

```
Project_Xpert/
├── __init__.py          # Package initialization
├── __main__.py          # Module entry point
├── main.py              # Main application
├── capture.py           # Screen capture functionality
├── ocr_export.py        # OCR processing
├── cleanup.py           # File cleanup
├── autorun.py           # Startup management
├── setup.py             # Package setup
├── pyproject.toml       # Modern package configuration
├── MANIFEST.in          # Package manifest
├── install.py           # Installation script
├── setup_env.py         # Environment setup helper
├── requirements.txt     # Dependencies
├── env.example          # Example environment configuration
├── .gitignore           # Git ignore rules
└── Tesseract-OCR/       # OCR engine (included)
```

### Building the Package

```bash
# Build the package
python -m build

# Install from built package
pip install dist/xpert-ad-targeting-1.0.0.tar.gz
```

## Security

- **Environment Files**: `.env` files are excluded from the package to protect sensitive information
- **Credentials**: Always use environment variables for API keys and database connections
- **Example Configuration**: Use `env.example` as a template for your configuration
- **Setup Script**: Use `setup_env.py` for guided environment configuration

## Support

For support, contact: support@xpert.chat

## License

MIT License 