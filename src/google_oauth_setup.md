# Google OAuth Setup Instructions

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 3. Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

## 4. Set up Google OAuth Credentials

### Step 1: Go to Google Cloud Console
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API

### Step 2: Create OAuth 2.0 Credentials
1. Go to "Credentials" in the left sidebar
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application" as the application type
4. Add authorized redirect URIs:
   - For development: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - For production: `https://yourdomain.com/accounts/google/login/callback/`

### Step 3: Configure Environment Variables
Create a `.env` file in your project root with:
```
SECRET_KEY=your-secret-key
DEBUG=True
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_SECRET=your-client-secret
```

### Step 4: Update Settings
Add these to your `main/settings.py`:
```python
# Google OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': config('GOOGLE_OAUTH2_CLIENT_ID'),
            'secret': config('GOOGLE_OAUTH2_SECRET'),
        }
    }
}
```

## 5. Test the Setup
1. Run the development server: `python manage.py runserver`
2. Visit `http://127.0.0.1:8000/auth/login/`
3. Click "Continue with Google"
4. Complete the OAuth flow
5. You should be redirected to the role selection page

## 6. Admin Setup
1. Go to Django admin: `http://127.0.0.1:8000/admin/`
2. Add a new "Sites" entry with domain `127.0.0.1:8000` and name `localhost`
3. Add a new "Social Applications" entry:
   - Provider: Google
   - Name: Google OAuth
   - Client id: Your Google Client ID
   - Secret key: Your Google Client Secret
   - Sites: Select the site you created

## Notes
- The system now requires Google OAuth for both login and registration
- Users will be redirected to role selection after Google authentication
- Profile completion is required before accessing dashboards
- Full name is now included in both student and teacher profile forms
