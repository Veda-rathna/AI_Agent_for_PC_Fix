# Quick Setup Script for Google Gemini Integration
# Run this script from the backend directory

Write-Host "🚀 Setting up Google Gemini Integration..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the backend directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: This script must be run from the backend directory" -ForegroundColor Red
    Write-Host "   Run: cd backend" -ForegroundColor Yellow
    exit 1
}

# Step 1: Install dependencies
Write-Host "📦 Step 1: Installing Python dependencies..." -ForegroundColor Green
pip install google-generativeai>=0.3.0 python-dotenv>=1.0.0
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Check if .env exists
Write-Host "📝 Step 2: Checking environment configuration..." -ForegroundColor Green
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Write-Host "📋 Copying .env.example to .env..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔑 IMPORTANT: Edit .env and add your Google Gemini API key!" -ForegroundColor Yellow
        Write-Host "   Get your key from: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "❌ .env.example not found" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
    Write-Host ""
}

# Step 3: Verify configuration
Write-Host "🔍 Step 3: Verifying configuration..." -ForegroundColor Green
$envContent = Get-Content ".env" -Raw

if ($envContent -match "GEMINI_API_KEY=your_google_gemini_api_key_here") {
    Write-Host "⚠️  WARNING: GEMINI_API_KEY is still set to placeholder!" -ForegroundColor Yellow
    Write-Host "   Please update .env with your actual API key" -ForegroundColor Yellow
    Write-Host ""
} elseif ($envContent -match "GEMINI_API_KEY=\w+") {
    Write-Host "✅ GEMINI_API_KEY is configured" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⚠️  GEMINI_API_KEY not found in .env" -ForegroundColor Yellow
    Write-Host ""
}

if ($envContent -match "LLM_PROVIDER=gemini") {
    Write-Host "✅ LLM_PROVIDER set to gemini" -ForegroundColor Green
} else {
    Write-Host "ℹ️  LLM_PROVIDER not set to gemini (will use default)" -ForegroundColor Cyan
}
Write-Host ""

# Step 4: Test Django setup
Write-Host "🧪 Step 4: Testing Django configuration..." -ForegroundColor Green
python manage.py check --deploy
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Django check found some issues" -ForegroundColor Yellow
} else {
    Write-Host "✅ Django configuration is valid" -ForegroundColor Green
}
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env and add your Google Gemini API key" -ForegroundColor White
Write-Host "2. Run: python manage.py runserver" -ForegroundColor White
Write-Host "3. Test the API at: http://localhost:8000/api/predict/" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - GEMINI_INTEGRATION_GUIDE.md" -ForegroundColor White
Write-Host "   - README.md (updated with Google integration)" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Get API Key: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
Write-Host ""
