import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('PizzaMenu')

print "Loading functions.."

def lambda_handler(event,context):
    method = event['method']
    response = None
    if(method == "POST"):
        response = postPizzaMenu(event,context)
    elif(method == "GET"):
        response = getPizzaMenu(event,context)
    elif(method == "DELETE"):
        response = delPizzaMenu(event,context)
    elif(method == "PUT"):
        response = putPizzaMenu(event,context)

    return response
    
def postPizzaMenu(event,context):    
    store_name = event['body']['store_name']
    selection = event['body']['selection']
    size = event['body']['size']
    price = event['body']['price']
    store_hours = event['body']['store_hours']
    item = {
        'menu_id': str(uuid.uuid1()),
        'store_name': store_name,
        'selection': selection,
        'size': size,
        'sequence': ["selection","size"],
        'price': price,
        'store_hours' : store_hours
    }
    # write the menu items to the database
    table.put_item(Item=item)

    # create a response
    response = "200 OK"
    return response
     
def getPizzaMenu(event,context):
    menu_id = event['params']['menu-id']
    result = table.get_item(
        Key= {
            'menu_id': menu_id
        }
    )
    item = result['Item']
    return item
    
def putPizzaMenu(event,context): 
    
    # write the menu items to the database
    result = table.update_item(
        Key= {
            'menu_id': event['params']['menu-id']
        },UpdateExpression="set selection = :val",
    ExpressionAttributeValues={
        ':val': event['body']['selection']
    },
    ReturnValues="UPDATED_NEW"
    )

    # create a response
    response = "200 OK"
    return response
    
def delPizzaMenu(event,context):
    
    menu_id = event['params']['menu-id']
    result = table.delete_item(
        Key= {
            'menu_id': menu_id
        }
    )
    # create a response
    response = "200 OK"

    return response