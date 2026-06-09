import os
import json
import boto3
from ..models.user import User
from dotenv import load_dotenv
from ..utilities import validate_model

import logging
logging.basicConfig(level=logging.INFO)


load_dotenv()

def process_message(message):
    sns_envelope = json.loads(message.body)
    event = json.loads(sns_envelope["Message"])

    if event["event_type"] == "order.placed":
        order = event["payload"]

        print("=== ORDER CONFIRMATION ===")
        print(f"User ID: {order['user_id']}")
        print(f"Order ID: {order['id']}")

        for item in order["items"]:
            print(f"- {item['product_name']} x {item['quantity']}")

    return True

def poll(wait_time=20):
    while True:
        sqs = boto3.resource('sqs')
        queue = sqs.Queue(os.environ["QUEUE_URL"])

        print("Polling For Messages...")

        messages = queue.receive_messages(
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,
            WaitTimeSeconds=wait_time
        )

        for message in messages:
            try:
              print(f"Processing Message: {message.message_id}")
              is_processed = process_message(message)

              if is_processed:
                  message.delete()
                  print(f"Message {message.message_id} PROCESSED!")
                  continue
            except Exception as e:
                print(f"Message {message.message_id} NOT PROCESSED!")

if __name__ == "__main__":
  from .. import create_app
  app = create_app()

  with app.app_context():
    poll(wait_time=20)