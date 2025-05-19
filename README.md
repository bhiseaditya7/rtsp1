# rtsp1

## Features
- User authentication 
- Real-Time Streaming Protocol application
- tested using Larix Broadcaster


## Technologies Used
- Django (REST Framework)
- PostgreSQL (Database) or sqlite
- Redis (Caching)
- Django CORS Headers 
- React on frontend
- AWS EC2 instance for docker and redis 

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/bhiseaditya7/rtsp1.git
    cd rtsp1
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv ccenv
    source ccenv/bin/activate  # On Windows: ccenv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt    
    ``
      ```
4. **Run database migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    daphne project_stream.asgi:application 
    ```

## API Endpoints (will be made available via Postman)

- `POST /api/register/` - Register a new user
- `POST /api/signin/` - User login and JWT token generation

## Already registered credentials (for testing)
 username : Aditya21
 password : btwin20019

## Contributing
Contributions are welcome! Please follow the standard Git workflow:

1. Fork the repository
2. Create a new feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request
