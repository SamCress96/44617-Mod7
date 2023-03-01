"""
    This program receives messages from the outage queue the RabbitMQ server.
    The program identifies how much time there is for power to be restored based on outage reason.   
   
    Author: Samantha Cress
    Based on code by Dr. Denise Case
    Date: Febuary 28, 2023
"""
#Needed modules
import pika
import sys
import time

#Define constants
host = "localhost"
csv_file = "outage.csv"
queueO = "Outage"


#Define function on getting message from outage queue and creating alert. 
def outage_callback(ch, method, properties, body):
    # receive & decode the binary message body to a string
    print(f" [x] Received {body.decode()}: Outage_Alert")
    # simulate work
    time.sleep(1)
    #declare variable to place the body data
    bodydata = body.decode()
    outage_message1 = bodydata
    # split message, so outage reason can be indentifed seperately
    outage_message1_split = outage_message1.split(", ")
    outage1_message1 = (outage_message1_split[0])
    #declare list variable for data to be transformed from bodydata
    """ Define behavior on getting a message."""
    if queueO == 'Outage':
        if outage1_message1 == 'Severe Weather - Thunderstorms':
            print('1 Hour to Restore: Emergency Response')
        elif outage1_message1 == 'Physical Attack':
            print('.5 Hours to Restore')
        elif outage1_message1 == 'Electrical System Separation (Islanding)':
            print('.5 Hours to Restore')
        elif outage1_message1 == 'Vandalism':
            print('1 Hours to Restore')
        elif outage1_message1 == 'Severe Weather':
            print('1 Hour to Restore: Emergency Response')
        else:
            print('8 Hours to Restore: Normal Response')

def main(host: str, queue1: str):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={host}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        # need one channel per consumer
        channel = connection.channel()
      

        # use the channel to declare a durable queue (1 per queue)
        # a durable queue will survive a RabbitMQ server restart and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=queueO, durable=True)
        

        # The QoS level controls the # of messages that can be in-flight (unacknowledged by the consumer) at any given time.
        # Set the prefetch count to one to limit the number of messages being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 
        

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # we use the auto_ack for this assignment
        channel.basic_consume(queue=queueO, on_message_callback=outage_callback, auto_ack=True)
       


        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()

########################################################

# Run program

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main(host, queueO)
