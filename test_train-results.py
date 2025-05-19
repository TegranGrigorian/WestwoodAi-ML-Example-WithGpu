#the title sucks but this code will test if the training works as well as the zipping and extaction of the results to a zip onto a S3

import ultralytics
import config
from src.train_yolo import YOLOTrainer
from src.data_manager import S3DataHandler
import os

trainer = YOLOTrainer(config.model_path, 
                      config.yaml_file, 
                      1, #only 1 epoch for test 
                      config.bucket_name
                      )

trainer.train_model(sns_topic_arn=config.sns_topic_arn, device=0) #use gpu
trainer.zip_results(runs_dir='./runs', zip_path=config.result_zip_path)
trainer.upload_results(zip_path=config.result_zip_path,s3_key=config.S3_results_zip)