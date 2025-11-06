"""
Complete Codebase Scanner with MCP Integration
Features:
- Refactor code for version changes (preserve structure)
- Add documentation to functions missing it
- Assess risk score (low/medium/high)
- Automatically create GitHub PR with summary
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import anthropic
import subprocess
import tempfile

from token_manager import TokenManager


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class FileAnalysis:
    """Analysis result for a single file"""
    file_path: str
    original_code: str
    refactored_code: str
    changes_made: List[str]
    risk_level: RiskLevel
    risk_reasoning: str
    functions_documented: int
    lines_changed: int


@dataclass
class CodebaseAnalysis:
    """Complete codebase analysis"""
    files: List[FileAnalysis]
    overall_risk: RiskLevel
    total_files: int
    total_changes: int
    summary: str
    packages: Dict[str, List[FileAnalysis]] = None  # Group by package/directory
    has_critical_security: bool = False


class CodebaseScanner:
    """
    Intelligent codebase scanner with MCP integration
    """
    
    def __init__(self, repo_path: str, config_path: str = "mcp_config.yaml", prompt_config_path: str = "config/prompt_config.yaml"):
        """
        Initialize scanner
        
        Args:
            repo_path: Path to Git repository
            config_path: Path to MCP config
            prompt_config_path: Path to prompt configuration file
        """
        self.repo_path = Path(repo_path)
        self.config_path = config_path
        self.prompt_config_path = prompt_config_path
        
        # Load prompt configuration
        self.prompt_config = self._load_prompt_config()
        
        # Initialize token manager
        print("🔐 Initializing MCP tokens...")
        self.token_manager = TokenManager(config_path)
        self.token_manager.load_from_env_file()
        
        # Check tokens (non-interactive for now)
        status = self.token_manager.check_tokens()
        if status['missing']:
            print(f"⚠️  Missing tokens: {', '.join(status['missing'])}")
            print("   Run token_manager.py first to set up tokens")
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        self.anthropic = anthropic.Anthropic(api_key=api_key)
        
        # Get enabled MCP servers
        self.mcp_tools = self._get_mcp_context()
        
        print(f"✓ Scanner initialized for {self.repo_path}")
        print(f"✓ {len(self.token_manager.get_enabled_servers())} MCP servers enabled")
    
    def _load_prompt_config(self) -> Dict:
        """Load prompt configuration from YAML file"""
        import yaml
        
        prompt_file = Path(self.prompt_config_path)
        if not prompt_file.exists():
            # Use default embedded prompt if file doesn't exist
            print(f"⚠️  Prompt config not found: {prompt_file}, using defaults")
            return self._get_default_prompt_config()
        
        with open(prompt_file, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✓ Loaded prompt config: {prompt_file}")
        if 'version_history' in config and config['version_history']:
            latest = config['version_history'][0]
            print(f"  Version: {latest['version']} ({latest['date']})")
        
        return config
    
    def _get_default_prompt_config(self) -> Dict:
        """Get default prompt configuration if file doesn't exist"""
        return {
            'system_prompt': """You are an expert code refactoring assistant.""",
            'output_format': """Return XML format with code and analysis.""",
            'user_message_template': """Analyze and refactor: {code}"""
        }
    
    def _get_mcp_context(self) -> str:
        """Get MCP tools context for system prompt"""
        from config.mcp_catalog import MCP_CATALOG
        
        enabled = self.token_manager.get_enabled_servers()
        
        context = "\n=== Available MCP Tools ===\n"
        context += "You have access to the following tools:\n\n"
        
        for server_id in enabled:
            if server_id not in MCP_CATALOG:
                continue
            
            server = MCP_CATALOG[server_id]
            context += f"**{server['name']}**: {server['description']}\n"
            context += f"  Tools: {', '.join(server['tools'])}\n\n"
        
        return context
    
    def get_system_prompt(self) -> str:
        """Build system prompt from configuration file"""
        system_prompt = self.prompt_config.get('system_prompt', '')
        output_format = self.prompt_config.get('output_format', '')
        
        full_prompt = f"{system_prompt}\n\n{output_format}\n\n{self.mcp_tools}"
        
        return full_prompt
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files in repository (recursively)"""
        print(f"\n🔍 Searching for Python files in: {self.repo_path}")
        print(f"   (Recursively scanning all subdirectories...)")
        
        python_files = []
        
        for path in self.repo_path.rglob("*.py"):
            # Skip common directories
            if any(part.startswith('.') for part in path.parts):
                continue
            if 'venv' in path.parts or 'env' in path.parts:
                continue
            if '__pycache__' in path.parts:
                continue
            
            python_files.append(path)
        
        print(f"   Found {len(python_files)} Python files across all subdirectories")
        
        # Show directory structure
        if python_files:
            dirs = set()
            for f in python_files:
                relative = f.relative_to(self.repo_path)
                if len(relative.parts) > 1:
                    dirs.add(relative.parts[0])
            
            if dirs:
                print(f"   Directories found: {', '.join(sorted(dirs))}")
        
        return python_files
    
    def analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """
        Analyze and refactor a single Python file
        
        Args:
            file_path: Path to Python file
        
        Returns:
            FileAnalysis or None if skipped
        """
        print(f"\n📄 Analyzing: {file_path.relative_to(self.repo_path)}")
        
        try:
            original_code = file_path.read_text()
        except Exception as e:
            print(f"   ⊘ Error reading file: {e}")
            return None
        
        # Skip if file is too small (likely no real code)
        if len(original_code.strip()) < 50:
            print("   ⊘ File too small, skipping")
            return None
        
        # Check if file needs refactoring/documentation
        needs_work = self._needs_refactoring(original_code)
        if not needs_work:
            print("   ✓ File looks good, no changes needed")
            return None
        
        # Use Claude to analyze and refactor
        print("   🤖 Refactoring with Claude...")
        
        # Build user message from template
        user_message_template = self.prompt_config.get('user_message_template', 
            'Analyze and refactor this Python file:\n\nFile: {filename}\n\n```python\n{code}\n```')
        
        user_message = user_message_template.format(
            filename=file_path.name,
            code=original_code
        )
        
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            system=self.get_system_prompt(),
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )
        
        # Parse response
        response_text = response.content[0].text
        
        # Extract code from <refactored_code> tags
        code_match = re.search(r'<refactored_code>(.*?)</refactored_code>', response_text, re.DOTALL)
        if not code_match:
            print("   ⊘ Failed to find <refactored_code> tags")
            print(f"   Response preview: {response_text[:200]}")
            return None
        
        refactored_code = code_match.group(1).strip()
        
        # Extract JSON from <analysis> tags
        analysis_match = re.search(r'<analysis>(.*?)</analysis>', response_text, re.DOTALL)
        if not analysis_match:
            print("   ⊘ Failed to find <analysis> tags")
            return None
        
        analysis_json = analysis_match.group(1).strip()
        
        # Parse JSON
        import json
        try:
            # Clean up any markdown that might still be there
            if analysis_json.startswith('```'):
                lines = analysis_json.split('\n')
                lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                analysis_json = '\n'.join(lines)
            
            result = json.loads(analysis_json)
            result['refactored_code'] = refactored_code
            
        except json.JSONDecodeError as e:
            print(f"   ⊘ Invalid JSON in analysis: {e}")
            print(f"   JSON preview: {analysis_json[:200]}")
            return None
        
        # Calculate changes
        lines_changed = self._count_lines_changed(
            original_code,
            result['refactored_code']
        )
        
        analysis = FileAnalysis(
            file_path=str(file_path.relative_to(self.repo_path)),
            original_code=original_code,
            refactored_code=result['refactored_code'],
            changes_made=result['changes_made'],
            risk_level=RiskLevel(result['risk_level']),
            risk_reasoning=result['risk_reasoning'],
            functions_documented=result.get('functions_documented', 0),
            lines_changed=lines_changed
        )
        
        print(f"   ✓ Risk: {analysis.risk_level.value.upper()}")
        print(f"   ✓ Changes: {len(analysis.changes_made)}")
        print(f"   ✓ Documented: {analysis.functions_documented} functions")
        
        return analysis
    
    def _needs_refactoring(self, code: str) -> bool:
        """Quick check if file needs work"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return True  # Syntax errors need fixing
        
        # Check for missing docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    return True  # Missing docstring
        
        # Check for old-style code patterns
        if 'print ' in code and 'print(' not in code:  # Python 2 print
            return True
        
        return True  # Default to checking
    
    def _count_lines_changed(self, original: str, refactored: str) -> int:
        """Count number of lines changed"""
        original_lines = set(original.split('\n'))
        refactored_lines = set(refactored.split('\n'))
        
        return len(original_lines.symmetric_difference(refactored_lines))
    
    def _group_by_package(self, analyses: List[FileAnalysis]) -> Dict[str, List[FileAnalysis]]:
        """Group files by package/directory"""
        packages = {}
        
        for analysis in analyses:
            path = Path(analysis.file_path)
            
            # Get the top-level directory (package)
            if len(path.parts) > 1:
                package = path.parts[0]
            else:
                package = "root"
            
            if package not in packages:
                packages[package] = []
            
            packages[package].append(analysis)
        
        return packages
    
    def _has_critical_security_issues(self, analyses: List[FileAnalysis]) -> bool:
        """Check if any analysis mentions security issues"""
        # Get security keywords from config
        security_keywords = self.prompt_config.get('security_keywords', [
            'security', 'vulnerability', 'exploit', 'injection', 'xss', 'sql injection'
        ])
        
        for analysis in analyses:
            reasoning_lower = analysis.risk_reasoning.lower()
            for keyword in security_keywords:
                if keyword in reasoning_lower:
                    return True
            
            for change in analysis.changes_made:
                change_lower = change.lower()
                for keyword in security_keywords:
                    if keyword in change_lower:
                        return True
        
        return False
    
    def scan_codebase(self) -> CodebaseAnalysis:
        """
        Scan entire codebase
        
        Returns:
            CodebaseAnalysis with all results
        """
        print("🔍 Scanning codebase...")
        print("=" * 60)
        
        python_files = self.find_python_files()
        print(f"Found {len(python_files)} Python files")
        
        analyses: List[FileAnalysis] = []
        
        for file_path in python_files:
            analysis = self.analyze_file(file_path)
            if analysis:
                analyses.append(analysis)
        
        # Calculate overall risk
        overall_risk = self._calculate_overall_risk(analyses)
        
        # Group by package
        packages = self._group_by_package(analyses)
        
        # Check for critical security issues
        has_critical_security = self._has_critical_security_issues(analyses)
        
        # Generate summary
        summary = self._generate_summary(analyses, overall_risk)
        
        return CodebaseAnalysis(
            files=analyses,
            overall_risk=overall_risk,
            total_files=len(analyses),
            total_changes=sum(len(a.changes_made) for a in analyses),
            summary=summary,
            packages=packages,
            has_critical_security=has_critical_security
        )
    
    def _calculate_overall_risk(self, analyses: List[FileAnalysis]) -> RiskLevel:
        """Calculate overall risk level"""
        if not analyses:
            return RiskLevel.LOW
        
        risk_counts = {
            RiskLevel.HIGH: 0,
            RiskLevel.MEDIUM: 0,
            RiskLevel.LOW: 0
        }
        
        for analysis in analyses:
            risk_counts[analysis.risk_level] += 1
        
        # If any HIGH risk, overall is HIGH
        if risk_counts[RiskLevel.HIGH] > 0:
            return RiskLevel.HIGH
        
        # If >50% MEDIUM, overall is MEDIUM
        if risk_counts[RiskLevel.MEDIUM] > len(analyses) / 2:
            return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
    
    def _generate_summary(self, analyses: List[FileAnalysis], overall_risk: RiskLevel) -> str:
        """Generate summary of changes"""
        if not analyses:
            return "No files needed refactoring"
        
        lines = [
            f"Analyzed {len(analyses)} files",
            f"Overall Risk: {overall_risk.value.upper()}",
            "",
            "Files modified:"
        ]
        
        for analysis in analyses:
            lines.append(f"  • {analysis.file_path} ({analysis.risk_level.value})")
            for change in analysis.changes_made[:2]:  # Show first 2 changes
                lines.append(f"    - {change}")
        
        lines.append("")
        lines.append(f"Total changes: {sum(len(a.changes_made) for a in analyses)}")
        lines.append(f"Functions documented: {sum(a.functions_documented for a in analyses)}")
        
        return '\n'.join(lines)
    
    def apply_changes(self, analysis: CodebaseAnalysis) -> bool:
        """
        Apply refactored code to files
        
        Args:
            analysis: CodebaseAnalysis with changes
        
        Returns:
            True if successful
        """
        print("\n💾 Applying changes...")
        
        for file_analysis in analysis.files:
            file_path = self.repo_path / file_analysis.file_path
            
            try:
                file_path.write_text(file_analysis.refactored_code)
                print(f"   ✓ {file_analysis.file_path}")
            except Exception as e:
                print(f"   ✗ {file_analysis.file_path}: {e}")
                return False
        
        print(f"\n✓ Applied changes to {len(analysis.files)} files")
        return True
    
    def create_github_pr(self, analysis: CodebaseAnalysis, package_name: Optional[str] = None) -> Optional[str]:
        """
        Create GitHub Pull Request using MCP infrastructure
        
        Args:
            analysis: CodebaseAnalysis with all changes
            package_name: Optional package name for package-specific PRs
        
        Returns:
            PR URL if successful, None otherwise
        """
        if package_name:
            print(f"\n📤 Creating GitHub PR for package: {package_name} via MCP...")
        else:
            print("\n📤 Creating GitHub Pull Request via MCP...")
        
        # Check if GitHub is enabled
        if 'github' not in self.token_manager.get_enabled_servers():
            print("   ✗ GitHub not enabled in config")
            return None
        
        # Check for GitHub token
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("   ✗ GITHUB_TOKEN not set")
            return None
        
        # Get repo info
        try:
            owner, repo = self._get_repo_info()
        except Exception as e:
            print(f"   ✗ Failed to get repo info: {e}")
            return None
        
        # Determine branch name and PR details
        if package_name:
            branch_name = f"refactor/{package_name}-improvements"
            pr_title = f"🤖 Refactor {package_name}/ - {analysis.overall_risk.value.upper()} Risk"
        elif analysis.has_critical_security:
            branch_name = "security/critical-fixes"
            pr_title = f"🚨 SECURITY: Critical Security Fixes - {analysis.overall_risk.value.upper()} Risk"
        else:
            branch_name = "refactor/automated-code-improvements"
            pr_title = f"🤖 Automated Code Refactoring - {analysis.overall_risk.value.upper()} Risk"
        
        # Generate commit message and PR body
        commit_message = self._generate_commit_message(analysis, package_name)
        pr_body = self._generate_pr_body(analysis, package_name)
        
        # Get list of changed files
        changed_files = {}
        for file_analysis in analysis.files:
            file_path = str(self.repo_path / file_analysis.file_path)
            changed_files[file_analysis.file_path] = file_analysis.refactored_code
        
        # Use MCP to create PR
        try:
            pr_url = self._create_pr_via_mcp(
                owner=owner,
                repo=repo,
                branch_name=branch_name,
                commit_message=commit_message,
                pr_title=pr_title,
                pr_body=pr_body,
                files=changed_files
            )
            
            if pr_url:
                print(f"   ✓ PR created via MCP: {pr_url}")
                return pr_url
            else:
                print("   ✗ Failed to create PR via MCP")
                return None
        
        except Exception as e:
            print(f"   ✗ MCP error: {e}")
            return None
    
    def _get_repo_info(self) -> tuple:
        """Get repository owner and name using MCP filesystem"""
        try:
            # Try to read .git/config using MCP filesystem
            git_config_path = self.repo_path / ".git" / "config"
            
            if git_config_path.exists():
                # Read git config file
                with open(git_config_path, 'r') as f:
                    git_config = f.read()
                
                # Parse remote URL from config
                # Look for [remote "origin"] section
                import re
                
                # Match: url = https://github.com/owner/repo.git
                # Or: url = git@github.com:owner/repo.git
                url_match = re.search(r'url\s*=\s*(.+)', git_config)
                
                if not url_match:
                    raise ValueError("No remote URL found in .git/config")
                
                remote_url = url_match.group(1).strip()
                
                # Parse owner/repo from URL
                if "github.com/" in remote_url:
                    parts = remote_url.split("github.com/")[1]
                elif "github.com:" in remote_url:
                    parts = remote_url.split("github.com:")[1]
                else:
                    raise ValueError("Not a GitHub repository")
                
                parts = parts.replace(".git", "").strip()
                owner, repo = parts.split("/", 1)
                
                return owner, repo
            else:
                raise ValueError("Not a git repository (no .git/config found)")
        
        except Exception as e:
            # Fallback to asking user
            print(f"   ⚠️  Could not detect repo info automatically: {e}")
            print("   Please provide repository information:")
            
            owner = input("   GitHub username/organization: ").strip()
            repo = input("   Repository name: ").strip()
            
            if not owner or not repo:
                raise Exception("Repository information required")
            
            return owner, repo
    
    def _generate_commit_message(self, analysis: CodebaseAnalysis, package_name: Optional[str] = None) -> str:
        """Generate commit message"""
        if package_name:
            title = f"Refactor {package_name}/ package - {analysis.overall_risk.value.upper()} risk"
        elif analysis.has_critical_security:
            title = f"SECURITY: Critical fixes - {analysis.overall_risk.value.upper()} risk"
        else:
            title = f"Automated code refactoring - {analysis.overall_risk.value.upper()} risk"
        
        message = f"{title}\n\n{analysis.summary}\n\nChanges made:\n"
        for file_analysis in analysis.files:
            for change in file_analysis.changes_made[:3]:
                message += f"- {change}\n"
        
        message += f"\nRisk Assessment: {analysis.overall_risk.value.upper()}\n"
        message += f"Files Modified: {analysis.total_files}\n"
        message += f"Total Changes: {analysis.total_changes}\n"
        
        return message
    
    def _create_pr_via_mcp(
        self,
        owner: str,
        repo: str,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        pr_body: str,
        files: Dict[str, str]
    ) -> Optional[str]:
        """
        Create PR using MCP GitHub server
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch_name: Branch to create
            commit_message: Commit message
            pr_title: PR title
            pr_body: PR description
            files: Dict of {file_path: content}
        
        Returns:
            PR URL if successful
        """
        print("   🔧 Using MCP GitHub server...")
        
        # Step 1: Push files via MCP
        print("   📤 Pushing files via MCP push_files tool...")
        
        push_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "push_files",
                "arguments": {
                    "owner": owner,
                    "repo": repo,
                    "branch": branch_name,
                    "files": [
                        {
                            "path": path,
                            "content": content
                        }
                        for path, content in files.items()
                    ],
                    "message": commit_message
                }
            }
        }
        
        push_result = self._run_mcp_tool("github", push_request)
        
        if not push_result or "error" in push_result:
            error_msg = push_result.get("error", {}).get("message", "Unknown error") if push_result else "No response"
            print(f"   ✗ MCP push_files failed: {error_msg}")
            return None
        
        print("   ✓ Files pushed via MCP")
        
        # Step 2: Create PR via MCP
        print("   📋 Creating PR via MCP create_pull_request tool...")
        
        pr_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "create_pull_request",
                "arguments": {
                    "owner": owner,
                    "repo": repo,
                    "title": pr_title,
                    "body": pr_body,
                    "head": branch_name,
                    "base": "main"
                }
            }
        }
        
        pr_result = self._run_mcp_tool("github", pr_request)
        
        if not pr_result or "error" in pr_result:
            error_msg = pr_result.get("error", {}).get("message", "Unknown error") if pr_result else "No response"
            print(f"   ✗ MCP create_pull_request failed: {error_msg}")
            return None
        
        # Extract PR URL
        result_data = pr_result.get("result", {})
        pr_url = result_data.get("html_url") or result_data.get("url")
        
        if not pr_url:
            print("   ⚠️  PR created but no URL in response")
            print(f"   Response: {result_data}")
        
        return pr_url
    
    def _run_mcp_tool(self, server: str, request: Dict) -> Optional[Dict]:
        """
        Run an MCP tool via Docker
        
        Args:
            server: MCP server name (e.g., 'github')
            request: MCP JSON-RPC request
        
        Returns:
            MCP response dict or None
        """
        import json
        
        # Get environment variables for the server
        env_vars = self.token_manager.get_env_dict()
        
        # Build docker command
        docker_cmd = ["docker", "run", "-i", "--rm"]
        
        # Add environment variables
        for key, value in env_vars.items():
            docker_cmd.extend(["-e", f"{key}={value}"])
        
        # Add volume mount for repository
        docker_cmd.extend(["-v", f"{self.repo_path}:/workspace"])
        
        # Add MCP server image
        docker_cmd.append(f"mcp/{server}")
        
        try:
            # Run MCP server
            result = subprocess.run(
                docker_cmd,
                input=json.dumps(request),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"   ⚠️  Docker command failed: {result.stderr}")
                return None
            
            # Parse response
            response = json.loads(result.stdout)
            return response
        
        except subprocess.TimeoutExpired:
            print("   ✗ MCP tool timed out")
            return None
        except json.JSONDecodeError as e:
            print(f"   ✗ Invalid MCP response: {e}")
            print(f"   Output: {result.stdout[:200]}")
            return None
        except Exception as e:
            print(f"   ✗ MCP tool error: {e}")
            return None
    
    def _generate_pr_body(self, analysis: CodebaseAnalysis, package_name: Optional[str] = None) -> str:
        """Generate GitHub PR body"""
        if package_name:
            body = f"""## 🤖 Automated Refactoring - Package: {package_name}/

### Risk Assessment: {analysis.overall_risk.value.upper()}

This PR contains automated code improvements for the `{package_name}/` package.
"""
        elif analysis.has_critical_security:
            body = f"""## 🚨 CRITICAL SECURITY FIXES

### Risk Assessment: {analysis.overall_risk.value.upper()}

⚠️ **This PR addresses critical security vulnerabilities detected in the codebase.**

"""
        else:
            body = f"""## 🤖 Automated Code Refactoring

### Risk Assessment: {analysis.overall_risk.value.upper()}

This PR contains automated code improvements generated by an AI-powered codebase scanner.

"""
        
        body += f"""
### Summary
{analysis.summary}

### Files Modified ({analysis.total_files})
"""
        
        for file_analysis in analysis.files:
            body += f"\n#### `{file_analysis.file_path}` - {file_analysis.risk_level.value.upper()} Risk\n"
            body += f"**Reasoning:** {file_analysis.risk_reasoning}\n\n"
            body += "**Changes:**\n"
            for change in file_analysis.changes_made:
                body += f"- {change}\n"
            body += "\n"
        
        body += f"""
### Statistics
- **Total Changes:** {analysis.total_changes}
- **Functions Documented:** {sum(f.functions_documented for f in analysis.files)}
- **Lines Changed:** {sum(f.lines_changed for f in analysis.files)}

### Review Guidelines
"""
        
        if analysis.overall_risk == RiskLevel.HIGH:
            body += "⚠️ **HIGH RISK** - Careful review required. Significant logic changes made.\n"
        elif analysis.overall_risk == RiskLevel.MEDIUM:
            body += "⚡ **MEDIUM RISK** - Standard review recommended. Syntax and minor logic updates.\n"
        else:
            body += "✅ **LOW RISK** - Quick review sufficient. Mostly documentation and minor updates.\n"
        
        body += "\n---\n*Generated by Codebase Scanner with MCP Integration*"
        
        return body
    


def main():
    """Main entry point"""
    import sys
    
    # Get repo path from command line arg or default to /workspace
    if len(sys.argv) >= 2:
        repo_path = sys.argv[1]
    else:
        # Default to /workspace (Docker mount point)
        repo_path = "/workspace"
        if not os.path.exists(repo_path):
            print("Usage: python scanner.py <repo_path>")
            print("Or: docker-compose run scanner (scans /workspace)")
            print("Or: REPO_PATH=/your/repo docker-compose run scanner")
            sys.exit(1)
    
    try:
        # Initialize scanner
        scanner = CodebaseScanner(repo_path)
        
        # Scan codebase
        analysis = scanner.scan_codebase()
        
        print("\n" + "=" * 60)
        print("📊 SCAN COMPLETE")
        print("=" * 60)
        print(f"\nOverall Risk: {analysis.overall_risk.value.upper()}")
        print(f"Files Modified: {analysis.total_files}")
        print(f"Total Changes: {analysis.total_changes}")
        
        if analysis.has_critical_security:
            print("\n🚨 CRITICAL: Security issues detected!")
        
        if analysis.total_files == 0:
            print("\n✨ Codebase looks good! No changes needed.")
            return
        
        # Show detailed summary
        print("\n" + "=" * 60)
        print("📋 REFACTORING SUMMARY")
        print("=" * 60)
        
        if analysis.packages:
            print(f"\n📦 Changes grouped by package:")
            for package, files in analysis.packages.items():
                risk_levels = [f.risk_level.value for f in files]
                highest_risk = max(risk_levels, key=lambda x: ['low', 'medium', 'high'].index(x))
                print(f"\n  📁 {package}/ ({len(files)} files, {highest_risk.upper()} risk)")
                for file_analysis in files:
                    print(f"     • {Path(file_analysis.file_path).name} - {file_analysis.risk_level.value}")
                    # Show first 2 changes
                    for change in file_analysis.changes_made[:2]:
                        print(f"       - {change}")
                    if len(file_analysis.changes_made) > 2:
                        print(f"       ... and {len(file_analysis.changes_made) - 2} more changes")
        
        print("\n" + "=" * 60)
        
        # Decide PR strategy
        if analysis.has_critical_security:
            print("\n🚨 SECURITY ISSUE DETECTED")
            print("   Creating ONE PR with all security fixes...")
            pr_strategy = "single"
        elif len(analysis.packages) > 1:
            print(f"\n📦 Multiple packages detected ({len(analysis.packages)})")
            strategy = input("   Create PR per package or one combined PR? (per-package/combined): ").strip().lower()
            pr_strategy = "per-package" if strategy == "per-package" else "single"
        else:
            pr_strategy = "single"
        
        # Offer to create PR(s)
        create_pr = input(f"\n📤 Create GitHub PR(s)? (y/N): ").strip().lower()
        
        if create_pr == 'y':
            # Apply changes first (required for PR)
            print("\n💾 Applying changes to files...")
            if scanner.apply_changes(analysis):
                if pr_strategy == "per-package" and len(analysis.packages) > 1:
                    # Create PR per package
                    for package, files in analysis.packages.items():
                        print(f"\n📤 Creating PR for package: {package}")
                        package_analysis = CodebaseAnalysis(
                            files=files,
                            overall_risk=scanner._calculate_overall_risk(files),
                            total_files=len(files),
                            total_changes=sum(len(f.changes_made) for f in files),
                            summary=f"Refactoring for {package}/ package",
                            packages={package: files},
                            has_critical_security=False
                        )
                        scanner.create_github_pr(package_analysis, package_name=package)
                else:
                    # Single PR for everything
                    scanner.create_github_pr(analysis)
        else:
            print("\n✨ Scan complete. No changes applied.")
        
        print("\n✅ Done!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()