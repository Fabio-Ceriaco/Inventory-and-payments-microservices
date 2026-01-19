# Inventory-and-payments-microservices

This project demonstrates a microservices architecture using FastAPI for backend REST APIs and Angular for the frontend interface. It consists of two primary microservices: Product Inventory and Payments, which communicate via HTTP requests to simulate real-world transactions. The project leverages Redis as the system database for each microservice to manage data and facilitate real-time status updates using HTTP streaming.

# Key Features:

  - Microservices Communication: Inventory and Payments services interact seamlessly via HTTP requests, enabling simulation of payment processing and stock management.

  - Real-Time Updates: Status notifications between microservices are delivered using HTTP streaming, supported by separate Redis databases for each service.

  - Frontend Interface: Built with Angular, providing a responsive and interactive user experience.

  - Modern Styling: Utilizes HTML and Tailwind CSS for streamlined UI design.

# Technology Stack:

  - Frontend: Angular, HTML, Tailwind CSS, JavaScript

  - Backend: FastAPI (Python)

  - Database / Caching: Redis (separate instances for Inventory and Payments)

# Highlights:

  - Experimented with microservices orchestration and inter-service communication.

  - Implemented Redis-backed streaming for real-time transaction updates.

  - Full-stack integration from frontend Angular application to backend FastAPI services.
