"""
Comprehensive MCP Server Catalog
Auto-generated from Docker Hub mcp/ namespace
Source: https://hub.docker.com/mcp/explore
"""

MCP_CATALOG = {
    # === Development & Version Control ===
    "github": {
        "name": "GitHub Official",
        "description": "Official GitHub MCP server for repository management, issues, PRs",
        "image": "mcp/github",
        "category": "development",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "GITHUB_TOKEN",
        "tools": ["create_repository", "create_issue", "create_pull_request", "search_repositories", "get_file_contents", "push_files"],
        "docker_run": "docker run -i --rm -e GITHUB_TOKEN mcp/github"
    },
    "gitlab": {
        "name": "GitLab",
        "description": "GitLab API integration for project management",
        "image": "mcp/gitlab",
        "category": "development",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "GITLAB_TOKEN",
        "tools": ["create_project", "create_issue", "create_merge_request"],
        "docker_run": "docker run -i --rm -e GITLAB_TOKEN mcp/gitlab"
    },
    "git": {
        "name": "Git Operations",
        "description": "Local Git repository operations",
        "image": "mcp/git",
        "category": "development",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["git_status", "git_commit", "git_push", "git_diff"],
        "docker_run": "docker run -i --rm -v $(pwd):/repo mcp/git"
    },
    
    # === Documentation & Code Intelligence ===
    "context7": {
        "name": "Context7",
        "description": "Up-to-date code documentation for LLMs and AI code editors",
        "image": "mcp/context7",
        "category": "documentation",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["get-library-docs", "resolve-library-id"],
        "docker_run": "docker run -i --rm mcp/context7"
    },
    "gemini-docs": {
        "name": "Google Gemini Docs",
        "description": "Search and retrieve Google Gemini API documentation",
        "image": "mcp/gemini-docs",
        "category": "documentation",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["search_docs", "get_doc"],
        "docker_run": "docker run -i --rm mcp/gemini-docs"
    },
    "astro-docs": {
        "name": "Astro Documentation",
        "description": "Access Astro web framework documentation, guides, and API references",
        "image": "mcp/astro-docs",
        "category": "documentation",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["search_astro_docs", "get_guide"],
        "docker_run": "docker run -i --rm mcp/astro-docs"
    },
    
    # === AI & Problem Solving ===
    "sequential-thinking": {
        "name": "Sequential Thinking",
        "description": "Dynamic problem-solving through thought sequences",
        "image": "mcp/sequential-thinking",
        "category": "ai",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["sequentialthinking"],
        "docker_run": "docker run -i --rm mcp/sequential-thinking"
    },
    
    # === Web & Scraping ===
    "firecrawl": {
        "name": "Firecrawl",
        "description": "Web scraping, crawling, and screenshot capabilities",
        "image": "mcp/firecrawl",
        "category": "web",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "FIRECRAWL_API_KEY",
        "tools": ["firecrawl_scrape", "firecrawl_crawl", "firecrawl_search", "firecrawl_screenshot"],
        "docker_run": "docker run -i --rm -e FIRECRAWL_API_KEY mcp/firecrawl"
    },
    "puppeteer": {
        "name": "Puppeteer",
        "description": "Browser automation for screenshots and web interaction",
        "image": "mcp/puppeteer",
        "category": "web",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["puppeteer_navigate", "puppeteer_screenshot", "puppeteer_click", "puppeteer_fill"],
        "docker_run": "docker run -i --rm mcp/puppeteer"
    },
    "apify": {
        "name": "Apify",
        "description": "Web scraping marketplace - extract data from any website",
        "image": "mcp/apify",
        "category": "web",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "APIFY_API_TOKEN",
        "tools": ["run_actor", "get_dataset", "scrape_url"],
        "docker_run": "docker run -i --rm -e APIFY_API_TOKEN mcp/apify"
    },
    "brave": {
        "name": "Brave Search",
        "description": "Search the web using Brave Search API",
        "image": "mcp/brave",
        "category": "web",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "BRAVE_API_KEY",
        "tools": ["brave_web_search", "brave_local_search"],
        "docker_run": "docker run -i --rm -e BRAVE_API_KEY mcp/brave"
    },
    
    # === Databases ===
    "postgres": {
        "name": "PostgreSQL",
        "description": "Query and manage PostgreSQL databases",
        "image": "mcp/postgres",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "POSTGRES_URI",
        "tools": ["query", "list_tables", "describe_table", "execute"],
        "docker_run": "docker run -i --rm -e POSTGRES_URI mcp/postgres"
    },
    "mongodb": {
        "name": "MongoDB",
        "description": "Connect to MongoDB databases and MongoDB Atlas",
        "image": "mcp/mongodb",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "MONGODB_URI",
        "tools": ["find", "insert", "update", "delete", "aggregate"],
        "docker_run": "docker run -i --rm -e MONGODB_URI mcp/mongodb"
    },
    "sqlite": {
        "name": "SQLite",
        "description": "Advanced SQLite with analytics, text search, and geospatial",
        "image": "mcp/sqlite",
        "category": "database",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["read_query", "write_query", "list_tables", "create_table"],
        "docker_run": "docker run -i --rm -v $(pwd):/data mcp/sqlite"
    },
    "mysql": {
        "name": "MySQL",
        "description": "MySQL database operations",
        "image": "mcp/mysql",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "MYSQL_URI",
        "tools": ["query", "execute", "list_tables"],
        "docker_run": "docker run -i --rm -e MYSQL_URI mcp/mysql"
    },
    "redis": {
        "name": "Redis",
        "description": "Redis key-value store operations",
        "image": "mcp/redis",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "REDIS_URI",
        "tools": ["get", "set", "del", "keys", "exists"],
        "docker_run": "docker run -i --rm -e REDIS_URI mcp/redis"
    },
    "elasticsearch": {
        "name": "Elasticsearch",
        "description": "Interact with Elasticsearch indices",
        "image": "mcp/elasticsearch",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "ELASTICSEARCH_URL",
        "tools": ["search", "index", "delete", "bulk"],
        "docker_run": "docker run -i --rm -e ELASTICSEARCH_URL mcp/elasticsearch"
    },
    "couchbase": {
        "name": "Couchbase",
        "description": "Distributed document database with search engine",
        "image": "mcp/couchbase",
        "category": "database",
        "requires_auth": True,
        "auth_type": "connection_string",
        "env_var": "COUCHBASE_URI",
        "tools": ["query", "get", "upsert", "delete"],
        "docker_run": "docker run -i --rm -e COUCHBASE_URI mcp/couchbase"
    },
    "neon": {
        "name": "Neon",
        "description": "Neon serverless Postgres management and databases",
        "image": "mcp/neon",
        "category": "database",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "NEON_API_KEY",
        "tools": ["create_database", "query", "list_databases"],
        "docker_run": "docker run -i --rm -e NEON_API_KEY mcp/neon"
    },
    
    # === Cloud Services ===
    "aws": {
        "name": "AWS",
        "description": "AWS CLI commands for managing AWS infrastructure",
        "image": "mcp/aws",
        "category": "cloud",
        "requires_auth": True,
        "auth_type": "credentials",
        "env_var": "AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY",
        "tools": ["aws_cli", "list_buckets", "describe_instances"],
        "docker_run": "docker run -i --rm -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY mcp/aws"
    },
    "azure": {
        "name": "Azure AKS",
        "description": "Azure Kubernetes Service official MCP server",
        "image": "mcp/azure-aks",
        "category": "cloud",
        "requires_auth": True,
        "auth_type": "credentials",
        "env_var": "AZURE_TENANT_ID,AZURE_CLIENT_ID,AZURE_CLIENT_SECRET",
        "tools": ["list_clusters", "get_cluster", "create_cluster"],
        "docker_run": "docker run -i --rm -e AZURE_TENANT_ID -e AZURE_CLIENT_ID -e AZURE_CLIENT_SECRET mcp/azure-aks"
    },
    "gcp": {
        "name": "Google Cloud",
        "description": "Google Cloud Platform operations",
        "image": "mcp/gcp",
        "category": "cloud",
        "requires_auth": True,
        "auth_type": "credentials",
        "env_var": "GOOGLE_APPLICATION_CREDENTIALS",
        "tools": ["gcloud_command", "list_instances", "create_bucket"],
        "docker_run": "docker run -i --rm -e GOOGLE_APPLICATION_CREDENTIALS mcp/gcp"
    },
    "heroku": {
        "name": "Heroku",
        "description": "Heroku Platform using Heroku CLI",
        "image": "mcp/heroku",
        "category": "cloud",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "HEROKU_API_KEY",
        "tools": ["list_apps", "create_app", "deploy"],
        "docker_run": "docker run -i --rm -e HEROKU_API_KEY mcp/heroku"
    },
    
    # === Container & DevOps ===
    "dockerhub": {
        "name": "Docker Hub",
        "description": "Search images and manage Docker Hub repositories",
        "image": "mcp/dockerhub",
        "category": "devops",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "HUB_PAT_TOKEN",
        "tools": ["search_images", "get_repository", "list_namespaces", "create_repository"],
        "docker_run": "docker run -i --rm -e HUB_PAT_TOKEN mcp/dockerhub"
    },
    "grafana": {
        "name": "Grafana",
        "description": "MCP server for Grafana monitoring and dashboards",
        "image": "mcp/grafana",
        "category": "devops",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "GRAFANA_API_KEY",
        "tools": ["create_dashboard", "query_metrics", "list_dashboards"],
        "docker_run": "docker run -i --rm -e GRAFANA_API_KEY mcp/grafana"
    },
    
    # === Payment & Commerce ===
    "stripe": {
        "name": "Stripe",
        "description": "Interact with Stripe payment services",
        "image": "mcp/stripe",
        "category": "payment",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "STRIPE_API_KEY",
        "tools": ["create_customer", "create_payment_intent", "list_payments", "refund"],
        "docker_run": "docker run -i --rm -e STRIPE_API_KEY mcp/stripe"
    },
    
    # === Productivity & Collaboration ===
    "notion": {
        "name": "Notion Official",
        "description": "Official Notion MCP server for workspace management",
        "image": "mcp/notion",
        "category": "productivity",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "NOTION_API_KEY",
        "tools": ["create_page", "search", "update_page", "query_database"],
        "docker_run": "docker run -i --rm -e NOTION_API_KEY mcp/notion"
    },
    "slack": {
        "name": "Slack",
        "description": "Slack workspace integration",
        "image": "mcp/slack",
        "category": "productivity",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "SLACK_BOT_TOKEN",
        "tools": ["send_message", "list_channels", "create_channel"],
        "docker_run": "docker run -i --rm -e SLACK_BOT_TOKEN mcp/slack"
    },
    "linear": {
        "name": "Linear",
        "description": "Linear issue tracking and project management",
        "image": "mcp/linear",
        "category": "productivity",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "LINEAR_API_KEY",
        "tools": ["create_issue", "update_issue", "list_issues"],
        "docker_run": "docker run -i --rm -e LINEAR_API_KEY mcp/linear"
    },
    
    # === Data & Analytics ===
    "arxiv": {
        "name": "ArXiv",
        "description": "Search arXiv papers, download and analyze research",
        "image": "mcp/arxiv",
        "category": "research",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["search_papers", "download_paper", "get_paper_details"],
        "docker_run": "docker run -i --rm mcp/arxiv"
    },
    "astra": {
        "name": "Astra DB",
        "description": "DataStax Astra DB workloads",
        "image": "mcp/astra",
        "category": "database",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "ASTRA_DB_TOKEN",
        "tools": ["query", "insert", "update", "delete"],
        "docker_run": "docker run -i --rm -e ASTRA_DB_TOKEN mcp/astra"
    },
    "atlan": {
        "name": "Atlan",
        "description": "Data governance and discovery - asset search, updates, lineage",
        "image": "mcp/atlan",
        "category": "data",
        "requires_auth": True,
        "auth_type": "api_key",
        "env_var": "ATLAN_API_KEY",
        "tools": ["search_assets", "update_asset", "get_lineage"],
        "docker_run": "docker run -i --rm -e ATLAN_API_KEY mcp/atlan"
    },
    
    # === IoT & Monitoring ===
    "thingsboard": {
        "name": "ThingsBoard",
        "description": "IoT platform - query telemetry, manage devices and assets",
        "image": "mcp/thingsboard",
        "category": "iot",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "THINGSBOARD_TOKEN",
        "tools": ["query_telemetry", "create_device", "list_assets"],
        "docker_run": "docker run -i --rm -e THINGSBOARD_TOKEN mcp/thingsboard"
    },
    "victoriametrics": {
        "name": "VictoriaMetrics",
        "description": "VictoriaMetrics monitoring and observability",
        "image": "mcp/victoriametrics",
        "category": "monitoring",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "VM_TOKEN",
        "tools": ["query_metrics", "list_metrics", "write_metrics"],
        "docker_run": "docker run -i --rm -e VM_TOKEN mcp/victoriametrics"
    },
    "victorialogs": {
        "name": "VictoriaLogs",
        "description": "VictoriaLogs instance for logs and observability",
        "image": "mcp/victorialogs",
        "category": "monitoring",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "VL_TOKEN",
        "tools": ["query_logs", "write_logs", "list_streams"],
        "docker_run": "docker run -i --rm -e VL_TOKEN mcp/victorialogs"
    },
    "victoriatraces": {
        "name": "VictoriaTraces",
        "description": "VictoriaTraces for tracing and debugging",
        "image": "mcp/victoriatraces",
        "category": "monitoring",
        "requires_auth": True,
        "auth_type": "token",
        "env_var": "VT_TOKEN",
        "tools": ["query_traces", "write_trace", "get_trace"],
        "docker_run": "docker run -i --rm -e VT_TOKEN mcp/victoriatraces"
    },
    
    # === File & System ===
    "filesystem": {
        "name": "Filesystem",
        "description": "Search, update, manage files and run terminal commands",
        "image": "mcp/filesystem",
        "category": "system",
        "requires_auth": False,
        "auth_type": "none",
        "tools": ["read_file", "write_file", "list_directory", "search_files", "run_command"],
        "docker_run": "docker run -i --rm -v $(pwd):/workspace mcp/filesystem"
    }
}

# Category definitions
CATEGORIES = {
    "development": "Version control, Git, and development tools",
    "documentation": "Code documentation and API references",
    "ai": "AI and machine learning tools",
    "web": "Web scraping, crawling, and browser automation",
    "database": "Database management and queries",
    "cloud": "Cloud platform services (AWS, Azure, GCP)",
    "devops": "DevOps, monitoring, and CI/CD tools",
    "payment": "Payment processing and commerce",
    "productivity": "Collaboration and productivity tools",
    "research": "Research papers and academic resources",
    "data": "Data governance and analytics",
    "iot": "Internet of Things and device management",
    "monitoring": "System monitoring and observability",
    "system": "Filesystem and system operations"
}

def get_servers_by_category(category: str):
    """Get all servers in a category"""
    return {k: v for k, v in MCP_CATALOG.items() if v["category"] == category}

def get_servers_requiring_auth():
    """Get all servers that require authentication"""
    return {k: v for k, v in MCP_CATALOG.items() if v["requires_auth"]}

def get_servers_no_auth():
    """Get all servers that don't require authentication"""
    return {k: v for k, v in MCP_CATALOG.items() if not v["requires_auth"]}
