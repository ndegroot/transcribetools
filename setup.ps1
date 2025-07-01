# Install uv
Write-Host "Installing uv..."
irm https://astral.sh/uv/install.ps1 | iex

# Create a virtual environment
#Write-Host "Creating virtual environment..."
#uv venv

# Activate the virtual environment
#Write-Host "Activating virtual environment..."
#.venv\Scripts\activate

# Install required packages
#Write-Host "Installing required packages..."
#uv pip install -r requirements.txt

# install tool
uv install transcribetools

Write-Host "Setup complete. TranscribeTools is installed. Run by using 'uv tool transcribetools'  "