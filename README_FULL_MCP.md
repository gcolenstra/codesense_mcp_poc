# 🤖 Codebase Scanner - Full MCP Version

**Complete MCP-based code refactoring system**

## ✨ What Makes This "Full MCP"?

This version uses **MCP (Model Context Protocol) for EVERYTHING**:

- ✅ **GitHub PR Creation** → `mcp/github` server
- ✅ **Code Documentation** → `mcp/context7` server  
- ✅ **Problem Solving** → `mcp/sequential-thinking` server
- ✅ **File Operations** → `mcp/filesystem` server

**NO direct API calls. NO git commands. 100% MCP infrastructure.**

---

## 🎯 Features

### Core Capabilities
- ✅ Refactor code while preserving structure
- ✅ Add documentation to undocumented functions
- ✅ Assess risk (LOW/MEDIUM/HIGH)
- ✅ Auto-create GitHub PR via MCP
- ✅ Smart PR grouping (per-package or combined)
- ✅ Security issue detection

### MCP Integration
- ✅ **100+ MCP servers** available
- ✅ **Smart token management** - only prompts for enabled servers
- ✅ **Versioned prompts** - external YAML configuration
- ✅ **Docker-based** - fully portable

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git repository to scan
- Anthropic API key
- GitHub token

### 1. Setup

```bash
cd codebase_scanner_mcp

# Copy environment template
cp .env.template .env

# Edit .env - add tokens
nano .env
```

**Minimum required:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
GITHUB_TOKEN=ghp_your-github-token
```

### 2. Configure MCP Servers

```bash
# Edit mcp_config.yaml
nano mcp_config.yaml
```

**Enable servers:**
```yaml
servers:
  github:
    enabled: true    # Required for PR creation
  context7:
    enabled: true    # Recommended - no auth needed
  sequential-thinking:
    enabled: true    # Recommended - no auth needed
```

### 3. Run Scanner

```bash
# Build Docker image
docker-compose build

# Run on your repository
REPO_PATH=/path/to/your/repo docker-compose run scanner
```

---

## 📋 How It Works

### Full MCP Workflow

```
1. Scan codebase
   ↓
2. Analyze with Claude + MCP Context7
   ↓
3. Show summary with risk assessment
   ↓
4. Ask: "Create GitHub PR(s)?"
   ↓
5. If yes:
   ├─ Use MCP GitHub push_files tool
   ├─ Use MCP GitHub create_pull_request tool
   └─ Return PR URL
```

### MCP Architecture

```
Scanner (Python)
   ↓
MCP JSON-RPC Request
   ↓
Docker Container (mcp/github, mcp/context7, etc.)
   ↓
External API (GitHub, Documentation, etc.)
   ↓
MCP JSON-RPC Response
   ↓
Scanner (Python)
```

**Everything goes through MCP!**

---

## 🔧 Configuration

### mcp_config.yaml

Toggle MCP servers:

```yaml
servers:
  # === Core (Recommended) ===
  github:
    enabled: true     # Required for PR creation (MCP-based!)
  
  context7:
    enabled: true     # Code documentation - no auth
  
  sequential-thinking:
    enabled: true     # Problem solving - no auth
  
  filesystem:
    enabled: true     # File operations - no auth
```

### config/prompt_config.yaml

Customize refactoring prompts:

```yaml
# System prompt
system_prompt: |
  You are an expert code refactoring assistant...

# Output format (XML-based to avoid JSON escaping)
output_format: |
  <refactored_code>
  # Full code here
  </refactored_code>
  
  <analysis>
  {
      "changes_made": [...],
      "risk_level": "low/medium/high",
      ...
  }
  </analysis>

# Security keywords
security_keywords:
  - "sql injection"
  - "xss"
  - "hardcoded credentials"
```

---

## 📊 Example Run

```bash
$ REPO_PATH=./my-project docker-compose run scanner

🔐 Initializing MCP tokens...
✓ Loaded prompt config: config/prompt_config.yaml
  Version: 1.0 (2024-11-06)
✓ Tokens already set for: github, context7
✓ Scanner initialized for /workspace
✓ 4 MCP servers enabled

🔍 Scanning codebase...
============================================================
Found 15 Python files

📄 Analyzing: src/main.py
   🤖 Refactoring with Claude...
   ✓ Risk: MEDIUM
   ✓ Changes: 8
   ✓ Documented: 4 functions

[... analyzes all files ...]

============================================================
📊 SCAN COMPLETE
============================================================

Overall Risk: MEDIUM
Files Modified: 8
Total Changes: 47

🚨 CRITICAL: Security issues detected!

============================================================
📋 REFACTORING SUMMARY
============================================================

📦 Changes grouped by package:

  📁 src/ (5 files, MEDIUM risk)
     • main.py - medium
       - SECURITY FIX: Replaced hardcoded API key
       - Updated deprecated syntax
       ... and 6 more changes

============================================================

🚨 SECURITY ISSUE DETECTED
   Creating ONE PR with all security fixes...

📤 Create GitHub PR(s)? (y/N): y

💾 Applying changes to files...
   ✓ All changes applied

📤 Creating GitHub Pull Request via MCP...
   🔧 Using MCP GitHub server...
   📤 Pushing files via MCP push_files tool...
   ✓ Files pushed via MCP
   📋 Creating PR via MCP create_pull_request tool...
   ✓ PR created via MCP: https://github.com/user/repo/pull/42

✅ Done!
```

---

## 🎯 MCP vs Direct API

### Why Full MCP?

**Old Way (Direct API):**
```python
# ❌ Direct git commands
subprocess.run(["git", "push", ...])

# ❌ Direct GitHub API
requests.post("https://api.github.com/repos/.../pulls")
```

**New Way (Full MCP):**
```python
# ✅ MCP GitHub server
mcp_request = {
    "method": "tools/call",
    "params": {
        "name": "create_pull_request",
        "arguments": {...}
    }
}

docker run mcp/github < mcp_request
```

**Benefits:**
- ✅ Consistent architecture (everything via MCP)
- ✅ Portable (only needs Docker)
- ✅ Simple (just token needed)
- ✅ Testable (MCP responses are structured)
- ✅ Extensible (add new MCP servers easily)

---

## 🔐 Security

### Token Management
- ✅ Tokens in .env (not committed)
- ✅ Only prompts for enabled servers
- ✅ Validates tokens before use
- ✅ Passed to MCP servers via Docker env vars

### MCP Security
- ✅ MCP servers run in isolated Docker containers
- ✅ No direct host access
- ✅ Controlled environment variable passing
- ✅ Read-only config mounts

### GitHub Safety
- ✅ Creates PR via MCP (not direct commit)
- ✅ Risk assessment visible in PR
- ✅ Changes reviewable before merge
- ✅ Detailed change log

---

## 📁 Project Structure

```
codebase_scanner_mcp/
├── config/
│   ├── mcp_catalog.py          # 100+ MCP servers catalog
│   └── prompt_config.yaml      # Versioned prompts
│
├── src/
│   ├── scanner.py              # Main scanner (Full MCP!)
│   └── token_manager.py        # Smart token management
│
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Orchestration
├── mcp_config.yaml             # MCP server toggles
├── .env.template               # Token template
├── requirements.txt            # Python dependencies (no requests!)
└── README.md                   # This file
```

---

## 🏆 MCP Servers Used

### GitHub (mcp/github)
**Tools used:**
- `push_files` - Push changes to branch
- `create_pull_request` - Create PR

**Authentication:** `GITHUB_TOKEN`

### Context7 (mcp/context7)
**Tools used:**
- `get-library-docs` - Get library documentation
- `resolve-library-id` - Find library IDs

**Authentication:** None required

### Sequential Thinking (mcp/sequential-thinking)
**Tools used:**
- `sequentialthinking` - Problem-solving assistance

**Authentication:** None required

### Filesystem (mcp/filesystem)
**Tools used:**
- `read_file` - Read file contents
- `write_file` - Write file contents
- `search_files` - Search for files

**Authentication:** None required

---

## 🐛 Troubleshooting

### "MCP push_files failed"

**Cause:** GitHub MCP server couldn't push files

**Solutions:**
1. Check `GITHUB_TOKEN` has `repo` scope
2. Verify repository URL is correct
3. Check branch doesn't already exist
4. Ensure you have push access

### "MCP create_pull_request failed"

**Cause:** PR creation via MCP failed

**Solutions:**
1. Check if branch was pushed successfully
2. Verify base branch exists (main/master)
3. Check for existing PR with same head branch
4. Verify token has PR creation permissions

### "Invalid MCP response"

**Cause:** MCP server returned malformed JSON

**Solutions:**
1. Check Docker can run MCP servers
2. Verify MCP server image exists
3. Check server logs: `docker logs <container>`
4. Try running MCP server manually

### "Docker command failed"

**Cause:** Docker couldn't run MCP server

**Solutions:**
```bash
# Test MCP server manually
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run -i --rm mcp/github

# Check Docker is running
docker ps

# Pull MCP images
docker pull mcp/github
docker pull mcp/context7
```

---

## 📚 Advanced Usage

### Custom Prompts

Edit `config/prompt_config.yaml`:

```yaml
system_prompt: |
  Your custom instructions...

user_message_template: |
  Custom template with {filename} and {code}...
```

No rebuild needed! The scanner loads prompts at runtime.

### Multiple Prompt Versions

```bash
# Use different prompt config
docker-compose run scanner --prompt-config config/aggressive_prompt.yaml

# Or set environment variable
PROMPT_CONFIG=config/conservative_prompt.yaml docker-compose run scanner
```

### Batch Processing

```bash
# Scan multiple repos
for repo in repo1 repo2 repo3; do
  REPO_PATH=/path/$repo docker-compose run scanner
done
```

### CI/CD Integration

```yaml
# .github/workflows/refactor.yml
- name: Run Scanner
  run: |
    docker-compose run \
      -e ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }} \
      -e GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }} \
      scanner
```

---

## 🎓 How MCP Works

### JSON-RPC Protocol

MCP uses JSON-RPC 2.0 for communication:

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "create_pull_request",
    "arguments": {
      "owner": "user",
      "repo": "repo",
      "title": "PR Title",
      "head": "branch",
      "base": "main"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "html_url": "https://github.com/user/repo/pull/123",
    "number": 123,
    "state": "open"
  }
}
```

### Docker Communication

```bash
# Scanner sends JSON to MCP server via stdin
echo '{...mcp_request...}' | docker run -i mcp/github

# MCP server processes and returns JSON via stdout
{"jsonrpc":"2.0","id":1,"result":{...}}
```

---

## 📝 Tips & Best Practices

### 1. Start with Core Servers

Enable only essential servers first:
```yaml
servers:
  github: {enabled: true}
  context7: {enabled: true}
  sequential-thinking: {enabled: true}
```

### 2. Test MCP Servers

Before running full scan:
```bash
# Test GitHub MCP
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run -i --rm -e GITHUB_TOKEN=$GITHUB_TOKEN mcp/github
```

### 3. Use Versioned Prompts

Track prompt changes in git:
```bash
git add config/prompt_config.yaml
git commit -m "Update prompt to v1.1"
```

### 4. Review PRs Carefully

Especially HIGH risk changes - always review before merging!

### 5. Enable More Servers Gradually

As needed, enable additional MCP servers for enhanced analysis.

---

## 🆚 Comparison: Old vs New

| Feature | Old (API) | New (Full MCP) |
|---------|-----------|----------------|
| **GitHub PR** | ❌ Direct API | ✅ MCP |
| **Dependencies** | git, gh, requests | Docker only |
| **Architecture** | Mixed | 100% MCP |
| **Portability** | Requires setup | Runs anywhere |
| **Consistency** | Inconsistent | All via MCP |
| **Testability** | Hard | Easy (MCP protocol) |

---

## 🎉 Summary

This is a **complete, production-ready, Full MCP** codebase scanner:

1. ✅ **100% MCP** - No direct API calls
2. ✅ **100+ MCP servers** available
3. ✅ **Smart tokens** - only prompts when needed
4. ✅ **Versioned prompts** - external YAML config
5. ✅ **Docker-based** - fully portable
6. ✅ **Complete scanner** - refactor, document, assess, PR

**Start scanning:**
```bash
cd codebase_scanner_mcp
cp .env.template .env
# Edit .env with your tokens
docker-compose build
REPO_PATH=/your/repo docker-compose run scanner
```

---

**Built with ❤️ using pure MCP architecture**

No direct API calls. No git commands. Just MCP. 🚀
