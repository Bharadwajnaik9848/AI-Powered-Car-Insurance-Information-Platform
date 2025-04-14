# Car AI Assistant

A Flask web application that helps users compare cars and get AI-powered insights using Mistral AI.

## Features

- **Car Management**
  - Add, edit, and delete car listings
  - View detailed car information
  - Search and filter cars by make, model, and year

- **AI-Powered Car Comparisons**
  - Compare two cars side by side
  - Get AI-generated insights about value, features, and recommendations
  - View price differences and detailed analysis
  - Save and manage your comparisons

- **Insurance Estimates**
  - Get insurance estimates for your cars
  - Track and manage insurance information
  - Compare insurance costs across different cars

- **User Authentication**
  - Secure user registration and login
  - Personal dashboard for managing cars and comparisons
  - User-specific data isolation

## Tech Stack

- **Backend**: Python/Flask
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: Mistral AI API
- **Frontend**: HTML, Tailwind CSS
- **Authentication**: Flask-Login

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/car-ai-assistant.git
cd car-ai-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Environment Variables

Create a `.env` file with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
MISTRAL_API_KEY=your-mistral-api-key
```

## Project Structure

```
car-ai-assistant/
├── app.py                 # Main application file
├── config/               # Configuration files
│   ├── database.py       # Database configuration
│   └── settings.py       # Application settings
├── models/               # Database models
│   ├── car.py           # Car model
│   ├── comparison.py    # Car comparison model
│   ├── insurance.py     # Insurance model
│   └── user.py          # User model
├── routes/              # Route handlers
│   ├── admin.py         # Admin routes
│   ├── auth.py          # Authentication routes
│   ├── cars.py          # Car management routes
│   ├── chat.py          # AI chat routes
│   ├── comparisons.py   # Comparison routes
│   └── insurance.py     # Insurance routes
├── templates/           # HTML templates
│   ├── admin/          # Admin templates
│   ├── auth/           # Authentication templates
│   ├── cars/           # Car templates
│   ├── chat/           # Chat interface templates
│   ├── comparisons/    # Comparison templates
│   └── insurance/      # Insurance templates
├── static/             # Static files (CSS, JS, images)
├── utils/              # Utility functions
│   └── mistral_ai.py   # Mistral AI integration
├── migrations/         # Database migrations
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## API Integration

### Mistral AI

The application uses Mistral AI for:
- Generating car comparisons
- Providing AI-powered insights
- Answering car-related questions

To use the Mistral AI features:
1. Sign up for a Mistral AI API key
2. Add your API key to the `.env` file
3. The AI features will be automatically available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Mistral AI for providing the AI capabilities
- Flask team for the web framework
- Tailwind CSS team for the styling framework
