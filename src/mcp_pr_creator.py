"""
MCP-Based GitHub PR Creator
Uses GitHub MCP server tools instead of direct git/API calls
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List


class MCPGitHubPRCreator:
    """
    Creates GitHub PRs using MCP infrastructure
    """
    
    def __init__(self, repo_path: str, github_token: str):
        """
        Initialize PR creator
        
        Args:
            repo_path: Path to repository
            github_token: GitHub token for authentication
        """
        self.repo_path = Path(repo_path)
        self.github_token = github_token
    
    def _run_mcp_tool(self, server: str, tool: str, params: Dict) -> Dict:
        """
        Run an MCP tool via Docker
        
        Args:
            server: MCP server name (e.g., 'github', 'git')
            tool: Tool name (e.g., 'create_pull_request')
            params: Tool parameters as dict
        
        Returns:
            Tool response as dict
        """
        # Build MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool,
                "arguments": params
            }
        }
        
        # Run MCP server via Docker
        docker_cmd = [
            "docker", "run", "-i", "--rm",
            "-e", f"GITHUB_TOKEN={self.github_token}",
            "-v", f"{self.repo_path}:/workspace",
            f"mcp/{server}"
        ]
        
        try:
            result = subprocess.run(
                docker_cmd,
                input=json.dumps(mcp_request),
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse MCP response
            response = json.loads(result.stdout)
            
            if "error" in response:
                raise Exception(f"MCP error: {response['error']}")
            
            return response.get("result", {})
        
        except subprocess.CalledProcessError as e:
            raise Exception(f"Docker command failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid MCP response: {e}")
    
    def get_repo_info(self) -> tuple[str, str]:
        """
        Get repository owner and name from git remote
        
        Returns:
            Tuple of (owner, repo_name)
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True
            )
            
            remote_url = result.stdout.strip()
            
            # Parse owner/repo from URL
            # Supports: https://github.com/owner/repo.git and git@github.com:owner/repo.git
            if "github.com/" in remote_url:
                parts = remote_url.split("github.com/")[1]
            elif "github.com:" in remote_url:
                parts = remote_url.split("github.com:")[1]
            else:
                raise ValueError("Not a GitHub repository")
            
            # Remove .git suffix
            parts = parts.replace(".git", "")
            owner, repo = parts.split("/", 1)
            
            return owner, repo
        
        except Exception as e:
            raise Exception(f"Failed to get repo info: {e}")
    
    def create_branch_and_commit(self, branch_name: str, commit_message: str, files: List[str]) -> bool:
        """
        Create branch and commit changes using git MCP server
        
        Args:
            branch_name: Name of new branch
            commit_message: Commit message
            files: List of file paths to commit
        
        Returns:
            True if successful
        """
        print(f"   📝 Creating branch: {branch_name}")
        
        # Use git commands directly (MCP git server is for operations, not branching)
        try:
            # Create and checkout branch
            subprocess.run(
                ["git", "-C", str(self.repo_path), "checkout", "-b", branch_name],
                capture_output=True,
                check=True
            )
            
            # Stage files
            subprocess.run(
                ["git", "-C", str(self.repo_path), "add"] + files,
                capture_output=True,
                check=True
            )
            
            # Commit using git MCP server
            print("   💾 Committing changes via MCP...")
            
            # For now, use direct git (MCP git server is more for status/diff)
            subprocess.run(
                ["git", "-C", str(self.repo_path), "commit", "-m", commit_message],
                capture_output=True,
                check=True
            )
            
            print("   ✓ Changes committed")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Git operation failed: {e.stderr.decode()}")
            return False
    
    def push_branch(self, branch_name: str) -> bool:
        """
        Push branch to remote using GitHub MCP push_files tool
        
        Args:
            branch_name: Branch name to push
        
        Returns:
            True if successful
        """
        print(f"   📤 Pushing branch: {branch_name}")
        
        try:
            # Get repo info
            owner, repo = self.get_repo_info()
            
            # Use GitHub MCP push_files tool
            result = self._run_mcp_tool(
                server="github",
                tool="push_files",
                params={
                    "owner": owner,
                    "repo": repo,
                    "branch": branch_name,
                    "files": "*"  # Push all changed files
                }
            )
            
            print("   ✓ Branch pushed via MCP")
            return True
        
        except Exception as e:
            # Fallback to direct git push
            print(f"   ⚠️  MCP push failed ({e}), using git push...")
            try:
                subprocess.run(
                    ["git", "-C", str(self.repo_path), "push", "-u", "origin", branch_name],
                    capture_output=True,
                    check=True
                )
                print("   ✓ Branch pushed via git")
                return True
            except subprocess.CalledProcessError as e:
                print(f"   ✗ Push failed: {e.stderr.decode()}")
                return False
    
    def create_pull_request(
        self, 
        branch_name: str,
        title: str,
        body: str,
        base_branch: str = "main"
    ) -> Optional[str]:
        """
        Create pull request using GitHub MCP server
        
        Args:
            branch_name: Source branch name
            title: PR title
            body: PR body (description)
            base_branch: Target branch (default: main)
        
        Returns:
            PR URL if successful, None otherwise
        """
        print(f"   📋 Creating PR via MCP GitHub server...")
        
        try:
            # Get repo info
            owner, repo = self.get_repo_info()
            
            # Use GitHub MCP create_pull_request tool
            result = self._run_mcp_tool(
                server="github",
                tool="create_pull_request",
                params={
                    "owner": owner,
                    "repo": repo,
                    "title": title,
                    "body": body,
                    "head": branch_name,
                    "base": base_branch
                }
            )
            
            # Extract PR URL from result
            pr_url = result.get("html_url") or result.get("url")
            
            if pr_url:
                print(f"   ✓ PR created via MCP: {pr_url}")
                return pr_url
            else:
                print(f"   ⚠️  PR created but no URL in response")
                return None
        
        except Exception as e:
            print(f"   ✗ MCP PR creation failed: {e}")
            return None
    
    def create_pr_workflow(
        self,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        pr_body: str,
        files: List[str],
        base_branch: str = "main"
    ) -> Optional[str]:
        """
        Complete workflow: create branch, commit, push, create PR
        
        Args:
            branch_name: New branch name
            commit_message: Commit message
            pr_title: PR title
            pr_body: PR description
            files: Files to commit
            base_branch: Target branch
        
        Returns:
            PR URL if successful
        """
        print(f"\n🔧 Creating PR using MCP infrastructure...")
        
        # Step 1: Create branch and commit
        if not self.create_branch_and_commit(branch_name, commit_message, files):
            return None
        
        # Step 2: Push branch
        if not self.push_branch(branch_name):
            return None
        
        # Step 3: Create PR
        pr_url = self.create_pull_request(branch_name, pr_title, pr_body, base_branch)
        
        if pr_url:
            print(f"\n✅ PR created successfully via MCP!")
            return pr_url
        else:
            print(f"\n⚠️  PR creation failed")
            return None


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mcp_pr_creator.py <repo_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("Error: GITHUB_TOKEN not set")
        sys.exit(1)
    
    creator = MCPGitHubPRCreator(repo_path, github_token)
    
    # Example PR creation
    pr_url = creator.create_pr_workflow(
        branch_name="feature/test-mcp-pr",
        commit_message="Test commit via MCP",
        pr_title="🤖 Test PR via MCP",
        pr_body="This PR was created using MCP infrastructure!",
        files=["."],  # All files
        base_branch="main"
    )
    
    if pr_url:
        print(f"Success! {pr_url}")
    else:
        print("Failed to create PR")
