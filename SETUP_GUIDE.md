# Lab 11 Setup Guide

This guide will help you set up the Lab 11 environment with virtual environment and proper API key management.

## Quick Setup (Recommended)

### For Linux/Mac Users

```bash
# 1. Run the setup script
chmod +x setup_venv.sh
./setup_venv.sh

# 2. Edit .env and add your API key
nano .env  # or use your preferred editor

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Run the lab
cd src
python main.py
```

### For Windows Users

```bash
# 1. Run the setup script
setup_venv.bat

# 2. Edit .env and add your API key
notepad .env  # or use your preferred editor

# 3. Activate the virtual environment
venv\Scripts\activate

# 4. Run the lab
cd src
python main.py
```

---

## Manual Setup (Alternative)

If the automated scripts don't work, follow these manual steps:

### Step 1: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your-actual-api-key-here
   ```

3. Get your API key at: https://aistudio.google.com/apikey

### Step 4: Verify Installation

```bash
# Check Python version (should be 3.10+)
python --version

# Check installed packages
pip list | grep -E "google|nemo|dotenv"

# Expected output:
# google-adk          0.3.0+
# google-genai        1.0.0+
# nemoguardrails      0.10.0+
# python-dotenv       1.0.0+
```

---

## Environment Variables

The `.env` file supports the following variables:

### Required

```bash
# Your Google API key (required)
GOOGLE_API_KEY=your-google-api-key-here
```

### Optional

```bash
# Use Vertex AI instead of AI Studio (default: 0)
GOOGLE_GENAI_USE_VERTEXAI=0

# Default model to use (default: gemini-2.5-flash-lite)
DEFAULT_MODEL=gemini-2.5-flash-lite

# Rate limiting configuration
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
```

---

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution:**
1. Make sure `.env` file exists in the project root
2. Check that `.env` contains `GOOGLE_API_KEY=your-key`
3. Verify the key is valid at https://aistudio.google.com/apikey
4. Restart your terminal/IDE after editing `.env`

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Virtual environment not activating

**Linux/Mac:**
```bash
# Make sure script is executable
chmod +x setup_venv.sh

# Try activating manually
source venv/bin/activate
```

**Windows:**
```bash
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
venv\Scripts\activate
```

### Issue: NeMo Guardrails installation fails

**Solution:**
```bash
# NeMo has many dependencies, try installing separately:
pip install nemoguardrails>=0.10.0

# If it still fails, the lab will skip Part 2C automatically
# You can still complete the rest of the lab
```

### Issue: Permission denied on setup scripts

**Linux/Mac:**
```bash
# Make scripts executable
chmod +x setup_venv.sh

# Run with bash explicitly
bash setup_venv.sh
```

---

## Verifying Your Setup

Run this verification script to check everything is working:

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run verification
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

print('✅ Checking setup...')
print(f'Python: OK')

try:
    import google.genai
    print(f'google-genai: OK')
except ImportError:
    print(f'❌ google-genai: NOT INSTALLED')

try:
    import google.adk
    print(f'google-adk: OK')
except ImportError:
    print(f'❌ google-adk: NOT INSTALLED')

try:
    from dotenv import load_dotenv
    print(f'python-dotenv: OK')
except ImportError:
    print(f'❌ python-dotenv: NOT INSTALLED')

api_key = os.getenv('GOOGLE_API_KEY')
if api_key and api_key != 'your-google-api-key-here':
    print(f'GOOGLE_API_KEY: OK (length: {len(api_key)})')
else:
    print(f'❌ GOOGLE_API_KEY: NOT SET')

print('✅ Setup verification complete!')
"
```

Expected output:
```
✅ Checking setup...
Python: OK
google-genai: OK
google-adk: OK
python-dotenv: OK
GOOGLE_API_KEY: OK (length: 39)
✅ Setup verification complete!
```

---

## Running the Lab

Once setup is complete:

### Run All Parts
```bash
cd src
python main.py
```

### Run Specific Parts
```bash
python main.py --part 1    # Attacks
python main.py --part 2    # Guardrails
python main.py --part 3    # Testing
python main.py --part 4    # HITL
```

### Run Assignment 11
```bash
# From project root
python assignment11_starter.py
```

---

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

---

## Updating Dependencies

If you need to update packages:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Update specific package
pip install --upgrade google-genai

# Or update all packages
pip install --upgrade -r requirements.txt
```

---

## Clean Reinstall

If something goes wrong and you want to start fresh:

**Linux/Mac:**
```bash
# Remove virtual environment
rm -rf venv

# Remove .env (backup first if needed)
rm .env

# Run setup again
./setup_venv.sh
```

**Windows:**
```bash
# Remove virtual environment
rmdir /s /q venv

# Remove .env (backup first if needed)
del .env

# Run setup again
setup_venv.bat
```

---

## Security Best Practices

1. **Never commit `.env` to version control**
   - The `.env` file is already in `.gitignore`
   - Always use `.env.example` as a template

2. **Keep your API key secure**
   - Don't share your `.env` file
   - Don't hardcode API keys in code
   - Rotate keys regularly

3. **Use environment-specific configurations**
   - Development: `.env`
   - Production: Use proper secret management (e.g., AWS Secrets Manager)

---

## Next Steps

After successful setup:

1. ✅ Read [QUICK_START.md](QUICK_START.md) for usage instructions
2. ✅ Review [README.md](README.md) for lab overview
3. ✅ Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
4. ✅ Run `python src/main.py` to start the lab

---

## Getting Help

If you encounter issues not covered here:

1. Check the [QUICK_START.md](QUICK_START.md) troubleshooting section
2. Review the error messages carefully
3. Verify all prerequisites are met
4. Try a clean reinstall
5. Check the official documentation:
   - Google AI Studio: https://ai.google.dev/
   - Google ADK: https://google.github.io/adk-docs/
   - NeMo Guardrails: https://github.com/NVIDIA/NeMo-Guardrails

---

**Last Updated**: April 16, 2026  
**Version**: 2.0 (with venv and .env support)
