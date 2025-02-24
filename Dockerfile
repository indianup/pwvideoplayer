# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY bot.py .

# Set environment variables (if needed)
ENV BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Run the bot
CMD ["python", "bot.py"]
