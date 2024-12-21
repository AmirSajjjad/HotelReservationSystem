# Hotel Booking System

## Overview
Welcome to the Hotel Reservation System project! This application aims to streamline the process of hotel reservations.

## Features
  - **User Management**: Handle user registration, login, and profile management.
  - **Room Inventory**: Track and manage room availability and details.
  - **Booking Management**: Process room bookings and manage reservations.

## Services:

- ### User Service
  - **Description:**
    - The User Service manages user accounts and authentication. It provides endpoints for user registration, login, and profile management.

  - **Technologies:**
    - **Framework:** Django
    - **Database:** PostgreSQL
 
  - **Endpoints:**
    - `/user_service/api/v1/auth/check_phone`: send OTP message to phone number
    - `/user_service/api/v1/auth/check_phone/verify`: validate OTP code then return access_token and refresh_token. [register phone number if user not exists]. 
    - `/user_service/api/v1/auth/refresh_token`: refresh access_token
    - `/user_service/api/v1/user/`: read and update user profile
    - `/user_service/admin`: django admin panel
    - `/user_service/swagger`: swagger documentation (only in debug mode)
    - `/user_service/redoc`: redoc documentation (only in debug mode)
  - **Running Tests:**
      To ensure the correctness of the code, you can run the tests:
    ```sh
    py manage.py test
    ```
      
- ### Hotel Service (Comming Soon)
  - **Description:**
    - The Hotel Service manages hotel information, including details about rooms and availability. It provides endpoints for adding new hotels, updating hotel information, and retrieving details about available rooms.

  - **Technologies:**
    - **Framework:** FastAPI
    - **Database:** MongoDB

  - **Endpoints:**
    <!-- - `/hotels`: Retrieve a list of hotels
    - `/hotels/{hotel_id}`: Retrieve details of a specific hotel
    - `/rooms`: Retrieve available rooms
    - `/rooms/{room_id}`: Retrieve details of a specific room -->
  - **ToDo Check List:**
    - [ ] Learning FastAPI (in progress)

- ### Booking Service (Comming Soon)
  - **Description:**
    - The Booking Service handles room bookings. It checks room availability, creates new bookings, and manages booking statuses (confirmed, cancelled, etc.).

  - **Technologies:**
    <!-- - **Framework:** Go (Gin)
    - **Database:** MySQL -->


  - **Endpoints:**
    <!-- - `/bookings`: Create a new booking
    - `/bookings/{booking_id}`: Retrieve details of a specific booking
    - `/bookings/user/{user_id}`: Retrieve all bookings for a specific user -->

## Getting Started
To get started with this project, you will need to:

1. Clone the repository:
   ```sh
   git clone https://github.com/AmirSajjjad/hotel-reservation-system.git
   ```
2. Navigate to the project directory:
    ```sh
    cd hotel-booking-system
    ```
3. set envirements:
   rename .env.sample to .env and edit this file
   ```sh
    mv .env.sample .enc
    nano .env
   ```
4. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```
5. Once the containers are up and running, you can access the services:
   - User Service (Django): http://localhost:8001
   - Booking Service (FastAPI): http://localhost:8002
   - Room Inventory Service (Go): http://localhost:8003
6. To stop the containers, use:
    ```sh
    docker-compose down
    ```

## Contributing
We welcome contributions to improve the project. Please fork the repository and submit pull requests for any enhancements or bug fixes.

## Contact

If you have any questions, suggestions, or comments about this project, please feel free to reach out to us at [this link](https://t.me/AmirSajjjad73). We usually respond within 24 hours.

You can also contact us via email at amirsajjjad2@gmail.com.

<!---
## Architecture
The system uses a microservice architecture where each service operates independently and communicates with other services through RESTful APIs. Message brokers like RabbitMQ or Kafka are used to handle asynchronous communication between services.


## Overview
Welcome to the Hotel Reservation System project! This application aims to streamline the process of hotel reservations by offering an efficient and user-friendly interface for customers and administrators alike. Leveraging a combination of SQL and NoSQL databases, the system ensures robust performance, scalability, and reliability.

---

## Services, Technologies, and Frameworks

### Payment Processing
- **Function**: Processes payments securely and ensures transaction integrity.
- **Technology**: Microsoft SQL Server
- **Language**: C#
- **Framework**: .NET Core
  - **Reason**: .NET Core ensures reliable transaction handling and security for payment data.

### Activity Logs
- **Function**: Maintains logs of all activities for auditing and analytics purposes.
- **Technology**: ElasticSearch
- **Language**: Python
- **Framework**: Flask
  - **Reason**: Flask is lightweight and efficient for implementing logging and search functionalities with ElasticSearch.


---

## Features
- **Reservation Management**: Handles bookings and availability in real-time.
- **Customer Information**: Stores and manages detailed customer profiles.
- **Room Inventory**: Tracks room availability and details dynamically.
- **Payment Processing**: Secures transactions and processes payments seamlessly.
- **Activity Logs**: Maintains comprehensive logs of all activities for auditing and analytics.

---

## Database Technologies
- **PostgreSQL**: Used for managing structured reservation data.
- **MongoDB**: Stores customer information with flexibility in schema.
- **Cassandra**: Manages room inventory data, optimized for high availability.
- **Microsoft SQL Server**: Ensures secure and reliable payment processing.
- **ElasticSearch**: Utilized for storing and searching through activity logs efficiently.

-->
