# ⚡ QUICK START - Codebase Scanner MCP

## 🎯 What You Have

A complete, production-ready codebase scanner that:
- ✅ **100+ MCP servers** from Docker's catalog
- ✅ **Smart token management** (only prompts for enabled servers)
- ✅ **Docker-based** (portable, runs anywhere)
- ✅ **Complete scanner** with refactoring, documentation, risk assessment, and auto-PR

## 🚀 Get Running in 5 Minutes

### Step 1: Setup (2 minutes)

```bash
cd /mnt/user-data/outputs/codebase_scanner_mcp

# Copy environment template
cp .env.template .env

# Edit .env - add minimum:
nano .env
```

**Add these two lines:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
GITHUB_TOKEN=ghp_your-token-here
```

**Get tokens:**
- **Anthropic**: https://console.anthropic.com/
- **GitHub**: https://github.com/settings/tokens (needs `repo` scope)

### Step 2: Build (1 minute)

```bash
# Build Docker image
docker-compose build
```

### Step 3: Run (2 minutes)

```bash
# Run on your repository
REPO_PATH=/path/to/your/repo docker-compose run scanner
```

**Example:**
```bash
REPO_PATH=~/projects/my-app docker-compose run scanner
```

That's it! The scanner will:
1. ✅ Analyze all Python files
2. ✅ Refactor outdated code
3. ✅ Add missing documentation
4. ✅ Assess risk levels
5. ✅ Create GitHub PR automatically

---

## 📋 What Happens

```
🔐 Initializing MCP tokens...
✓ Tokens already set for: github, context7
✓ Scanner initialized for /workspace
✓ 4 MCP servers enabled

🔍 Scanning codebase...
Found 15 Python files

📄 Analyzing: src/main.py
   🤖 Refactoring with Claude...
   ✓ Risk: MEDIUM
   ✓ Changes: 5
   ✓ Documented: 3 functions

[... analyzes all files ...]

📊 SCAN COMPLETE
Overall Risk: MEDIUM
Files Modified: 8
Total Changes: 23

💾 Apply changes to files? (y/N): y
✓ Applied changes to 8 files

📤 Create GitHub PR? (y/N): y
✓ PR created: https://github.com/user/repo/pull/123

✅ Done!
```

---

## 🎯 Key Features

### 1. Smart Token Management

**Only prompts for tokens you need!**

The scanner checks:
1. Which servers are **enabled** in `mcp_config.yaml`
2. Which servers **require authentication**
3. Which tokens are **not already set**

Then prompts **only for missing tokens**.

### 2. 100+ MCP Servers

**Comprehensive catalog** from Docker Hub:

- **github** - PR creation ✅ ENABLED
- **context7** - Code docs ✅ ENABLED  
- **sequential-thinking** - Problem solving ✅ ENABLED
- **firecrawl** - Web scraping
- **postgres**, **mongodb**, **mysql** - Databases
- **aws**, **azure**, **gcp** - Cloud
- **stripe** - Payments
- **notion**, **slack** - Productivity
- And 90+ more...

**Enable more in `mcp_config.yaml`:**
```yaml
servers:
  firecrawl:
    enabled: true  # Enable web scraping
  postgres:
    enabled: true  # Enable database analysis
```

### 3. Complete Scanner

**What it does:**

1. **Refactor Code**
   - Updates deprecated syntax
   - Modernizes patterns
   - **Preserves structure** (no architecture changes)

2. **Add Documentation**
   - Adds docstrings to undocumented functions
   - Does NOT modify existing docs
   - Clear, concise descriptions

3. **Assess Risk**
   - **LOW**: Doc only, minor updates
   - **MEDIUM**: Syntax changes, minor logic
   - **HIGH**: Significant logic changes

4. **Create GitHub PR**
   - Creates branch
   - Commits changes
   - Opens PR with:
     - Detailed summary
     - Risk assessment per file
     - Review guidelines
     - Statistics

---

## 🔧 Configuration

### Minimal Setup

**Default `mcp_config.yaml`** (already configured):
```yaml
servers:
  github: {enabled: true}      # For PR creation
  context7: {enabled: true}    # Code docs (no auth)
  sequential-thinking: {enabled: true}  # Problem solving (no auth)
```

**Minimal `.env`:**
```env
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
```

### Add More Servers

**Enable web scraping:**
```yaml
firecrawl:
  enabled: true
```

Then add to `.env`:
```env
FIRECRAWL_API_KEY=fc_...
```

The scanner will **automatically detect** and use it!

---

## 💡 Usage Examples

### Basic Scan
```bash
REPO_PATH=/path/to/repo docker-compose run scanner
```

### Scan Current Directory
```bash
REPO_PATH=$(pwd) docker-compose run scanner
```

### Non-Interactive (CI/CD)
```bash
# Export tokens
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_TOKEN=ghp_...

# Run scanner
docker-compose run scanner /workspace
```

### Test on Example Repo
```bash
# Clone a test repo
git clone https://github.com/example/old-python-project test-repo

# Scan it
REPO_PATH=./test-repo docker-compose run scanner
```

---

## 🐛 Common Issues

### "ANTHROPIC_API_KEY not set"
```bash
# Add to .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> .env
```

### "GITHUB_TOKEN not set"
```bash
# Add to .env
echo "GITHUB_TOKEN=ghp_your-token" >> .env
```

### "Docker socket permission denied"
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Want More MCP Servers?
```bash
# Edit config
nano mcp_config.yaml

# Enable servers you want
# Add tokens to .env
nano .env

# Run again
docker-compose run scanner
```

---

## 📚 Next Steps

### 1. Try It Now (5 min)
```bash
cd /mnt/user-data/outputs/codebase_scanner_mcp
cp .env.template .env
nano .env  # Add your tokens
docker-compose build
REPO_PATH=/your/repo docker-compose run scanner
```

### 2. Customize (10 min)
- Edit `mcp_config.yaml` to enable more servers
- Add corresponding tokens to `.env`
- Run again with enhanced capabilities

### 3. Integrate (30 min)
- Add to CI/CD pipeline
- Schedule periodic scans
- Automate code improvements

---

## 🎉 You're Ready!

**Complete project structure:**
```
codebase_scanner_mcp/
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
├── config/
│   └── mcp_catalog.py     ← 100+ MCP servers
├── src/
│   ├── scanner.py         ← Complete scanner
│   └── token_manager.py   ← Smart token mgmt
├── Dockerfile
├── docker-compose.yml
├── mcp_config.yaml        ← Toggle servers
├── .env.template          ← Token template
└── requirements.txt
```

**Start now:**
```bash
cd /mnt/user-data/outputs/codebase_scanner_mcp
cp .env.template .env
nano .env  # Add ANTHROPIC_API_KEY and GITHUB_TOKEN
docker-compose build
REPO_PATH=/your/repo docker-compose run scanner
```

---

**Need help?** Check [README.md](README.md) for full documentation.

**Everything working?** Start enabling more MCP servers for enhanced analysis!

🚀 Happy scanning!
