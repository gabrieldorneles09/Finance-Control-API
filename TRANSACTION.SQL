CREATE TABLE TRANSACTION(
    transaction_id VARCHAR(255) PRIMARY KEY,
    transaction_receiver_id VARCHAR(255),
    payment_form VARCHAR(255),
    entry_type VARCHAR(255),
    category VARCHAR(255),
    description VARCHAR(255),
    value FLOAT,
    charge_date VARCHAR(255),
    payment_date VARCHAR(255),
    recurrent BOOLEAN,
    recurrence_type VARCHAR(255),
    insert_date VARCHAR(255)
)