import logging
import os
from src.data_manager import S3DataHandler
from src.train_yolo import YOLOTrainer
from src.sns import sns
from src.ec2_shutdown import Ec2Shutdown

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

    bucket_name = os.getenv('S3_BUCKET_NAME', 'train-object-detector-ec2-bucket')
    data_in_path = os.getenv('S3_DATA_IN_PATH', "in/roofsegment.zip")
    output_zip_file = 'data.zip'
    extracted_data_dir = './'
    model_path = "yolov8n.pt"
    yaml_file = "data.yaml"
    epochs = 100
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-2:354918395782:train-object-detector-ec2-sns:cc28e55d-bfd4-43d4-871d-2aa293ef3f58')
    sns_message = "Training completed for YOLO model."
    results_zip_path = './runs.zip'
    s3_results_key = 'roofsegment-results.zip'

    # Initialize handlers
    data_handler = S3DataHandler(bucket_name)
    trainer = YOLOTrainer(model_path, yaml_file, epochs, bucket_name)
    sns_instance = sns()
    ec2_shutdown = Ec2Shutdown()

    try:
        logging.info("Step 1: Downloading data from S3...")
        data_handler.download_file(data_in_path, output_zip_file)

        logging.info("Step 2: Extracting data...")
        data_handler.extract_zip(output_zip_file, extract_to=extracted_data_dir)

        logging.info("Step 3: Checking CUDA availability...")
        import torch
        if not torch.cuda.is_available():
            logging.error("CUDA GPU is not available. Exiting.")
            return
        else:
            logging.info(f"CUDA is available. Device count: {torch.cuda.device_count()}")

        logging.info("Step 4: Starting YOLO training...")
        trainer.train_model(sns_topic_arn=sns_topic_arn, device=0)

        logging.info("Step 5: Zipping training results...")
        trainer.zip_results(runs_dir='./runs', zip_path=results_zip_path)

        logging.info("Step 6: Uploading results to S3...")
        trainer.upload_results(zip_path=results_zip_path, s3_key=s3_results_key)

        logging.info("Step 7: Sending SNS notification...")
        sns_instance.send_sns(topic_arn=sns_topic_arn, message=sns_message)

        logging.info("Step 8: Shutting down EC2 instance...")
        logging.info("Process completed successfully, and EC2 instance is shutting down.")
        ec2_shutdown.shutdown()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    configure_logging()
    main()
