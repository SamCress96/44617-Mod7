# Module 7 Custom Project
# Steps taken to create outage producer
1. Define a function to clear queues when file has been run previously. 
2. Define a function to only show rabbitmq pop up when set to true. 
3. Set host and set queue names. 2 queues are needed for outage prodcer to work. 
4. Define a function to create and send a message to the appropriate queue each execution. 
5. Create connection and channel within the rabbitmq server, also declare queue name and create durable queue. 
6. Define function to read from outage CSV and create message.
7. Use fstrings to create message from the data, first fstring pulls the outage cause from column one. 
8. Create 2 seperate messages, the first sends a message with outage reason, outage day, and outage time. Second message sends information about outage restore.
9. Set the producer to sleep for 1 second. 
10. Use the python idiom to call appropriate functions. 
# Steps taken for outage consumers
1. Create two different consumers that will each read from two different queues.
2. Consumer one will recieve messages from the outage queue. 
3. Messages will consist of outage infromation
4. Depending on outage reaons the consumer will identify how long it should take for power to be restored. 
5. To create second consumer:
7. Create a callback function like the one created for the outage consumer
8. Set perameters for identifying if power was restored in time.
9. Consumer 2 will identify if power has been restored in time. 