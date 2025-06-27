#!/bin/bash

# Get the current Python version
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")

# Define your project environment name
PROJECT_ENV_NAME="whatsbot-env-$PYTHON_VERSION"

# brew install pyenv-virtualenv

# Create the pyenv virtual environment
pyenv virtualenv "$PYTHON_VERSION" "$PROJECT_ENV_NAME"

echo "Virtual environment '$PROJECT_ENV_NAME' created using Python version $PYTHON_VERSION."

pyenv local "$PROJECT_ENV_NAME"

echo "Local pyenv version configured for $PROJECT_ENV_NAME"