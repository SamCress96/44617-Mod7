"""
    This program sends a message to 3 different queues on the RabbitMQ server.
    It gets messages by reading a csv file column by column. It sends a message every 30 seconds. 
   
    Author: Samantha Cress
    Based on code by Dr. Denise Case
    Date: February 13, 2023
    Updated: February 20, 2023
"""
import pika
import sys
import webbrowser
import csv
import time

# Defines host and queue names
host = 'localhost'
queueO = 'Outage'
queueR = 'Restore'


# Function offers rabbitmq pop up if set to true. 
def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website"""
    if show_offer == True:
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.
    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """
    try: 
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queueO, durable=True)
        ch.queue_declare(queue=queueR, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queueO, body=message)
        ch.basic_publish(exchange="", routing_key=queueR, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")

    except pika.exceptions.AMQPConnectionError as e:
            print(f"Error: Connection to RabbitMQ server failed: {e}")
            sys.exit(1)
    finally:
            # close the connection to the server
            conn.close()
   
def get_message_from_column(input_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        next(file)  # Skips over header when sending message   
        for row in reader:

            # use an fstring to create a message from our data, this will be for the timestamp. 
            fstring_message_reason = f"{row[0]}" #First row will be zero, do not put column here put row!!

            # Get Channel 1 column (smart_smoker) and send message
            outage_day = (row[1])
            outage_time = (row[2])
            fstring_message_out_all = f"{fstring_message_reason}, {outage_day}, {outage_time}" #Sends the timestamp from column followed by smart smoker temp. 
            outage_message = fstring_message_out_all.encode()
            send_message(host, queueO, outage_message)

            # use an fstring to create a message from our data, this will be for the timestamp. 
            fstring_message_reason = f"{row[0]}" #First row will be zero, do not put column here put row!!

            # Get Channel 1 column (smart_smoker) and send message
            restore_day = (row[3])
            restore_time = (row[4])
            restore_complete = (row[5])
            fstring_message_restore_all = f"{fstring_message_reason}, {restore_day}, {restore_time}, {restore_complete}" #Sends the timestamp from column followed by smart smoker temp. 
            restore_message = fstring_message_restore_all.encode()
            send_message(host, queueR, restore_message)

            # sleep for 30 seconds
            time.sleep(1)

def clear_queue(host: str, queue_name: str):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    # use the connection to create a communication channel
    ch = conn.channel()
    # delete the queue
    ch.queue_delete(queue=queueO)
    ch.queue_delete(queue=queueR)


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    offer_rabbitmq_admin_site(False)
    csv_file = 'outage.csv'
    get_message_from_column(csv_file)
