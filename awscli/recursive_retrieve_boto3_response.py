"""
    Recursive retrieve all the responses until NextToken not present in the n last response
"""
def recursive_response(boto_method, key, response=None, all_res=[], **kwargs):
    """
    (method)
    boto_method : function
        boto3 function from a specific client
    response : dict, not required
        Response from boto3 client request (default is None)
    all_res : list, not required
        List of all responses from boto3 client request (default is [])
    key : filter key for boto3 client request
    kwargs  : nested keywords for boto3 client request
    """
    if response == None:
        pass
    elif 'NextToken' not in response:
        return all_res
    else:
        kwargs.update({'NextToken': response['NextToken']})
    
    if kwargs != {}:
        response = boto_method(**kwargs)
    else:
        response = boto_method()

    all_res.extend(response[key])

    return recursive_response(boto_method, key, response, all_res, **kwargs)

# Example of usage
def run():
    import boto3
    import os
    os.environ['AWS_PROFILE'] = "main-admin"
    os.environ['AWS_REGION'] = "us-east-1"
    
    client = boto3.client('ssm')
    
    res = recursive_response(client.get_parameters_by_path, key='Parameters', Path='/qa', Recursive=True, WithDecryption=True)
    print(res)



if __name__ == "__main__":
    run()