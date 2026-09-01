# Messages architecture (v0)

![Current architecture for messages](docs/message%20rest.png)

## Signal Desk
Signal desk responsabilities will be :
- User web interface. Angular frontend
- Should have a button called messages. On clicking button should ask open an interface with an input asking which message user wants to send.
- Only communicates with HTTPs to Message Service
- Transient data. Will not communicate directly with Postgres database to avoid leaking credentials and other exploits that could hit database directly with any amount of messages and no control over traffic.


## Message Service
- Exposes REST API to handle simple messages only one attribute POST /messages
- Should persist any message sent to database
- Should be able to retrieve a list of previous sent messages and return GET /messages
- Persistance should be done using Postgres