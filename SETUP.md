# OpportunityAI Setup Guide

This guide will help you set up the complete OpportunityAI development environment.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 13+
- Docker and Docker Compose (optional)
- React Native development environment (for mobile development)

## Quick Start with Docker

1. **Clone and setup environment**
   ```bash
   git clone <repository-url>
   cd OpportunityAI
   cp .env.example .env
   ```

2. **Configure environment variables**
   Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

3. **Start with Docker**
   ```bash
   npm run docker:up
   ```

4. **Access the services**
   - Backend API: http://localhost:3000
   - AI Engine: http://localhost:8000
   - Database: localhost:5432

## Manual Setup

### 1. Database Setup

```bash
# Install and start PostgreSQL
# Create database
creatdb opportunity_ai

# Run schema
psql -U postgres -d opportunity_ai -f database/schema.sql
```

### 2. Backend Setup

```bash
cd backend
npm install
cp ../.env.example .env  # Configure your environment
npm run build
npm run dev
```

### 3. AI Engine Setup

```bash
cd ai-engine
pip install -r requirements.txt
cp ../.env.example .env  # Add your OpenAI API key
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Mobile App Setup

```bash
cd mobile
npm install

# For iOS development
npx pod-install ios

# Start Metro bundler
npm start

# In another terminal, run on device/simulator
npm run ios     # iOS
npm run android # Android
```

## Environment Variables

Key environment variables you need to configure:

- `OPENAI_API_KEY`: Your OpenAI API key for the AI engine
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token generation
- `NODE_ENV`: Set to 'development' for local development

## Testing the Setup

1. **Test Backend API**
   ```bash
   curl http://localhost:3000/health
   ```

2. **Test AI Engine**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test Database Connection**
   ```bash
   psql -U postgres -d opportunity_ai -c "SELECT COUNT(*) FROM career_paths;"
   ```

## Development Workflow

1. **Start all services**
   ```bash
   npm run docker:up
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop services**
   ```bash
   npm run docker:down
   ```

## API Endpoints

### Backend API (Port 3000)
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/chat/message` - Send chat message
- `GET /api/career/paths` - Get career paths
- `POST /api/career/forecast` - Generate career forecast

### AI Engine (Port 8000)
- `GET /health` - Health check
- `POST /chat` - Process chat message
- `POST /career-match` - Find matching careers
- `POST /recommendations` - Get recommendations

## Troubleshooting

### Common Issues

**Database Connection Issues**
- Ensure PostgreSQL is running
- Check DATABASE_URL in your .env file
- Verify database exists and schema is loaded

**OpenAI API Issues**
- Verify your API key is correct
- Check your OpenAI account has sufficient credits
- Ensure the key has proper permissions

**React Native Issues**
- Clear Metro cache: `npx react-native start --reset-cache`
- Clean build: `cd ios && xcodebuild clean` (iOS)
- Ensure Android SDK is properly configured

**Docker Issues**
- Clear Docker cache: `docker system prune -a`
- Rebuild containers: `npm run docker:build`
- Check Docker daemon is running

### Getting Help

If you encounter issues:
1. Check the logs: `docker-compose logs service-name`
2. Verify environment variables are set correctly
3. Ensure all prerequisites are installed
4. Try rebuilding containers: `npm run docker:build`

## Next Steps

Once setup is complete:
1. Test the mobile app with the backend
2. Try the chat functionality
3. Explore career recommendations
4. Generate 4-year career forecasts

For development, see the individual README files in each component directory.