import json
import uuid
import boto3
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('PizzaMenu')

print "Loading functions.."

def handler(event, context):
    #print context.httpMethod
    #if(context.httpMethod == 'GET'):
        response = create(event,context);
        return response


def create(event,context):
   # data = json.loads(event['body'])

    store_name = event.get('store_name')
    Selection = event.get('selection')
    size = event.get('size')
    price = event.get('price')
    store_hours = event.get('store_hours')

    item = {
        'menu_id': str(uuid.uuid1()),
        'selection': Selection,
        'size': size,
        'price': price,
        'store_hours' : store_hours
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

def get(event, context):

    menu_id = event.get('id')
    #pathParameters = event.get(pathParameters)
    # fetch todo from the database
    result = table.get_item(
        Key={
            'menu_id': menu_id
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], indent=4,
                           cls=DecimalEncoder)
    }

    return response
