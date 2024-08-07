# Art Recommendation System

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Data Sources](#data-sources)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Evaluation](#evaluation)
9. [Contributing](#contributing)
10. [License](#license)

## Introduction
The Art Recommendation System is a comprehensive solution designed to provide personalized art recommendations to users. It leverages various recommendation techniques such as content-based filtering, collaborative filtering, demographic filtering, and knowledge-based filtering. The system combines these techniques using an ensemble approach to ensure accurate and personalized recommendations.

**Access the application [here](https://art-recommender.onrender.com/).**

## Features
- **Content-Based Recommendations**: Suggests artworks similar to those a user has interacted with.
- **Collaborative Filtering**: Recommends artworks based on interactions of similar users.
- **Demographic Recommendations**: Uses user demographic information to suggest artworks.
- **Knowledge-Based Recommendations**: Leverages domain-specific knowledge and user preferences.
- **Ensemble Recommendations**: Combines multiple recommendation techniques for better accuracy.
- **Exhibition Recommendations**: Suggests relevant exhibitions based on user preferences.

## Data Sources
The primary data source for this project is the [Art Institute of Chicago API](https://api.artic.edu/docs/). The API provides data on:
- Artworks
- Artists
- Exhibitions
- Galleries

## Installation
To set up the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/art-recommendation-system.git
   cd art-recommendation-system
   ```

2. **Set up a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python manage.py migrate
   ```

4. **Populate the database with initial data**:
   ```bash
   python manage.py runscript populate_data
   ```

## Usage
1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000`.

3. **Interact with the system**:
   - Register a new user or log in with an existing account.
   - Explore artwork recommendations.
   - View recommended exhibitions.

## Database Schema
The database schema includes tables for:
- **UserProfile**: Stores user information and preferences.
- **Artwork**: Stores information about artworks.
- **Exhibition**: Stores information about exhibitions.
- **UserInteraction**: Records interactions between users and artworks (e.g., views, likes, shares).
- **Preference**: Stores user preferences related to art types.

## API Endpoints
The project interacts with the following API endpoints from the Art Institute of Chicago:
- `/artworks`: Retrieves information about artworks.
- `/artists`: Retrieves information about artists.
- `/exhibitions`: Retrieves information about exhibitions.
- `/galleries`: Retrieves information about galleries.

## Evaluation
The recommendation models are evaluated using precision and recall metrics to measure accuracy and relevance.

### Precision
\[ \text{Precision@K} = \frac{| \{ \text{Relevant Items} \} \cap \{ \text{Recommended Items@K} \} |}{K} \]

### Recall
\[ \text{Recall@K} = \frac{| \{ \text{Relevant Items} \} \cap \{ \text{Recommended Items@K} \} |}{| \{ \text{Relevant Items} \} |} \]

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README file further based on your project's specifics and preferences.