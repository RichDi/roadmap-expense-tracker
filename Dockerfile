# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pip dependencies
RUN pip install --upgrade pip setuptools wheel

# Install the package dependencies
RUN pip install -r requirements.txt

# Install the CLI package
RUN pip install .

# Make sure the CLI command is accessible
# Test the installation by showing the help command (optional)
RUN expense-tracker --help

# Define the default command (optional, for testing directly)
CMD ["expense-tracker", "--help"]
