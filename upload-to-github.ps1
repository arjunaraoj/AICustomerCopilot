# upload-to-github.ps1
# Complete script to upload AI Customer Copilot project to GitHub

param(
    [string]$RepoName = "ai-customer-copilot-singapore",
    [string]$Description = "AI Customer Copilot - Multi-Agent LLM System for Singapore Tourism Board. Provides intelligent assistance for attractions, dining, shopping, and promotions.",
    [string]$GitHubUsername = "arjunaraoj"
)

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "="*70
Write-ColorOutput Green "🚀 GitHub Upload Script - AI Customer Copilot"
Write-ColorOutput Green "="*70

# Step 1: Check if git is installed
Write-ColorOutput Yellow "`n📌 Step 1: Checking Git installation..."
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "❌ Git is not installed. Please install Git from https://git-scm.com/"
    Write-ColorOutput Yellow "Press any key to open Git download page..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Start-Process "https://git-scm.com/download/win"
    exit 1
}
Write-ColorOutput Green "✅ Git is installed"

# Step 2: Initialize git repository
Write-ColorOutput Yellow "`n📌 Step 2: Initializing Git repository..."
if (Test-Path ".git") {
    Write-ColorOutput Yellow "⚠️  Git repository already exists. Removing old one..."
    Remove-Item -Recurse -Force .git
}
git init
Write-ColorOutput Green "✅ Git repository initialized"

# Step 3: Create .gitignore file
Write-ColorOutput Yellow "`n📌 Step 3: Creating .gitignore..."
$gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
logs/
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project specific
*.backup
*.tmp
temp/
"@

$gitignore | Out-File -FilePath ".gitignore" -Encoding utf8
Write-ColorOutput Green "✅ .gitignore created"

# Step 4: Create README.md
Write-ColorOutput Yellow "`n📌 Step 4: Creating README.md..."
$readme = @"
# 🇸🇬 AI Customer Copilot - Singapore Tourism Board

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)](https://openai.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-ready multi-agent AI system for Singapore tourism recommendations, powered by Large Language Models (LLMs). Built with a modular agent architecture that provides intelligent assistance for attractions, dining, shopping, and promotions.

## 🌟 Features

- 🤖 **Multi-Agent Architecture**: Planner, Retrieval, Analytics, Marketing, and Response agents
- 📊 **Realistic Singapore Data**: Complete datasets for attractions, restaurants, shops, and promotions
- 🎯 **Intelligent Recommendations**: Personalized suggestions based on user preferences
- 💬 **Natural Language Interface**: Conversational AI powered by GPT-4
- 🔍 **Semantic Search**: Vector-based search capabilities
- 📈 **Analytics Integration**: Customer behavior analysis and trend detection
- 🎨 **Marketing Content Generation**: Automated promotional content creation

## 🏗️ Architecture
