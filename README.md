# SecCodeSmith Backend

This repository contains the Django-powered REST API backend for the SecCodeSmith portfolio website. It provides endpoints for blog posts, project showcases, image properties, and static page content (About, Contact, Skills, Footer Links).

## Table of Contents

* [About](#about)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the Server](#running-the-server)
* [Running Tests](#running-tests)
* [API Reference](#api-reference)

  * [General API](#general-api)
  * [Blog API](#blog-api)
  * [Project API](#project-api)
  * [Images API](#images-api)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## About

SecCodeSmith Backend serves as the data layer for the portfolio site, supplying JSON over REST endpoints that the front-end consumes for dynamic content.

---

## Tech Stack

* **Python** 3.10+
* **Django** 5.2.1
* **Django REST Framework** 3.16.0
* **Markdown** for rich-text blog content
* **django-filter** for API filtering
* **psycopg2-binary** (optional) for PostgreSQL integration
* **python-decouple** for environment variable management
* **django-cors-headers** to enable CORS
* **Pillow** for image handling
* **django-extensions** for development utilities
* **pytest-django** for testing and CI integration ([github.com][1])

---

## Features

* **Blog Posts**: List, paginate, and count pages of blog entries.
* **Project Showcase**: List projects, view details, and filter by category.
* **Image Properties**: Serve metadata for portfolio images.
* **Static Pages**: Endpoints for About, Contact, Skills, and Footer Links content.
* **CSRF Support**: Retrieve CSRF tokens for secure front-end forms.
* **Admin Interface**: Built-in Django admin at `/admin/`. ([github.com][2])

---

## Requirements

* Python 3.10 or later
* pip (Python package installer)
* (Optional) PostgreSQL if you plan to use a production database

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/SecCodeSmith/SecCodeSmith-backend.git
   cd SecCodeSmith-backend
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

This project uses SQLite by default. To customize:

1. **Environment variables**
   Create a `.env` file in the project root (supported via `python-decouple`) to override:

   ```dotenv
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Database settings**

   * To switch to PostgreSQL, update the `DATABASES` section in `SecCodeSmithBackend/settings.py` accordingly.

---

## Running the Server

Apply migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## Running Tests

Execute the test suite with pytest:

```bash
pytest
```

---

## API Reference

### General API

Base path: `/api/`

| Endpoint            | Method | Description                            |
| ------------------- | ------ | -------------------------------------- |
| `/api/csrf`         | GET    | Retrieve CSRF token                    |
| `/api/skills-cards` | GET    | List skill cards for front-end display |
| `/api/about/`       | GET    | Get content for the “About” page       |
| `/api/footer-links` | GET    | List social/footer links               |
| `/api/contact/`     | GET    | Get content for the “Contact” page     |

---

### Blog API

Base path: `/blog-api/`

| Endpoint                        | Method | Description                              |
| ------------------------------- | ------ | ---------------------------------------- |
| `/blog-api/post/`               | GET    | List all blog posts                      |
| `/blog-api/count_pages/`        | GET    | Retrieve total number of paginated pages |
| `/blog-api/post-page/?page=<n>` | GET    | List posts on page `<n>`                 |

---

### Project API

Base path: `/project-api/` 

| Endpoint                      | Method | Description                            |
| ----------------------------- | ------ | -------------------------------------- |
| `/project-api/projects/`      | GET    | List all projects                      |
| `/project-api/projects/<id>/` | GET    | Get details for project with ID `<id>` |
| `/project-api/cat`            | GET    | List available project categories      |

---

### Images API

Base path: `/img/` 

| Endpoint           | Method | Description                                     |
| ------------------ | ------ | ----------------------------------------------- |
| `/img/Image/<id>/` | GET    | Retrieve properties (metadata) for image `<id>` |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/XYZ`)
5. Open a Pull Request

Please adhere to existing coding styles and include tests for new functionality.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

