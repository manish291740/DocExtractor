
# Document Processing Django Application

This Django application allows users to register, log in, and upload images or PDFs. Once uploaded, the application extracts text from these documents and analyzes the text using NLP models, such as those provided by SpaCy or Hugging Face Transformers.


## Features

- User Registration & Login: Users can create an account and log in to the application.
- File Upload: Users can upload images or PDF documents.
- Text Extraction: The application extracts text from uploaded documents.
- Text Analysis: The extracted text is analyzed using NLP models like SpaCy or Hugging Face Transformers.
- Data Display: The uploaded documents  are displayed in a table, where users can initiate the processing and their extracted text display on page.


## Prerequisites

- Python 3.10.5
- MySQL Database
## Installation

1. Clone the Repository

```bash
git clone https://github.com/manish291740/DocExtractor.git
cd <your-repo-directory>
```

2. Install Requirements

    Install the necessary Python packages:
    
```bash
pip install -r requirements.txt

```
 3. Set Up MySQL Database   

 - Ensure MySQL is installed and running on your machine.
- Create a database named document:

```sql
CREATE DATABASE document;
```
-   Configure your database settings in the settings.py file of your Django project:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'document',
        'USER': 'root',
        'PASSWORD': '<your-mysql-password>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```

5. Apply Migrations
 Run the following commands to apply migrations:

 ```bash
 python manage.py makemigrations
python manage.py migrate

 ```

 6. Create a Superuser

 To access the Django admin panel, create a superuser account:

 ```bash
 python manage.py createsuperuser
```

7. Run the Server
Start the development server:

```bash
python manage.py runserver
```
The application will be hosted at http://127.0.0.1:8000/.



## Usage

1. Register and Login: Access the application and register a new user account. After registering, log in with your credentials.
2. Upload Files: Navigate to the upload section and submit an image or PDF document.
3. Start Processing: Once the document is uploaded, it will be displayed in a table. From here, you can start the text extraction and analysis process.
4. View Results: After processing, the extracted and analyzed text will be displayed on the screen.



## Tech Stack

- Django: Web framework used for building the application.
- MySQL: Database used for storing user information and uploaded documents.
- SpaCy / Hugging Face Transformers: NLP libraries used for text extraction and analysis.

