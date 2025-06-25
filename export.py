import boto3
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
import traceback
from datetime import datetime

# ===== LOGGING SETUP =====
def setup_logging():
    """Setup comprehensive logging with timestamp"""
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as executable
        app_dir = Path(sys.executable).parent
        log_dir = app_dir / 'logs'
    else:
        # Running as script
        app_dir = Path(__file__).parent
        log_dir = app_dir / 'logs'
    
    # Create logs directory
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = f"s3_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = log_dir / log_filename
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"=" * 60)
    logger.info(f"S3 UPLOAD APPLICATION STARTED")
    logger.info(f"Log file: {log_filepath}")
    logger.info(f"Application directory: {app_dir}")
    logger.info(f"=" * 60)
    
    return logger

# Initialize logger
logger = setup_logging()

# ===== ENVIRONMENT LOADING =====
def load_environment():
    """Load environment variables with comprehensive logging"""
    try:
        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            app_dir = Path(sys.executable).parent
        else:
            app_dir = Path(__file__).parent
        
        env_path = app_dir / '.env'
        logger.info(f"Looking for .env file at: {env_path}")
        logger.info(f".env file exists: {env_path.exists()}")
        
        if env_path.exists():
            load_dotenv(env_path)
            logger.info("✅ .env file loaded successfully")
        else:
            logger.warning("⚠️ .env file not found, using system environment variables")
            load_dotenv()  # Load from system environment
        
        # Get environment variables
        screenshot_dir = os.path.expanduser(os.getenv("SCREENSHOT_DIR", "~/Desktop/screenshots"))
        output_dir = os.path.expanduser(os.getenv("OUTPUT_DIR", "~/Desktop/AllJsons"))
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "ap-south-1")
        s3_bucket = os.getenv("S3_BUCKET_NAME", "soubhikpos")
        
        logger.info(f"SCREENSHOT_DIR: {screenshot_dir}")
        logger.info(f"OUTPUT_DIR: {output_dir}")
        logger.info(f"AWS_ACCESS_KEY_ID loaded: {aws_access_key is not None}")
        logger.info(f"AWS_SECRET_ACCESS_KEY loaded: {aws_secret_key is not None}")
        logger.info(f"AWS_REGION: {aws_region}")
        logger.info(f"S3_BUCKET_NAME: {s3_bucket}")
        
        return screenshot_dir, output_dir, aws_access_key, aws_secret_key, aws_region, s3_bucket
        
    except Exception as e:
        logger.error(f"❌ Environment loading failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

# Load environment variables
SCREENSHOT_DIR, OUTPUT_DIR, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET = load_environment()

def initialize_s3_client():
    """Initialize and test S3 client connection"""
    logger.info("🔍 Initializing S3 client...")
    
    try:
        # Use environment variables or fallback to hardcoded values
        access_key = AWS_ACCESS_KEY 
        secret_key = AWS_SECRET_KEY 
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=AWS_REGION
        )
        
        # Test connection by listing buckets
        logger.info("Testing S3 connection...")
        response = s3_client.list_buckets()
        logger.info(f"✅ S3 connection successful. Available buckets: {len(response['Buckets'])}")
        
        # Check if target bucket exists
        bucket_exists = any(bucket['Name'] == S3_BUCKET for bucket in response['Buckets'])
        if bucket_exists:
            logger.info(f"✅ Target bucket '{S3_BUCKET}' found")
        else:
            logger.warning(f"⚠️ Target bucket '{S3_BUCKET}' not found in available buckets")
        
        return s3_client
        
    except Exception as e:
        logger.error(f"❌ S3 client initialization failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def upload_files_to_s3(source_directory, s3_folder='uploads/', file_extensions=None):
    """
    Upload files from source directory to S3
    
    Args:
        source_directory (str): Local directory path
        s3_folder (str): S3 destination folder
        file_extensions (set): Set of valid file extensions
    """
    if file_extensions is None:
        file_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.txt', '.json'}
    
    logger.info(f"🚀 Starting S3 upload process")
    logger.info(f"📁 Source directory: {source_directory}")
    logger.info(f"🪣 S3 bucket: {S3_BUCKET}")
    logger.info(f"📂 S3 folder: {s3_folder}")
    logger.info(f"📋 File extensions: {file_extensions}")
    
    # Initialize S3 client
    s3_client = initialize_s3_client()
    if not s3_client:
        logger.error("❌ Failed to initialize S3 client")
        return False
    
    # Check if source directory exists
    if not os.path.exists(source_directory):
        logger.error(f"❌ Source directory does not exist: {source_directory}")
        return False
    
    # Get list of files to upload
    files_to_upload = []
    try:
        for filename in os.listdir(source_directory):
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in file_extensions:
                files_to_upload.append(filename)
        
        logger.info(f"📊 Found {len(files_to_upload)} files to upload")
        
        if not files_to_upload:
            logger.warning("⚠️ No files found matching the specified extensions")
            return True
    
    except Exception as e:
        logger.error(f"❌ Failed to list files in directory: {e}")
        return False
    
    # Upload files
    successful_uploads = 0
    failed_uploads = 0
    
    for filename in files_to_upload:
        try:
            local_file_path = os.path.join(source_directory, filename)
            s3_key = os.path.join(s3_folder, filename).replace('\\', '/')
            
            logger.info(f"📤 Uploading: {filename}")
            
            # Get file size for logging
            file_size = os.path.getsize(local_file_path)
            logger.debug(f"File size: {file_size} bytes")
            
            # Upload file
            s3_client.upload_file(local_file_path, S3_BUCKET, s3_key)
            
            logger.info(f"✅ Successfully uploaded: {filename} → s3://{S3_BUCKET}/{s3_key}")
            successful_uploads += 1
            
        except Exception as e:
            logger.error(f"❌ Failed to upload {filename}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            failed_uploads += 1
    
    # Summary
    logger.info(f"=" * 60)
    logger.info(f"📊 UPLOAD SUMMARY")
    logger.info(f"✅ Successful uploads: {successful_uploads}")
    logger.info(f"❌ Failed uploads: {failed_uploads}")
    logger.info(f"📁 Total files processed: {len(files_to_upload)}")
    logger.info(f"=" * 60)
    
    return failed_uploads == 0

def upload_screenshots():
    """Upload screenshots from SCREENSHOT_DIR"""
    logger.info("📸 Starting screenshot upload...")
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    return upload_files_to_s3(SCREENSHOT_DIR, 'screenshots/', image_extensions)

def upload_outputs():
    """Upload output files from OUTPUT_DIR"""
    logger.info("📄 Starting output files upload...")
    output_extensions = {'.txt', '.json', '.csv', '.xlsx'}
    return upload_files_to_s3(OUTPUT_DIR, 'outputs/', output_extensions)

def upload_all_directories():
    """Upload files from all configured directories"""
    logger.info("🚀 Starting upload of all directories...")
    
    results = []
    
    # Upload screenshots
    logger.info("=" * 40)
    screenshot_result = upload_screenshots()
    results.append(('Screenshots', screenshot_result))
    
    # Upload outputs
    logger.info("=" * 40)
    output_result = upload_outputs()
    results.append(('Outputs', output_result))
    
    # Final summary
    logger.info("=" * 60)
    logger.info("🏁 FINAL UPLOAD SUMMARY")
    for directory_type, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"{directory_type}: {status}")
    logger.info("=" * 60)
    
    return all(result[1] for result in results)

#