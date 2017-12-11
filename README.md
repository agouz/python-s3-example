# python-s3-example
A python app that reads a json file from a bucket and writes it as a csv to another bucket. Genius eh?

## Environment variables
Env Var  | Description | Default
------------- | ------------- | -------------
AWS_ACCESS_KEY_ID | AWS access key id to access the S3 bucket | none
AWS_SECRET_ACCESS_KEY | AWS access secret to access the S3 bucket | none

## Configuration parameters
All configuration paramteres are found in the `app_config.py` file

Config | Description | Default
------------- | ------------- | -------------
bucket_name | The name of the bucket to read and write to and from | 
input_folder_name | the name of the folder (key) that holds the input files | 'batman/'
output_folder_name | the name of the output folder to write the csv file to | 'superman/'
poll_frequency | How long should the app waits between each poll, i.e: checking for new files | 3.0

# Pre-requisite to running it locally (first time only)
pip virtualenv
virtualenv venv

# Install dependecies
source venv/bin/activate
pip install -r requirements.txt

## to run locally
# Run the following only once
source venv/bin/activate


# to run the app
First upload a sample json file in the configured input bukcet location and after running the app check that a new csv file is created in the configured target bucket location.

1- Configure the application with the correct bitbucket folders for input and output in app_config.py
2- Upload a new sample file to the input folder using the following command (rememebr to udate the command with your input folder name), examine the content of the sample file found in the samples folder
`aws s3 cp ./samples/sample.json s3://<bucket-name>/<input-folder>/sample.json`

3- Make sure that the file has been uplaoded and that the output folder is empty
`aws s3 ls <bucket-name>/<folder> --recursive`

4- Run the app using the following command
`python app.py`

5- Check that the sample file has been deleted from the input folder and a new file is created in the output folder using the same command in step-3

6- Download the generated file and examine its content
`aws s3 cp s3://<bucket-name>/<output-folder>/sample.csv ./samples/sample.csv`
