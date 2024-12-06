#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to stream users from the database in batches
    """
    # Establish database connection
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',  # Replace with your MySQL username
        password='your_password',  # Replace with your MySQL password
        database='ALX_prodev'
    )
    
    # Create cursor
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        batch = []
        for row in cursor:
            batch.append(row)
            
            # Yield batch when it reaches specified size
            if len(batch) == batch_size:
                yield batch
                batch = []
        
        # Yield remaining rows if batch is not empty
        if batch:
            yield batch
    
    finally:
        # Ensure cursor and connection are closed
        cursor.close()
        connection.close()

def batch_processing(batch_size=50):
    """
    Process users in batches, filtering users over 25 years old
    """
    # Iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Process and filter each batch
        for user in batch:
            if user['age'] > 25:
                print(user)