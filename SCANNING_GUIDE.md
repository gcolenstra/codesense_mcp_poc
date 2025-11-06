# 🔍 How to Scan Your Repository

## The scanner DOES recursively search subdirectories!

The scanner uses `rglob("*.py")` which automatically searches all subdirectories.

## ✅ Correct Ways to Run

### Method 1: Using REPO_PATH environment variable (Recommended)

```bash
REPO_PATH=/path/to/your/repo docker-compose run scanner
```

**Example:**
```bash
REPO_PATH=~/projects/my-app docker-compose run scanner
REPO_PATH=/home/user/code/backend docker-compose run scanner
```

### Method 2: Using command line argument

```bash
docker-compose run scanner /path/to/repo
```

**Note:** The path must be accessible from inside the Docker container. Using `REPO_PATH` is easier because docker-compose automatically mounts it.

### Method 3: Default to current directory

If you're already in your repo:
```bash
cd /path/to/your/repo
REPO_PATH=$(pwd) docker-compose run scanner
```

## 🔍 What Gets Scanned

The scanner:
✅ **Recursively searches ALL subdirectories**
✅ Finds every `.py` file

**Skips:**
- ❌ Hidden directories (`.git`, `.vscode`, etc.)
- ❌ Virtual environments (`venv/`, `env/`)
- ❌ Cache directories (`__pycache__/`)

## 📊 Example Output

```bash
$ REPO_PATH=~/projects/my-app docker-compose run scanner

🔍 Searching for Python files in: /workspace
   (Recursively scanning all subdirectories...)
   Found 47 Python files across all subdirectories
   Directories found: src, tests, scripts, utils, api, models

============================================================
Found 47 Python files

📄 Analyzing: src/main.py
📄 Analyzing: src/api/routes.py
📄 Analyzing: src/models/user.py
📄 Analyzing: tests/test_main.py
📄 Analyzing: utils/helpers.py
...
```

## 🗂️ Repository Structure Example

If your repo looks like this:
```
my-app/
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── handlers.py
│   └── models/
│       ├── user.py
│       └── product.py
├── tests/
│   ├── test_api.py
│   └── test_models.py
└── scripts/
    └── deploy.py
```

The scanner will find **ALL** Python files:
- `src/main.py`
- `src/api/routes.py`
- `src/api/handlers.py`
- `src/models/user.py`
- `src/models/product.py`
- `tests/test_api.py`
- `tests/test_models.py`
- `scripts/deploy.py`

## 🐛 Troubleshooting

### "Found 0 Python files"

**Cause:** Wrong path or permissions

**Fix:**
```bash
# Check if path exists
ls /path/to/your/repo

# Make sure it has Python files
find /path/to/your/repo -name "*.py" | head

# Try with absolute path
REPO_PATH=/absolute/path/to/repo docker-compose run scanner
```

### "Only finding files in current directory"

This shouldn't happen! The scanner uses `rglob("*.py")` which is recursive by default.

If this happens:
1. Check scanner output - it shows directories found
2. Make sure subdirectories aren't named `venv`, `env`, or start with `.`
3. Check file permissions

### "Permission denied"

```bash
# Make sure Docker can read the directory
chmod -R 755 /path/to/repo

# Or run with proper volume mount
docker-compose run -v /path/to/repo:/workspace:ro scanner
```

## 📝 Testing the Scanner

### Test 1: Verify Recursive Scan

Create a test repository:
```bash
mkdir -p test-repo/src/api
mkdir -p test-repo/src/models
mkdir -p test-repo/tests

# Create Python files in different directories
echo "print('main')" > test-repo/main.py
echo "print('api')" > test-repo/src/api/routes.py
echo "print('model')" > test-repo/src/models/user.py
echo "print('test')" > test-repo/tests/test_main.py

# Scan it
REPO_PATH=./test-repo docker-compose run scanner
```

You should see:
```
Found 4 Python files across all subdirectories
Directories found: src, tests
```

### Test 2: Check Your Real Repo

Before running the full scan:
```bash
# Count Python files manually
find /path/to/your/repo -name "*.py" -not -path "*/venv/*" -not -path "*/.git/*" | wc -l

# Then run scanner and compare
REPO_PATH=/path/to/your/repo docker-compose run scanner
```

The numbers should match!

## 💡 Pro Tips

### 1. Dry Run First
Check what will be scanned without actually refactoring:
```bash
# The scanner shows all files before asking to apply changes
REPO_PATH=/your/repo docker-compose run scanner
# Press 'N' when asked to apply changes
```

### 2. Scan Specific Subdirectory
```bash
# Only scan a specific subdirectory
REPO_PATH=/your/repo/src docker-compose run scanner
```

### 3. See What's Being Scanned
The improved scanner now shows:
- Total files found
- Which directories they're in
- Each file as it's analyzed

### 4. Verify Before Scanning
```bash
# List all Python files that will be scanned
find /your/repo -name "*.py" \
  -not -path "*/venv/*" \
  -not -path "*/env/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.git/*"
```

## ✅ Summary

**The scanner DOES recursively scan all subdirectories!**

Just use:
```bash
REPO_PATH=/your/repo docker-compose run scanner
```

And it will find every `.py` file in every subdirectory (except venv, .git, etc.)

If you're only seeing files in the current directory, something else is wrong - check the troubleshooting section above.
