---
title: "Firebase Service Account Setup"
date: "2025-08-28"
author: "QODER"
change_type: ["setup", "integration"]
modules: ["core/firebase_config", "api/routes/tars_api"]
links:
  pr: ""
  issues: []
summary: "Complete guide for setting up Firebase service account credentials for LANCELOTT TARS integration"
impact: "Enables Firebase Authentication, Firestore, and Storage integration for TARS API logging and synchronization"
---

# Firebase Service Account Setup

This document provides a comprehensive guide for setting up Firebase service account credentials for the LANCELOTT TARS integration.

## Overview

Firebase integration enables:

- **Authentication**: Secure user authentication and authorization
- **Firestore**: Real-time database for logging TARS events and commands
- **Storage**: File storage for reports, logs, and artifacts
- **Real-time Sync**: Dashboard synchronization with Firebase services

## Prerequisites

1. Google Cloud Account with billing enabled
2. Firebase Console access
3. LANCELOTT project with proper permissions
4. Terminal access to the LANCELOTT installation

## Step 1: Create Firebase Project

### 1.1 Firebase Console Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `lancelott-cybersec` (or your preferred name)
4. Enable Google Analytics (recommended)
5. Choose or create a Google Analytics account
6. Click "Create project"

### 1.2 Project Configuration

1. In the Firebase Console, go to Project Settings (gear icon)
2. Note the following information:
   - **Project ID**: `lancelott-cybersec`
   - **Web API Key**: Found in "General" tab
   - **Project Number**: Also in "General" tab

## Step 2: Enable Firebase Services

### 2.1 Authentication

1. In Firebase Console, go to "Authentication"
2. Click "Get started"
3. Go to "Sign-in method" tab
4. Enable the following providers:
   - **Email/Password**: For basic authentication
   - **Google**: For OAuth authentication (optional)
   - **Anonymous**: For guest access (optional)

### 2.2 Firestore Database

1. Go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location close to your servers
5. Click "Done"

### 2.3 Storage

1. Go to "Storage"
2. Click "Get started"
3. Review security rules
4. Choose the same location as Firestore
5. Click "Done"

## Step 3: Generate Service Account

### 3.1 Create Service Account

1. In Firebase Console, go to **Project Settings** → **Service accounts**
2. Click "Generate new private key"
3. Confirm by clicking "Generate key"
4. A JSON file will be downloaded automatically

### 3.2 Service Account Permissions

The service account automatically has the following roles:

- **Firebase Admin**: Full access to all Firebase services
- **Editor**: Can read and write to all project resources

For production, consider creating custom roles with minimal permissions.

## Step 4: Configure LANCELOTT

### 4.1 Service Account File Method (Recommended for Development)

1. Rename the downloaded JSON file to `firebase-service-account.json`
2. Place it in the LANCELOTT root directory:

   ```bash
   mv ~/Downloads/lancelott-cybersec-*.json /path/to/LANCELOTT/firebase-service-account.json
   ```

3. Verify file permissions:

   ```bash
   chmod 600 firebase-service-account.json
   ```

4. Add to `.gitignore` (already included):

   ```bash
   echo "firebase-service-account.json" >> .gitignore
   ```

### 4.2 Environment Variable Method (Recommended for Production)

1. Convert the service account JSON to base64:

   ```bash
   base64 -i firebase-service-account.json | tr -d '\n' | pbcopy
   ```

2. Add to your `.env` file:

   ```bash
   # Firebase Configuration
   FIREBASE_PROJECT_ID=lancelott-cybersec
   FIREBASE_SERVICE_ACCOUNT_BASE64=<paste_base64_string_here>
   FIREBASE_STORAGE_BUCKET=lancelott-cybersec.appspot.com
   FIREBASE_AUTH_DOMAIN=lancelott-cybersec.firebaseapp.com
   FIREBASE_DATABASE_URL=https://lancelott-cybersec-default-rtdb.firebaseio.com
   FIREBASE_API_KEY=<your_web_api_key>
   FIREBASE_MESSAGING_SENDER_ID=<your_sender_id>
   FIREBASE_APP_ID=<your_app_id>
   ```

### 4.3 Validation

Test the configuration:

```bash
python -c "
from core.firebase_config import initialize_firebase
success = initialize_firebase()
print('Firebase initialized:', success)
"
```

## Step 5: Security Configuration

### 5.1 Firestore Security Rules

Configure Firestore rules for TARS events:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // TARS events collection - authenticated users only
    match /tars_events/{document} {
      allow read, write: if request.auth != null;
    }

    // User data - owner only
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Admin collections - admin users only
    match /admin/{document} {
      allow read, write: if request.auth != null &&
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
  }
}
```

### 5.2 Storage Security Rules

Configure Storage rules:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // TARS logs and reports
    match /tars/{allPaths=**} {
      allow read, write: if request.auth != null;
    }

    // User uploads
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 5.3 Network Security

For production deployments:

1. **IP Allowlisting**: Configure Firebase to only accept connections from your server IPs
2. **VPC Configuration**: Use Google Cloud VPC for network isolation
3. **SSL/TLS**: Ensure all connections use HTTPS/TLS

## Step 6: Environment-Specific Configuration

### 6.1 Development Environment

```bash
# .env.development
FIREBASE_PROJECT_ID=lancelott-cybersec-dev
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
FIREBASE_STORAGE_BUCKET=lancelott-cybersec-dev.appspot.com
```

### 6.2 Production Environment

```bash
# .env.production
FIREBASE_PROJECT_ID=lancelott-cybersec-prod
FIREBASE_SERVICE_ACCOUNT_BASE64=<base64_encoded_credentials>
FIREBASE_STORAGE_BUCKET=lancelott-cybersec-prod.appspot.com
```

### 6.3 Testing Environment

```bash
# .env.test
FIREBASE_PROJECT_ID=lancelott-cybersec-test
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account-test.json
FIREBASE_STORAGE_BUCKET=lancelott-cybersec-test.appspot.com
```

## Step 7: Backup and Recovery

### 7.1 Service Account Backup

1. Store service account JSON in secure password manager
2. Create multiple service accounts for redundancy
3. Document all service account IDs and purposes

### 7.2 Firebase Project Backup

1. Export Firestore data regularly:

   ```bash
   gcloud firestore export gs://lancelott-cybersec-backup/$(date +%Y%m%d)
   ```

2. Backup Firebase configuration:

   ```bash
   firebase projects:list
   firebase use lancelott-cybersec
   firebase functions:config:get > firebase-config-backup.json
   ```

## Troubleshooting

### Common Issues

1. **"Default credentials not available"**
   - Ensure service account JSON is in the correct location
   - Check file permissions (should be 600)
   - Verify FIREBASE_SERVICE_ACCOUNT_BASE64 is properly encoded

2. **"Permission denied"**
   - Verify service account has Firebase Admin role
   - Check Firestore security rules
   - Ensure project ID is correct

3. **"Project not found"**
   - Verify FIREBASE_PROJECT_ID environment variable
   - Check Firebase Console for correct project ID
   - Ensure billing is enabled for the project

### Debug Commands

```bash
# Test Firebase connection
python scripts/test_firebase_connection.py

# Validate configuration
python -c "from core.firebase_config import get_firebase; print(get_firebase().verify_connection())"

# Check environment variables
env | grep FIREBASE
```

### Log Analysis

Monitor Firebase logs:

```bash
# Application logs
tail -f logs/lancelott.log | grep -i firebase

# Firebase debug logs
export GOOGLE_APPLICATION_CREDENTIALS=firebase-service-account.json
export FIREBASE_CONFIG_DEBUG=true
python app.py
```

## Security Best Practices

### 1. Credential Management

- **Never commit** service account JSON to version control
- Use **environment variables** for production deployments
- **Rotate credentials** regularly (every 90 days)
- **Monitor usage** through Google Cloud Console

### 2. Access Control

- **Principle of least privilege**: Grant minimum required permissions
- **Regular audits**: Review service account usage monthly
- **Multi-factor authentication**: Enable for Firebase Console access
- **IP restrictions**: Limit access to known IP ranges

### 3. Monitoring

- **Enable audit logs** in Google Cloud Console
- **Set up alerts** for unusual activity
- **Monitor costs** to detect potential abuse
- **Regular security reviews** of Firebase rules

### 4. Compliance

- **Data residency**: Choose appropriate Firebase regions
- **Encryption**: Ensure data is encrypted at rest and in transit
- **Retention policies**: Configure appropriate data retention
- **Privacy controls**: Implement GDPR/CCPA compliance measures

## Integration Testing

### Test Checklist

- [ ] Firebase initialization succeeds
- [ ] Firestore read/write operations work
- [ ] Authentication flow functions
- [ ] Storage upload/download works
- [ ] TARS event logging operates correctly
- [ ] Error handling functions properly
- [ ] Performance meets requirements

### Automated Tests

```bash
# Run Firebase integration tests
python -m pytest tests/integration/test_firebase_integration.py

# Run TARS API tests
python -m pytest tests/api/test_tars_api.py

# Full integration test suite
python tests/run_firebase_tests.py
```

## Support and Resources

### Documentation Links

- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Google Cloud IAM](https://cloud.google.com/iam/docs)

### Internal Resources

- TARS API Documentation: `docs/api/TARS_API_REFERENCE.md`
- Firebase Integration: `docs/integration/FIREBASE_INTEGRATION_COMPLETE.md`
- Security Guidelines: `docs/guides/SECURITY_GUIDE.md`

### Contact Information

For issues with Firebase setup:

1. Check the troubleshooting section above
2. Review application logs in `logs/`
3. Consult the LANCELOTT development team
4. Create an issue in the project repository

---

**Last Updated**: 2025-08-28
**Next Review**: 2025-09-28
**Version**: 1.0
