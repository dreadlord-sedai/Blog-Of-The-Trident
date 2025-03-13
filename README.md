# Blog of the Trident

![Blog of the Trident Logo](https://skillicons.dev/icons?i=flask,py,bootstrap,sass,sqlite)

## Table of Contents
- [Blog of the Trident](#blog-of-the-trident)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Error Handling](#error-handling)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Introduction
Blog of the Trident is a microblogging platform built with Flask that allows users to create and share content, interact with other users, and customize their profiles. The application provides a clean, intuitive interface for writing and publishing blog posts, messaging other users, and managing personal accounts.

## Features
- **User Authentication** - Secure registration and login system
- **Profile Management** - Users can create, view, and edit their profiles
- **Blog Creation** - Write, edit, and publish blog posts
- **Messaging System** - Private messaging between users
- **Responsive Design** - Mobile-friendly interface using Bootstrap and SASS
- **Database Integration** - SQLAlchemy with SQLite for efficient data management
- **Error Handling** - Custom error pages and intuitive error responses

## Technologies Used
- **Python**: Core programming language for backend development
- **Flask**: Micro web framework for building the application
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for storing user and blog data
- **Bootstrap**: Frontend framework for responsive design
- **SASS**: CSS preprocessor for advanced styling
- **Jinja2**: Template engine for Python
- **WTForms**: Form handling and validation

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,flask,bootstrap,sass,sqlite" />
  </a>
</p>

## Project Structure
```
Blog-Of-The-Trident/
│
├── app/
│   ├── __init__.py             # Application factory and configuration
│   ├── main/                   # Main application routes
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── ...             # Templates for main routes
│   ├── errors/                 # Error handling modules
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── errors.py
│   ├── templates/              # HTML templates
│   │   ├── errors/
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── ...
│   └── ...                     # Other modules (auth, blog, user, etc.)
├── venv/                       # Python virtual environment
│   ├── Scripts/
│   │   ├── activate
│   │   └── ...
│   └── ...
├── config.py                   # Application configuration
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── run.py                      # Application entry point
```

## Installation
To get a local copy up and running, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/[your-username]/Blog-Of-The-Trident.git
    ```

2. **Navigate to the project directory**:
    ```sh
    cd Blog-Of-The-Trident
    ```

3. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # macOS/Linux
    source venv/bin/activate
    ```

4. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Set up environment variables**:
    Create a `.env` file in the root directory with the following variables:
    ```
    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///blog.db
    ```

6. **Initialize the database**:
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

7. **Run the application**:
    ```sh
    flask run
    ```
    or
    ```sh
    python run.py
    ```

## Usage
1. **Register an account** at the registration page.
2. **Login** with your credentials.
3. **Create a profile** or edit your existing one.
4. **Write blog posts** by clicking on "New Post" button.
5. **Browse other users'** blogs and profiles.
6. **Send messages** to other users through the messaging system.

## API Endpoints
Blog of the Trident provides several API endpoints for programmatic access:

- `GET /api/users/<id>` - Get user information
- `GET /api/posts/<id>` - Get post information
- `POST /api/posts` - Create a new post (authentication required)
- `PUT /api/posts/<id>` - Update a post (authentication required)
- `DELETE /api/posts/<id>` - Delete a post (authentication required)

## Error Handling
The application includes custom error pages:
- 404 Not Found
- 500 Internal Server Error
- Additional error handlers for API error responses

## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or feedback, feel free to reach out:

- **Email**: [dahamifabbio@gmail.com](mailto:dahamifabbio@gmail.com)
- **GitHub**: [dreadlord-sedai](https://github.com/dreadlord-sedai)
