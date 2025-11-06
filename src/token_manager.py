"""
Smart Token Management System
Only prompts for tokens that are:
1. Enabled in config
2. Require authentication
3. Not already set in environment
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml

from config.mcp_catalog import MCP_CATALOG


class TokenManager:
    """
    Manages authentication tokens for MCP servers
    Intelligently prompts only for required missing tokens
    """
    
    def __init__(self, config_path: str = "mcp_config.yaml"):
        """Initialize token manager with config"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.env_file = Path(".env")
        self.missing_tokens: Dict[str, str] = {}
    
    def _load_config(self) -> Dict:
        """Load MCP configuration"""
        if not self.config_path.exists():
            print(f"⚠️  Config file not found: {self.config_path}")
            print("Creating default config...")
            self._create_default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _create_default_config(self):
        """Create default config with some common servers"""
        default_config = {
            'servers': {
                'github': {'enabled': True},
                'context7': {'enabled': True},
                'sequential-thinking': {'enabled': True},
                'filesystem': {'enabled': True}
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
    
    def get_enabled_servers(self) -> List[str]:
        """Get list of enabled server IDs"""
        if 'servers' not in self.config:
            return []
        
        enabled = []
        for server_id, config in self.config['servers'].items():
            if isinstance(config, dict) and config.get('enabled', False):
                enabled.append(server_id)
            elif config is True:
                enabled.append(server_id)
        
        return enabled
    
    def check_tokens(self) -> Dict[str, List[str]]:
        """
        Check which tokens are needed
        
        Returns:
            Dict with:
                'missing': List of servers needing tokens
                'present': List of servers with tokens already set
                'not_needed': List of servers not needing tokens
        """
        enabled = self.get_enabled_servers()
        
        result = {
            'missing': [],
            'present': [],
            'not_needed': []
        }
        
        for server_id in enabled:
            if server_id not in MCP_CATALOG:
                print(f"⚠️  Warning: {server_id} not in catalog")
                continue
            
            server = MCP_CATALOG[server_id]
            
            if not server['requires_auth']:
                result['not_needed'].append(server_id)
                continue
            
            # Check if token(s) already set
            env_vars = server['env_var'].split(',')
            all_present = all(os.getenv(var.strip()) for var in env_vars)
            
            if all_present:
                result['present'].append(server_id)
            else:
                result['missing'].append(server_id)
        
        return result
    
    def prompt_for_tokens(self, interactive: bool = True) -> bool:
        """
        Prompt user for missing tokens
        
        Args:
            interactive: If False, just report missing tokens without prompting
        
        Returns:
            True if all tokens obtained, False otherwise
        """
        status = self.check_tokens()
        
        # Report status
        if status['present']:
            print(f"\n✅ Tokens already set for: {', '.join(status['present'])}")
        
        if status['not_needed']:
            print(f"ℹ️  No auth needed for: {', '.join(status['not_needed'])}")
        
        if not status['missing']:
            print("\n✨ All required tokens are set!")
            return True
        
        print(f"\n⚠️  Missing tokens for: {', '.join(status['missing'])}")
        
        if not interactive:
            print("\n💡 Set these environment variables:")
            for server_id in status['missing']:
                server = MCP_CATALOG[server_id]
                print(f"   export {server['env_var']}=<your_token>")
            return False
        
        # Interactive prompting
        print("\n🔐 Token Setup")
        print("=" * 60)
        
        for server_id in status['missing']:
            server = MCP_CATALOG[server_id]
            print(f"\n📦 {server['name']}")
            print(f"   {server['description']}")
            print(f"   Auth type: {server['auth_type']}")
            
            env_vars = server['env_var'].split(',')
            
            for env_var in env_vars:
                env_var = env_var.strip()
                
                # Prompt for token
                token = input(f"\n   Enter {env_var} (or press Enter to skip): ").strip()
                
                if token:
                    self.missing_tokens[env_var] = token
                    # Set in current environment
                    os.environ[env_var] = token
                    print(f"   ✓ {env_var} set")
                else:
                    print(f"   ⊘ {env_var} skipped")
        
        # Offer to save to .env
        if self.missing_tokens:
            save = input(f"\n💾 Save tokens to {self.env_file}? (y/N): ").strip().lower()
            if save == 'y':
                self._save_to_env_file()
        
        # Check if all required tokens now set
        final_status = self.check_tokens()
        if final_status['missing']:
            print(f"\n⚠️  Still missing: {', '.join(final_status['missing'])}")
            print("   Some MCP servers may not work correctly")
            return False
        
        return True
    
    def _save_to_env_file(self):
        """Save tokens to .env file"""
        # Read existing .env if present
        existing = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing[key] = value
        
        # Merge with new tokens
        existing.update(self.missing_tokens)
        
        # Write back
        with open(self.env_file, 'w') as f:
            f.write("# MCP Server Tokens\n")
            f.write("# Generated by Token Manager\n\n")
            for key, value in existing.items():
                f.write(f"{key}={value}\n")
        
        print(f"✓ Tokens saved to {self.env_file}")
        print(f"  Load with: source {self.env_file}")
    
    def load_from_env_file(self):
        """Load tokens from .env file"""
        if not self.env_file.exists():
            return
        
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    def validate_setup(self) -> bool:
        """
        Validate that all enabled servers can work
        
        Returns:
            True if setup is valid
        """
        status = self.check_tokens()
        
        if status['missing']:
            print("\n❌ Setup incomplete!")
            print(f"   Missing tokens for: {', '.join(status['missing'])}")
            return False
        
        print("\n✅ Setup validated!")
        print(f"   {len(status['present']) + len(status['not_needed'])} servers ready")
        return True
    
    def get_env_dict(self) -> Dict[str, str]:
        """Get dict of all environment variables for enabled servers"""
        enabled = self.get_enabled_servers()
        env_dict = {}
        
        for server_id in enabled:
            if server_id not in MCP_CATALOG:
                continue
            
            server = MCP_CATALOG[server_id]
            if not server['requires_auth']:
                continue
            
            env_vars = server['env_var'].split(',')
            for env_var in env_vars:
                env_var = env_var.strip()
                value = os.getenv(env_var)
                if value:
                    env_dict[env_var] = value
        
        return env_dict


def setup_tokens(config_path: str = "mcp_config.yaml", interactive: bool = True) -> TokenManager:
    """
    Convenience function to setup tokens
    
    Args:
        config_path: Path to config file
        interactive: Whether to prompt for tokens
    
    Returns:
        TokenManager instance
    """
    manager = TokenManager(config_path)
    
    # Try to load from .env first
    manager.load_from_env_file()
    
    # Prompt for any missing tokens
    manager.prompt_for_tokens(interactive=interactive)
    
    return manager


if __name__ == "__main__":
    # Test the token manager
    print("🔐 MCP Token Manager\n")
    
    manager = setup_tokens(interactive=True)
    
    if manager.validate_setup():
        print("\n🎉 Ready to use MCP servers!")
    else:
        print("\n⚠️  Some servers may not work without tokens")
