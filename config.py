#this file contains the confidugation that needs to be done

#file pathing + data handling configuration
bucket_name = "train-object-detector-ec2-bucket"
region_name = "useast-2" #im on an airplane so I dont know for sure if this is correct. please check
data_in_path = "in/roofsegment.zip" #path relative to S3 bucket
output_zip_file = "data.zip" #you wont need to change this
extracted_data_desired_directory = "./"
S3_results_zip = "roofsegment-results.zip"

#SNS (tells us if the model is finsihed) Configuration - optional
sns_topic_arn = "arn:aws:sns:us-east-2:354918395782:train-object-detector-ec2-sns:cc28e55d-bfd4-43d4-871d-2aa293ef3f58"
sns_message = "Done!"

#ML-AI Configuration
model_path = "yolov8n.pt" #medium model weights
yaml_file = "data.yaml" #check this with your file from obtained data
epochs = 100 # change this to what you want, the default is 100
result_zip_path = "./runs.zip" #I wouldnt recomend changing this unless your model outputs a different result dir