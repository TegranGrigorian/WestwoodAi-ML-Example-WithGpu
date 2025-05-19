#this will extract the data you downloaded from obtain_data.py
import config
import zipfile
from src.data_manager import S3DataHandler

DataHandler = S3DataHandler(config.bucket_name, config.region_name)

DataHandler.extract_zip(config.output_zip_file,extract_to=config.extracted_data_desired_directory)