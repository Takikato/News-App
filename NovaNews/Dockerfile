FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /code

# Copy requirements first (better caching)
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose Django’s default port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
