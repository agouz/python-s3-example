"""
This module checks a S3 bucket for new files and reads them then writes them back to another bucket
"""
import os
import time
import boto3
import app_config as cfg
import s3.handler as s3
import utils.handler as utils


BUCKET_NAME = cfg.bucket_name
INPUT_PREFIX = cfg.input_folder_name
OUTPUT_PREFIX = cfg.output_folder_name
TMP_FOLDER = cfg.temp_dir
WAIT_TIME = cfg.poll_frequency

# set aws creds
os.environ['AWS_REGION'] = 'ap-southeast-2'


def main():
    """
    The main function that reads all files that exists in the configured bucket
    then convert them from json to csv
    upload the converted file to the configured location and then delete the json file
    """
    while 1 == 1:
        print('New poll started ...')
        # s3 client
        s3_client = boto3.client('s3')
        try:
            # get the list of files available in the configure bitbucket/key
            s3_objects = s3.get_objects(s3_client, BUCKET_NAME, INPUT_PREFIX)
            # if files exists then copy them to the configured location then delete them
            if s3_objects.get('Contents'):
                copied_object_keys = []
                # get all the objects found in the bucket
                for temp_obj in s3_objects.get('Contents'):
                    object_key = temp_obj.get('Key')
                    file_name_with_no_extension = object_key.split('/')[1].split('.')[0]
                    print('Reading file: {0}'.format(object_key))
                    # Now get the file content in json format
                    file_content = s3.get_object_json(s3_client, BUCKET_NAME, object_key)
                    # Convert it into csv
                    csv_data_file_name = utils.convert_json_to_csv(file_content, TMP_FOLDER, file_name_with_no_extension) # batman/fileName.json
                    # upload the converted file to S3
                    s3.upload_file(s3_client, csv_data_file_name, BUCKET_NAME, OUTPUT_PREFIX,'{}.csv'.format(file_name_with_no_extension) )
                    # keep track of what we've to delete it afterwards
                    copied_object_keys.append(object_key)
                s3.delete_objects(s3_client, copied_object_keys, BUCKET_NAME)
                print('Emptying the tmp folder')
                utils.empty_tmp_folder(TMP_FOLDER)
            else:
                print('No new files found...')
        except Exception as error:
            print('run-time error:', error)
        else:
            print('Processing finished, waiting for next poll...')
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()
