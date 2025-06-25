# XPERT AD-TARGETING Docker Makefile
# Provides convenient shortcuts for common Docker operations

.PHONY: help build up down logs clean setup dev prod shell test

# Default target
help:
	@echo "XPERT AD-TARGETING Docker Commands"
	@echo "=================================="
	@echo "setup     - Initial setup (create dirs, .env, build)"
	@echo "build     - Build Docker image"
	@echo "up        - Start services in background"
	@echo "down      - Stop and remove services"
	@echo "logs      - View application logs"
	@echo "dev       - Start in development mode"
	@echo "prod      - Start in production mode"
	@echo "shell     - Access container shell"
	@echo "test      - Run tests in container"
	@echo "clean     - Clean up containers and images"
	@echo "backup    - Backup data from container"
	@echo "restore   - Restore data to container"

# Initial setup
setup:
	@echo "🚀 Setting up XPERT AD-TARGETING Docker environment..."
	@mkdir -p data/logs data/AllJsons data/AllRawTexts data/screenshots config
	@if [ ! -f .env ]; then \
		if [ -f env.example ]; then \
			cp env.example .env; \
			echo "📝 Created .env from template. Please edit with your configuration."; \
		else \
			echo "❌ env.example not found. Please create .env manually."; \
			exit 1; \
		fi; \
	else \
		echo "✅ .env file already exists"; \
	fi
	@docker-compose build
	@echo "🎉 Setup completed!"

# Build Docker image
build:
	@echo "🔨 Building Docker image..."
	@docker-compose build

# Start services in background
up:
	@echo "🚀 Starting services..."
	@docker-compose up -d

# Stop and remove services
down:
	@echo "🛑 Stopping services..."
	@docker-compose down

# View logs
logs:
	@echo "📋 Viewing logs..."
	@docker-compose logs -f xpert-app

# Development mode
dev:
	@echo "🔧 Starting in development mode..."
	@docker-compose --profile development up --build

# Production mode
prod:
	@echo "🏭 Starting in production mode..."
	@docker-compose up -d

# Access container shell
shell:
	@echo "🐚 Accessing container shell..."
	@docker-compose exec xpert-app bash

# Run tests
test:
	@echo "🧪 Running tests..."
	@docker-compose run --rm xpert-app python -m pytest

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v --rmi all
	@docker system prune -f

# Backup data
backup:
	@echo "💾 Creating backup..."
	@mkdir -p backups
	@docker-compose exec xpert-app tar -czf /tmp/backup-$$(date +%Y%m%d_%H%M%S).tar.gz /app/AllJsons /app/AllRawTexts /app/logs
	@docker cp xpert-ad-targeting:/tmp/backup-*.tar.gz ./backups/
	@echo "✅ Backup created in ./backups/"

# Restore data (usage: make restore BACKUP_FILE=backup-20241201_120000.tar.gz)
restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify backup file: make restore BACKUP_FILE=backup-file.tar.gz"; \
		exit 1; \
	fi
	@echo "📥 Restoring from $(BACKUP_FILE)..."
	@docker cp ./backups/$(BACKUP_FILE) xpert-ad-targeting:/tmp/restore.tar.gz
	@docker-compose exec xpert-app tar -xzf /tmp/restore.tar.gz -C /
	@echo "✅ Restore completed"

# Show container status
status:
	@echo "📊 Container status:"
	@docker-compose ps
	@echo ""
	@echo "📈 Resource usage:"
	@docker stats --no-stream xpert-ad-targeting

# Show environment info
env-info:
	@echo "🔍 Environment information:"
	@docker-compose exec xpert-app env | grep -E "(AWS_|MONGO_|SSIM_|CLEANUP_|OUTPUT_|UPLOAD_)" | sort

# Check Tesseract
tesseract-check:
	@echo "🔍 Checking Tesseract installation:"
	@docker-compose exec xpert-app tesseract --version

# Check Python packages
packages:
	@echo "📦 Installed Python packages:"
	@docker-compose exec xpert-app pip list 