# ALX Travel App 0x03

### Celery + RabbitMQ + Email Notifications Setup

#### Steps to Run the Project

1. **Start RabbitMQ Server**
   ```bash
   sudo systemctl start rabbitmq-server
Start Celery Worker

bash
Copy code
celery -A alx_travel_app worker -l info
Start Django Development Server

bash
Copy code
python manage.py runserver
Trigger Background Email Task

Create a new booking via API or admin panel.

Celery will handle email sending asynchronously.

Configuration Summary
Broker: RabbitMQ (amqp://localhost)

Backend: RPC

Email Backend: Console (can be changed to SMTP)

Task File: listings/tasks.py

Trigger Point: BookingViewSet.perform_create
