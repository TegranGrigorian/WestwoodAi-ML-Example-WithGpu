#imports
import config
from src.data_manager import S3DataHandler

if __name__ == "__main__":
    DataHandler = S3DataHandler(config.bucket_name, config.region_name)
    DataHandler.download_file(config.data_in_path, config.output_zip)
    pass