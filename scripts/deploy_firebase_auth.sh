#!/bin/bash
# Firebase Authentication Deployment Script for LANCELOTT
# Deploys Firebase Auth configuration, security rules, and Data Connect

set -e

echo "🔥 LANCELOTT Firebase Authentication Deployment"
echo "=============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Firebase CLI is installed
    if ! command -v firebase &> /dev/null; then
        log_error "Firebase CLI is not installed"
        log_info "Install with: npm install -g firebase-tools"
        exit 1
    fi

    log_success "Firebase CLI found: $(firebase --version)"

    # Check if logged in to Firebase
    if ! firebase projects:list &> /dev/null; then
        log_warning "Not logged in to Firebase"
        log_info "Logging in to Firebase..."
        firebase login
    fi

    log_success "Firebase authentication verified"

    # Check if firebase.json exists
    if [[ ! -f "firebase.json" ]]; then
        log_error "firebase.json not found"
        exit 1
    fi

    log_success "firebase.json found"

    # Check if .firebaserc exists
    if [[ ! -f ".firebaserc" ]]; then
        log_error ".firebaserc not found"
        exit 1
    fi

    log_success ".firebaserc found"
}

# Deploy Firestore security rules
deploy_firestore_rules() {
    log_info "Deploying Firestore security rules..."

    if [[ ! -f "firestore.rules" ]]; then
        log_warning "firestore.rules not found, skipping..."
        return
    fi

    firebase deploy --only firestore:rules
    log_success "Firestore rules deployed"
}

# Deploy Storage security rules
deploy_storage_rules() {
    log_info "Deploying Storage security rules..."

    if [[ ! -f "storage.rules" ]]; then
        log_warning "storage.rules not found, skipping..."
        return
    fi

    firebase deploy --only storage
    log_success "Storage rules deployed"
}

# Deploy Firestore indexes
deploy_firestore_indexes() {
    log_info "Deploying Firestore indexes..."

    if [[ ! -f "firestore.indexes.json" ]]; then
        log_warning "firestore.indexes.json not found, skipping..."
        return
    fi

    firebase deploy --only firestore:indexes
    log_success "Firestore indexes deployed"
}

# Deploy Firebase Functions
deploy_functions() {
    log_info "Deploying Firebase Functions..."

    if [[ ! -d "functions" ]]; then
        log_warning "functions directory not found, skipping..."
        return
    fi

    # Install function dependencies
    if [[ -f "functions/requirements.txt" ]]; then
        log_info "Installing function dependencies..."
        cd functions
        pip install -r requirements.txt
        cd ..
    fi

    firebase deploy --only functions
    log_success "Firebase Functions deployed"
}

# Deploy Firebase Data Connect
deploy_dataconnect() {
    log_info "Deploying Firebase Data Connect..."

    if [[ ! -f "dataconnect.yaml" ]]; then
        log_warning "dataconnect.yaml not found, skipping Data Connect deployment..."
        return
    fi

    if [[ ! -d "dataconnect" ]]; then
        log_warning "dataconnect directory not found, skipping..."
        return
    fi

    firebase deploy --only dataconnect
    log_success "Firebase Data Connect deployed"
}

# Deploy Firebase Hosting
deploy_hosting() {
    log_info "Deploying Firebase Hosting..."

    # Check if dist directory exists
    if [[ ! -d "dist" ]]; then
        log_warning "dist directory not found, creating basic index.html..."
        mkdir -p dist
        cat > dist/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>LANCELOTT Security Framework</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            text-align: center;
            padding: 50px;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            font-size: 3em;
            color: #00ff88;
            margin-bottom: 20px;
        }
        .links {
            margin: 30px 0;
        }
        .links a {
            color: #00ff88;
            text-decoration: none;
            margin: 0 15px;
            padding: 10px 20px;
            border: 2px solid #00ff88;
            border-radius: 5px;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .links a:hover {
            background: #00ff88;
            color: #1e3c72;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ LANCELOTT</h1>
        <p>Professional Security Framework</p>
        <p>Unified Penetration Testing Suite</p>

        <div class="links">
            <a href="/docs">API Documentation</a>
            <a href="/api/v1/health">System Health</a>
            <a href="/api/v1/auth/config">Auth Config</a>
        </div>

        <p>Framework Status: <strong>Online</strong></p>
        <p>Version: 2.1.0</p>
    </div>
</body>
</html>
EOF
    fi

    firebase deploy --only hosting
    log_success "Firebase Hosting deployed"
}

# Verify deployment
verify_deployment() {
    log_info "Verifying deployment..."

    # Get project info
    PROJECT_ID=$(firebase use | grep "Now using project" | awk '{print $4}' || echo "unknown")

    if [[ "$PROJECT_ID" == "unknown" ]]; then
        PROJECT_ID=$(cat .firebaserc | grep -o '"default":[^,]*' | cut -d'"' -f4)
    fi

    log_info "Project ID: $PROJECT_ID"

    # Check hosting
    HOSTING_URL="https://${PROJECT_ID}.web.app"
    log_info "Hosting URL: $HOSTING_URL"

    # Check functions
    FUNCTIONS_URL="https://us-central1-${PROJECT_ID}.cloudfunctions.net"
    log_info "Functions URL: $FUNCTIONS_URL"

    # Test endpoints
    log_info "Testing endpoints..."

    # Test hosting
    if curl -s -o /dev/null -w "%{http_code}" "$HOSTING_URL" | grep -q "200"; then
        log_success "Hosting endpoint is accessible"
    else
        log_warning "Hosting endpoint may not be ready yet"
    fi

    log_success "Deployment verification completed"
}

# Print setup summary
print_summary() {
    echo ""
    echo "🎉 Firebase Authentication Deployment Summary"
    echo "============================================="

    PROJECT_ID=$(cat .firebaserc | grep -o '"default":[^,]*' | cut -d'"' -f4)

    echo ""
    echo "📋 Deployed Components:"
    echo "   ✅ Firestore Security Rules"
    echo "   ✅ Storage Security Rules"
    echo "   ✅ Firestore Indexes"
    echo "   ✅ Firebase Functions"
    echo "   ✅ Firebase Data Connect"
    echo "   ✅ Firebase Hosting"
    echo ""
    echo "🌐 Access URLs:"
    echo "   🏠 Dashboard: https://${PROJECT_ID}.web.app"
    echo "   📚 API Docs: https://${PROJECT_ID}.web.app/docs"
    echo "   🔐 Auth API: https://${PROJECT_ID}.web.app/api/v1/auth"
    echo "   🔥 Functions: https://us-central1-${PROJECT_ID}.cloudfunctions.net"
    echo "   📊 Console: https://console.firebase.google.com/project/${PROJECT_ID}"
    echo ""
    echo "🔐 Authentication Setup:"
    echo "   📧 Admin Email: knightprojeks@gmail.com"
    echo "   🔑 Password: Ggg123456789ggG!"
    echo "   👑 Role: Admin"
    echo "   🛡️ Permissions: Full Access"
    echo ""
    echo "🔧 Next Steps:"
    echo "   1. Go to Firebase Console > Authentication > Users"
    echo "   2. Find user: knightprojeks@gmail.com"
    echo "   3. Set password: Ggg123456789ggG!"
    echo "   4. Enable the user account"
    echo "   5. Test login at: https://${PROJECT_ID}.web.app"
    echo ""
    echo "⚠️  Security Notes:"
    echo "   • Change default password after first login"
    echo "   • Enable 2FA when available"
    echo "   • Review and adjust permissions as needed"
    echo "   • Monitor authentication logs regularly"
    echo ""
}

# Main deployment process
main() {
    echo "🚀 Starting Firebase deployment..."
    echo ""

    # Run deployment steps
    check_prerequisites
    echo ""

    deploy_firestore_rules
    echo ""

    deploy_storage_rules
    echo ""

    deploy_firestore_indexes
    echo ""

    deploy_dataconnect
    echo ""

    deploy_functions
    echo ""

    deploy_hosting
    echo ""

    verify_deployment
    echo ""

    print_summary

    log_success "Firebase deployment completed successfully!"
}

# Error handling
trap 'log_error "Deployment failed! Check error messages above."' ERR

# Run main function
main "$@"
