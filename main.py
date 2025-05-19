import logging
import os
from src.data_manager import S3DataHandler
from src.train_yolo import YOLOTrainer
from src.sns import sns
from src.ec2_shutdown import Ec2Shutdown
import config

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("main.log"),
            logging.StreamHandler()
        ]
    )

def main():
    # Configuration - edit these as needed
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Set CWD to script location


    # Initialize handlers
    data_handler = S3DataHandler(config.bucket_name)
    trainer = YOLOTrainer(config.model_path, 
                          config.yaml_file, 
                          config.epochs, 
                          config.bucket_name)
    #sns_instance = sns()
    ec2_shutdown = Ec2Shutdown()

    try:
        logging.info("Step 1: Downloading data from S3...")
        data_handler.download_file(config.data_in_path, config.output_zip_file)

        logging.info("Step 2: Extracting data...")
        data_handler.extract_zip(config.output_zip_file, extract_to=config.extracted_data_desired_directory)

        logging.info("Step 3: Checking CUDA availability...")
        import torch
        if not torch.cuda.is_available():
            logging.error("CUDA GPU is not available. Exiting.")
            return
        else:
            logging.info(f"CUDA is available. Device count: {torch.cuda.device_count()}")

        logging.info("Step 4: Starting YOLO training...")
        trainer.train_model(sns_topic_arn=config.sns_topic_arn, device=0)

        logging.info("Step 5: Zipping training results...")
        trainer.zip_results(runs_dir='./runs', zip_path=config.result_zip_path)

        logging.info("Step 6: Uploading results to S3...")
        trainer.upload_results(zip_path=config.result_zip_path, s3_key=config.S3_results_zip)

        logging.info("Step 7: Sending SNS notification...")
        #sns_instance.send_sns(topic_arn=sns_topic_arn, message=sns_message)

        logging.info("Step 8: Shutting down EC2 instance...")
        logging.info("Process completed successfully, and EC2 instance is shutting down.")
        ##ec2_shutdown.shutdown()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    configure_logging()
    main()
