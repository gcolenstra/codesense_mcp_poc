# 🤖 Codebase Scanner with MCP Integration

**Intelligent code refactoring, documentation, and automated PR creation using 100+ MCP servers**

## ✨ Features

### Core Capabilities
- ✅ **Refactor code** for version changes while preserving structure
- ✅ **Add documentation** to functions missing docstrings
- ✅ **Assess risk** (LOW/MEDIUM/HIGH) for all changes
- ✅ **Auto-create GitHub PR** with detailed summary and risk assessment
- ✅ **100+ MCP servers** available for enhanced analysis

### Smart Token Management
- ✅ **Only prompts for enabled servers** that need authentication
- ✅ **Auto-detects existing tokens** in environment
- ✅ **Interactive setup** or use .env file
- ✅ **Secure token storage**

### Docker-Based Deployment
- ✅ **Fully containerized** - portable and secure
- ✅ **No local dependencies** except Docker
- ✅ **Isolated MCP servers** running in containers
- ✅ **One-command deployment**

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git repository to scan
- Anthropic API key

### 1. Clone/Copy Project
```bash
# Copy the codebase_scanner_mcp directory to your machine
cp -r codebase_scanner_mcp ~/projects/
cd ~/projects/codebase_scanner_mcp
```

### 2. Configure
```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your tokens
nano .env
```

**Minimum required:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
GITHUB_TOKEN=ghp_your-github-token
```

### 3. Configure MCP Servers
```bash
# Edit mcp_config.yaml
nano mcp_config.yaml
```

**Enable servers you want to use:**
```yaml
servers:
  github:
    enabled: true    # Required for PR creation
  context7:
    enabled: true    # Recommended - no auth needed
  sequential-thinking:
    enabled: true    # Recommended - no auth needed
  # ... toggle others as needed
```

### 4. Run Scanner
```bash
# Build Docker image
docker-compose build

# Run on your repository
REPO_PATH=/path/to/your/repo docker-compose run scanner
```

**Example:**
```bash
REPO_PATH=~/projects/my-app docker-compose run scanner
```

---

## 📋 What It Does

### Step 1: Scan & Analyze
The scanner:
1. Finds all Python files in your repository
2. Analyzes each file for:
   - Outdated syntax/patterns
   - Missing documentation
   - Potential improvements
3. Uses Claude with MCP context for intelligent refactoring

### Step 2: Refactor & Document
For each file, it:
- ✅ Updates deprecated code patterns
- ✅ Modernizes syntax (Python 3.9+)
- ✅ Adds docstrings to undocumented functions
- ✅ **Preserves original structure** (no architecture changes)

### Step 3: Risk Assessment
Each change is assessed:
- **LOW**: Documentation only, minor syntax updates
- **MEDIUM**: Syntax changes, minor logic improvements
- **HIGH**: Significant logic changes, API modifications

### Step 4: Create GitHub PR
Automatically:
- ✅ Creates new branch
- ✅ Commits changes
- ✅ Pushes to GitHub
- ✅ Opens Pull Request with:
  - Detailed summary of all changes
  - Risk assessment for each file
  - Statistics (lines changed, functions documented)
  - Review guidelines based on risk level

---

## 🎯 Usage Examples

### Basic Scan
```bash
# Scan repository at current directory
docker-compose run scanner /workspace
```

### Scan Specific Repository
```bash
# Mount specific repo
REPO_PATH=/path/to/repo docker-compose run scanner
```

### Non-Interactive Mode
```bash
# Export tokens first
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_TOKEN=ghp_...

# Run scanner
docker-compose run scanner /workspace
```

### Interactive Token Setup
```bash
# Run token manager first
docker-compose run scanner python src/token_manager.py
```

---

## 📁 Project Structure

```
codebase_scanner_mcp/
├── config/
│   └── mcp_catalog.py          # 100+ MCP servers catalog
│
├── src/
│   ├── scanner.py              # Main scanner with all features
│   └── token_manager.py        # Smart token management
│
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Orchestration
├── mcp_config.yaml             # MCP server toggles
├── .env.template               # Token template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Configuration

### mcp_config.yaml

Toggle MCP servers on/off:

```yaml
servers:
  # === Core (Recommended) ===
  github:
    enabled: true     # Required for PR creation
  
  context7:
    enabled: true     # Code documentation - no auth
  
  sequential-thinking:
    enabled: true     # Problem solving - no auth
  
  # === Optional ===
  firecrawl:
    enabled: false    # Web scraping - needs API key
  
  postgres:
    enabled: false    # Database - needs connection string
  
  # ... 100+ more servers available
```

### .env File

Only provide tokens for **enabled** servers:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...

# Optional (only if enabled)
FIRECRAWL_API_KEY=fc_...
POSTGRES_URI=postgresql://...
```

**Smart token manager** will only prompt for missing tokens of enabled servers!

---

## 🏆 MCP Servers Available

### 100+ Servers Organized by Category

#### Development & Version Control
- **github** - GitHub repository management ✅ ENABLED BY DEFAULT
- **gitlab** - GitLab operations
- **git** - Local Git operations

#### Code Intelligence
- **context7** - Library documentation ✅ ENABLED BY DEFAULT
- **sequential-thinking** - Problem solving ✅ ENABLED BY DEFAULT
- **gemini-docs** - Google Gemini docs
- **astro-docs** - Astro framework docs

#### Web & Scraping
- **firecrawl** - Advanced web scraping
- **puppeteer** - Browser automation
- **apify** - Web scraping marketplace
- **brave** - Web search

#### Databases (40+ servers)
- **postgres**, **mongodb**, **mysql**, **redis**
- **elasticsearch**, **couchbase**, **neon**, **astra**
- **sqlite** - No auth required

#### Cloud Services
- **aws** - AWS operations
- **azure** - Azure AKS
- **gcp** - Google Cloud
- **heroku** - Heroku platform

#### DevOps & Monitoring
- **dockerhub** - Docker Hub management
- **grafana** - Monitoring dashboards
- **victoriametrics**, **victorialogs**, **victoriatraces**

#### Productivity
- **notion**, **slack**, **linear**

#### Payment
- **stripe** - Payment processing

#### And 60+ more...

**Full list:** See `config/mcp_catalog.py`

---

## 🎓 How It Works

### Architecture

```
Your Repository
      ↓
Docker Container (Scanner)
      ↓
┌─────────────┴──────────────┐
│                            │
Token Manager          Claude API
(Smart Prompting)     (Refactoring)
│                            │
└─────────────┬──────────────┘
              ↓
      MCP Infrastructure
      (100+ servers via Docker)
              ↓
┌─────────────┼──────────────┐
│             │              │
GitHub     Context7     Other MCP
(PR)      (Docs)        Servers
```

### Workflow

1. **Initialize**
   - Load mcp_config.yaml
   - Check enabled servers
   - Smart-prompt for missing tokens

2. **Scan**
   - Find all Python files
   - Analyze each file
   - Use Claude + MCP for refactoring

3. **Refactor**
   - Apply modern syntax
   - Add missing documentation
   - Preserve structure

4. **Assess Risk**
   - Analyze impact of changes
   - Assign LOW/MEDIUM/HIGH
   - Provide reasoning

5. **Create PR**
   - Create branch
   - Commit changes
   - Push to GitHub
   - Open PR with summary

---

## 📊 Example Output

```
🔐 Initializing MCP tokens...
✓ Tokens already set for: github, context7
ℹ️  No auth needed for: sequential-thinking, filesystem

✨ All required tokens are set!
✓ Scanner initialized for /workspace
✓ 4 MCP servers enabled

🔍 Scanning codebase...
============================================================
Found 15 Python files

📄 Analyzing: src/main.py
   🤖 Refactoring with Claude...
   ✓ Risk: MEDIUM
   ✓ Changes: 5
   ✓ Documented: 3 functions

📄 Analyzing: src/utils.py
   🤖 Refactoring with Claude...
   ✓ Risk: LOW
   ✓ Changes: 2
   ✓ Documented: 1 functions

...

============================================================
📊 SCAN COMPLETE
============================================================

Overall Risk: MEDIUM
Files Modified: 8
Total Changes: 23

💾 Apply changes to files? (y/N): y
   ✓ src/main.py
   ✓ src/utils.py
   ...

✓ Applied changes to 8 files

📤 Create GitHub PR? (y/N): y
   ✓ PR created: https://github.com/user/repo/pull/123

✅ Done!
```

---

## 🔒 Security

### Token Management
- ✅ Tokens stored in .env (not committed)
- ✅ Only prompts for enabled servers
- ✅ Validates tokens before use
- ✅ Secure environment variables

### Docker Isolation
- ✅ MCP servers run in containers
- ✅ No direct host access
- ✅ Controlled Docker socket access
- ✅ Read-only config mounts

### GitHub Safety
- ✅ Creates PR (not direct commit)
- ✅ Risk assessment visible
- ✅ Changes reviewable before merge
- ✅ Detailed change log

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
# Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> .env
```

### "GITHUB_TOKEN not set"
```bash
# Enable GitHub in config
# Edit mcp_config.yaml: github.enabled = true
# Add token to .env
echo "GITHUB_TOKEN=ghp_your-token" >> .env
```

### "Docker socket permission denied"
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### "gh CLI not found"
The scanner will fall back to GitHub API automatically. Or install gh:
```bash
# Inside container (if needed)
apt-get update && apt-get install gh
```

### Token prompts keep appearing
```bash
# Save tokens to .env file
cp .env.template .env
# Edit and fill in tokens
# Tokens will be auto-loaded
```

---

## 🎯 Tips & Best Practices

### 1. Start Small
Enable only essential servers first:
```yaml
servers:
  github: {enabled: true}
  context7: {enabled: true}
  sequential-thinking: {enabled: true}
```

### 2. Test on Branch
Run scanner on a test repository first to see results.

### 3. Review PRs Carefully
Always review the PR before merging, especially HIGH risk changes.

### 4. Use .env File
Store tokens in .env instead of environment variables for persistence.

### 5. Enable More Servers
As needed, enable additional MCP servers for enhanced analysis:
- **firecrawl** - If analyzing web scraping code
- **postgres** - If analyzing database code
- **aws** - If analyzing cloud infrastructure code

---

## 📚 Advanced Usage

### Custom Risk Thresholds
Edit `src/scanner.py` to customize risk assessment logic.

### Additional MCP Servers
Add more servers to `config/mcp_catalog.py` following the same pattern.

### Batch Processing
```bash
# Scan multiple repos
for repo in repo1 repo2 repo3; do
  REPO_PATH=/path/$repo docker-compose run scanner
done
```

### Integration with CI/CD
```yaml
# .github/workflows/scan.yml
- name: Run Codebase Scanner
  run: |
    docker-compose run \
      -e ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }} \
      -e GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }} \
      scanner
```

---

## 🤝 Contributing

Want to add more MCP servers or features?

1. Add server to `config/mcp_catalog.py`
2. Test with scanner
3. Submit PR

---

## 📄 License

MIT License - Use freely in your projects

---

## 🎉 Summary

This is a **complete, production-ready** codebase scanner that:

1. ✅ Uses **100+ MCP servers** from Docker's official catalog
2. ✅ **Smart token management** - only prompts for enabled servers needing auth
3. ✅ **Docker-based** - fully portable, runs anywhere
4. ✅ **Complete scanner** with:
   - Code refactoring (preserves structure)
   - Documentation generation
   - Risk assessment (LOW/MEDIUM/HIGH)
   - Automatic GitHub PR creation

**Start scanning now:**
```bash
cd codebase_scanner_mcp
cp .env.template .env
# Edit .env with your tokens
docker-compose build
REPO_PATH=/your/repo docker-compose run scanner
```

---

**Built with ❤️ using Docker's MCP infrastructure and Anthropic's Claude**
