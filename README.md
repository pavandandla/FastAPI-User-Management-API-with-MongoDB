
# **FastAPI User Management API with MongoDB**

## **Description**

This project implements a **RESTful API** using **FastAPI** and **MongoDB** to provide **User Management** functionalities. The API supports **CRUD operations** on user data, secured with **JWT authentication** and **role-based access control (RBAC)**. Designed with high performance, scalability, and modularity in mind, it is suitable for production-ready applications.



## **Features**

- **High Performance**  
    Built with **asynchronous operations** to ensure speed and responsiveness.
    
- **Security**  
    Implements robust security features including:
    
    - **JWT Authentication**
    - Password hashing with **bcrypt**
    - **Role-based access control (RBAC)** for fine-grained permissions.
- **Scalability**  
    Leverages **MongoDB** for horizontal scalability and ensures a modular API design.
    
- **Maintainability**  
    Follows a **clean and modular structure** with clear separation of concerns for easier maintenance.
    


## Prerequisites

- Python 3.9+
- pip
- Virtual environment support
  
## **Libraries Used**

- **FastAPI**
- **MongoDB**
- **PyMongo**
- **bcrypt** 
- **JWT** 



## **Installation and Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/pavandandla/FastAPI-User-Management-API-with-MongoDB.git
cd FastAPI-User-Management-API-with-MongoDB
```

### **2. Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### **3. Install dependencies**

```bash
pip install -r src/requirements.txt
```

### **4. Configure environment variables**

Create a `.env` file in the project root directory and add the following configurations:

```plaintext
MONGO_URI=mongodb://localhost:27017
DB_NAME=your_database_name
SECRET_KEY=your_secret_key
JWT_EXPIRATION_MINUTES=30
```

- **MONGO_URI**: Your MongoDB connection string.
- **DB_NAME**: Name of the database.
- **SECRET_KEY**: Secret key for JWT encoding and decoding.
- **JWT_EXPIRATION_MINUTES**: Token expiration time in minutes.



### **5. Run the application**

Start the FastAPI server using **Uvicorn**:

```bash
uvicorn src.app:app --reload
```

The API will be available at: `http://127.0.0.1:8000`





## **Workflow**

1. **User Registration**
    
    - A user registers with an email and password.
    - Passwords are securely hashed using **bcrypt** before being stored in the MongoDB database.
2. **User Authentication**
    
    - The user logs in with valid credentials.
    - A **JWT token** is issued, which is required to access protected routes.
3. **Role-Based Access Control**
    
    - Role checks ensure only authorized users (e.g., Admins) can perform sensitive actions like deleting or updating other users.
4. **CRUD Operations**
    
    - Users can perform CRUD operations on their data.
    - Admins have full access to all user data.



## **Environment Configuration**

Environment variables are used to keep configurations flexible and secure. Example `.env` file:

```plaintext
MONGO_URI=mongodb://localhost:27017
DB_NAME=fastapi_user_db
SECRET_KEY=your_secret_key
JWT_EXPIRATION_MINUTES=30
```



## **Contact**

For questions, suggestions, or issues, contact:

- GitHub: [pavandandla](https://github.com/pavandandla)
