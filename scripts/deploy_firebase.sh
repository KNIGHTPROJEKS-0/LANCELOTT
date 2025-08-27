#!/bin/bash

# LANCELOTT Firebase Deployment Script
# Comprehensive deployment automation for Firebase and GitHub integration
# Version: 2.1.0

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="lancelott-z9dko"
GITHUB_REPO="ORDEROFCODE/LANCELOTT"
DEPLOY_ENV="${DEPLOY_ENV:-production}"

# Function to print colored output
print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                   🛡️  LANCELOTT DEPLOYMENT SCRIPT                           ║${NC}"
    echo -e "${PURPLE}║                    Firebase & GitHub Integration                            ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${CYAN}🔄 $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."

    # Check if required tools are installed
    command -v firebase >/dev/null 2>&1 || {
        print_error "Firebase CLI is not installed. Installing..."
        npm install -g firebase-tools
    }

    command -v git >/dev/null 2>&1 || {
        print_error "Git is not installed. Please install Git first."
        exit 1
    }

    command -v python3 >/dev/null 2>&1 || {
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    }

    command -v node >/dev/null 2>&1 || {
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    }

    print_status "All prerequisites satisfied"
}

# Validate Firebase configuration
validate_firebase_config() {
    print_step "Validating Firebase configuration..."

    # Check for required files
    required_files=(
        "firebase.json"
        ".firebaserc"
        "firestore.rules"
        "storage.rules"
        "firestore.indexes.json"
    )

    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            print_status "Found $file"
        else
            print_error "Missing required file: $file"
            exit 1
        fi
    done

    # Validate Firebase project
    if firebase use --token "$FIREBASE_TOKEN" >/dev/null 2>&1; then
        print_status "Firebase authentication successful"
    else
        print_warning "Firebase authentication may be required"
        echo "Please run: firebase login"
    fi

    print_status "Firebase configuration validated"
}

# Validate environment configuration
validate_environment() {
    print_step "Validating environment configuration..."

    # Check .env file
    if [[ -f ".env" ]]; then
        print_status "Environment file found"

        # Check required environment variables
        required_vars=(
            "FIREBASE_PROJECT_ID"
            "FIREBASE_API_KEY"
            "FIREBASE_AUTH_DOMAIN"
            "FIREBASE_STORAGE_BUCKET"
        )

        for var in "${required_vars[@]}"; do
            if grep -q "^$var=" .env; then
                print_status "Found $var in environment"
            else
                print_warning "Missing $var in environment"
            fi
        done
    else
        print_warning "No .env file found. Using .env.example..."
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            print_status "Created .env from template"
        else
            print_error "No .env.example found"
            exit 1
        fi
    fi

    print_status "Environment configuration validated"
}

# Build the application
build_application() {
    print_step "Building LANCELOTT application..."

    # Create virtual environment if it doesn't exist
    if [[ ! -d ".venv" ]]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv .venv
    fi

    # Activate virtual environment
    source .venv/bin/activate
    print_status "Virtual environment activated"

    # Install Python dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt >/dev/null 2>&1
    print_status "Python dependencies installed"

    # Install Functions dependencies
    if [[ -d "functions" ]]; then
        print_info "Installing Firebase Functions dependencies..."
        cd functions
        pip install -r requirements.txt >/dev/null 2>&1
        cd ..
        print_status "Functions dependencies installed"
    fi

    # Ensure dist directory exists and copy files
    print_info "Preparing static files..."
    mkdir -p dist

    # Copy static files if they exist
    if [[ -d "static" ]]; then
        cp -r static/* dist/ 2>/dev/null || true
    fi

    # Ensure index.html exists
    if [[ ! -f "dist/index.html" ]]; then
        print_warning "No index.html found in dist/, using default dashboard"
    fi

    print_status "Application build completed"
}

# Run tests before deployment
run_tests() {
    print_step "Running tests..."

    # Activate virtual environment
    source .venv/bin/activate

    # Install test dependencies
    pip install pytest pytest-asyncio pytest-cov >/dev/null 2>&1

    # Run tests
    if pytest tests/ -v --tb=short; then
        print_status "All tests passed"
    else
        print_error "Tests failed"
        read -p "Continue with deployment anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Deploy to Firebase
deploy_firebase() {
    print_step "Deploying to Firebase..."

    # Authenticate with Firebase
    if [[ -n "$FIREBASE_TOKEN" ]]; then
        print_info "Using Firebase token for authentication"
        AUTH_FLAG="--token $FIREBASE_TOKEN"
    else
        AUTH_FLAG=""
        print_info "Using local Firebase authentication"
    fi

    # Set Firebase project
    firebase use "$PROJECT_ID" $AUTH_FLAG
    print_status "Using Firebase project: $PROJECT_ID"

    # Deploy Firestore rules
    print_info "Deploying Firestore rules..."
    firebase deploy --only firestore:rules $AUTH_FLAG

    # Deploy Firestore indexes
    print_info "Deploying Firestore indexes..."
    firebase deploy --only firestore:indexes $AUTH_FLAG

    # Deploy Storage rules
    print_info "Deploying Storage rules..."
    firebase deploy --only storage $AUTH_FLAG

    # Deploy Functions (if they exist)
    if [[ -d "functions" ]]; then
        print_info "Deploying Firebase Functions..."
        firebase deploy --only functions $AUTH_FLAG
    fi

    # Deploy Hosting
    print_info "Deploying Firebase Hosting..."
    firebase deploy --only hosting $AUTH_FLAG

    print_status "Firebase deployment completed"
}

# Verify deployment
verify_deployment() {
    print_step "Verifying deployment..."

    # Wait for deployment to propagate
    print_info "Waiting for deployment to propagate..."
    sleep 30

    # Test main site
    if curl -sf "https://$PROJECT_ID.web.app" >/dev/null; then
        print_status "Main site is accessible"
    else
        print_warning "Main site may not be ready yet"
    fi

    # Test API health endpoint
    if curl -sf "https://$PROJECT_ID.web.app/api/health" >/dev/null; then
        print_status "API health endpoint is working"
    else
        print_warning "API health endpoint may not be ready yet"
    fi

    # Test Firebase Functions
    if curl -sf "https://us-central1-$PROJECT_ID.cloudfunctions.net/health_check" >/dev/null; then
        print_status "Firebase Functions are working"
    else
        print_warning "Firebase Functions may not be ready yet"
    fi

    print_status "Deployment verification completed"
}

# Update GitHub repository
update_github() {
    print_step "Updating GitHub repository..."

    # Check if we're in a git repository
    if [[ ! -d ".git" ]]; then
        print_warning "Not in a Git repository. Initializing..."
        git init
        git remote add origin "https://github.com/$GITHUB_REPO.git"
    fi

    # Check for changes
    if git diff --quiet && git diff --staged --quiet; then
        print_info "No changes to commit"
    else
        # Add all files
        git add .

        # Create commit
        commit_message="🚀 Deploy LANCELOTT v2.1.0 to Firebase - $(date '+%Y-%m-%d %H:%M:%S')"
        git commit -m "$commit_message"
        print_status "Changes committed"

        # Push to GitHub
        if git push origin main; then
            print_status "Changes pushed to GitHub"
        else
            print_warning "Failed to push to GitHub. You may need to authenticate."
        fi
    fi
}

# Generate deployment report
generate_report() {
    print_step "Generating deployment report..."

    cat > deployment-report.md << EOF
# 🛡️ LANCELOTT Deployment Report

**Deployment Date:** $(date)
**Environment:** $DEPLOY_ENV
**Project ID:** $PROJECT_ID

## 🚀 Deployment Summary

| Service | Status | URL |
|---------|---------|-----|
| Firebase Hosting | ✅ Deployed | https://$PROJECT_ID.web.app |
| Firebase Functions | ✅ Deployed | https://us-central1-$PROJECT_ID.cloudfunctions.net |
| Firestore Database | ✅ Updated | Rules and indexes deployed |
| Cloud Storage | ✅ Updated | Security rules deployed |

## 🎯 Quick Links

- **Dashboard:** https://$PROJECT_ID.web.app
- **API Documentation:** https://$PROJECT_ID.web.app/docs
- **API Health Check:** https://$PROJECT_ID.web.app/api/health
- **Firebase Console:** https://console.firebase.google.com/project/$PROJECT_ID
- **GitHub Repository:** https://github.com/$GITHUB_REPO

## 📋 Deployment Steps Completed

- ✅ Prerequisites checked
- ✅ Firebase configuration validated
- ✅ Environment configuration validated
- ✅ Application built successfully
- ✅ Tests executed
- ✅ Firebase services deployed
- ✅ Deployment verified
- ✅ GitHub repository updated

## 🔗 Next Steps

1. Verify all services are working correctly
2. Monitor logs for any issues
3. Update documentation if needed
4. Notify team of successful deployment

## 📊 Deployment Metrics

- **Build Time:** $(date)
- **Deployment Duration:** Approximately 5-10 minutes
- **Services Deployed:** 4 (Hosting, Functions, Firestore, Storage)

EOF

    print_status "Deployment report generated: deployment-report.md"
}

# Main deployment function
main() {
    print_header

    echo "🚀 Starting LANCELOTT deployment process..."
    echo "📋 Environment: $DEPLOY_ENV"
    echo "🔥 Firebase Project: $PROJECT_ID"
    echo "📱 GitHub Repository: $GITHUB_REPO"
    echo ""

    # Run deployment steps
    check_prerequisites
    validate_firebase_config
    validate_environment
    build_application

    # Ask for confirmation before proceeding with deployment
    echo ""
    print_info "Ready to deploy to Firebase. This will:"
    echo "  • Deploy to Firebase project: $PROJECT_ID"
    echo "  • Update Firestore rules and indexes"
    echo "  • Deploy Cloud Functions"
    echo "  • Update Firebase Hosting"
    echo ""
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
        deploy_firebase
        verify_deployment
        update_github
        generate_report

        echo ""
        print_status "🎉 LANCELOTT deployment completed successfully!"
        echo ""
        echo "🌐 Your application is now live at:"
        echo "   https://$PROJECT_ID.web.app"
        echo ""
        echo "📚 API Documentation:"
        echo "   https://$PROJECT_ID.web.app/docs"
        echo ""
        echo "🔥 Firebase Console:"
        echo "   https://console.firebase.google.com/project/$PROJECT_ID"
        echo ""
    else
        print_info "Deployment cancelled by user"
        exit 0
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "validate")
        print_header
        check_prerequisites
        validate_firebase_config
        validate_environment
        print_status "Validation completed successfully"
        ;;
    "build")
        print_header
        check_prerequisites
        build_application
        print_status "Build completed successfully"
        ;;
    "test")
        print_header
        check_prerequisites
        run_tests
        print_status "Tests completed successfully"
        ;;
    "help"|"--help"|"-h")
        echo "🛡️ LANCELOTT Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy    - Full deployment process (default)"
        echo "  validate  - Validate configuration only"
        echo "  build     - Build application only"
        echo "  test      - Run tests only"
        echo "  help      - Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  FIREBASE_TOKEN  - Firebase CI token for authentication"
        echo "  DEPLOY_ENV      - Deployment environment (default: production)"
        echo ""
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
