"""
Module that handles S3 operations like upload and delete objects
"""
import json

def get_objects(client, bucket_name, input_prefix):
    """
    Retrive all the objects found in the given bucket and prefixes
    """
    objects = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=input_prefix,
        StartAfter=input_prefix
    )
    return objects

def get_object_json(client, bucket_name, key):
    """
    Get the file from S3 and returns its JSON content
    """
    # Getting the object:
    print("Getting S3 object...")
    # Note how we're using the same ``KEY`` we
    # created earlier.
    response = client.get_object(Bucket=bucket_name, Key=key)
    print("Done")
    return json.loads(response['Body'].read().decode('utf-8'))

def copy_object(client, object_list, bucket_name, output_prefix):
    """
    Copy given object into the given prefix and return the keys of the copied objects
    """
    copied_keys = []
    for obj in object_list.get('Contents'):
        object_key = obj.get('Key')
        print('File to copy : {0}'.format(object_key))
        copy_result = client.copy_object(
            Bucket=bucket_name,
            CopySource=bucket_name + '/'+object_key,
            Key=output_prefix + object_key.split('/')[1]
        )
        print('file copied')
        print(copy_result.get('CopyObjectResult'))
        copied_keys.append(object_key)
    return copied_keys

def delete_objects(client, object_keys, bucket_name):
    """
    delete the objects referenced by the given keys and return errors if any
    """
    if object_keys and len(object_keys) > 0:
        key_to_be_deleted = [{'Key':i} for i in object_keys]
        del_resp = client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': key_to_be_deleted,}
        )
        print('files deleted')
        print('Erros found: {0}'.format(del_resp.get('Errors')))
        return del_resp.get('Errors')
    return None

def upload_file(client, file, bucket_name, output_prefix, file_name):
    """
    Upoad the file to s3
    """
    print('Uploading file to S3...')
    upload_result = client.upload_file(file, bucket_name, output_prefix + file_name)
    print(upload_result)
    print('Done...')
