-- OpportunityAI Database Schema
-- PostgreSQL Database Schema for Military Career Guidance App

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_guest BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- User profiles table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    age INTEGER,
    education_level VARCHAR(50),
    current_occupation VARCHAR(100),
    location VARCHAR(100),
    phone VARCHAR(20),
    interests TEXT[], -- Array of interests
    skills TEXT[], -- Array of skills
    military_interest JSONB, -- JSON object for military preferences
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Career paths table
CREATE TABLE career_paths (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT[] NOT NULL,
    training_duration VARCHAR(100),
    difficulty_level VARCHAR(20),
    match_keywords TEXT[],
    civilian_translation JSONB,
    promotion_timeline JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata JSONB, -- For storing additional message data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saved careers table (user bookmarks)
CREATE TABLE saved_careers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    career_path_id VARCHAR(50) REFERENCES career_paths(id) ON DELETE CASCADE,
    notes TEXT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, career_path_id)
);

-- Career forecasts table
CREATE TABLE career_forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    career_path_id VARCHAR(50) REFERENCES career_paths(id) ON DELETE CASCADE,
    forecast_data JSONB NOT NULL,
    service_years INTEGER DEFAULT 4,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table (for tracking engagement)
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    duration_minutes INTEGER,
    pages_visited TEXT[],
    actions_taken JSONB
);

-- Recommendations table
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    priority VARCHAR(20) DEFAULT 'medium',
    is_dismissed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_saved_careers_user_id ON saved_careers(user_id);
CREATE INDEX idx_career_forecasts_user_id ON career_forecasts(user_id);
CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX idx_career_paths_branch ON career_paths(branch);
CREATE INDEX idx_career_paths_service_type ON career_paths(service_type);

-- Create GIN index for JSONB columns
CREATE INDEX idx_user_profiles_military_interest ON user_profiles USING gin(military_interest);
CREATE INDEX idx_career_paths_civilian_translation ON career_paths USING gin(civilian_translation);
CREATE INDEX idx_recommendations_content ON recommendations USING gin(content);

-- Insert sample career paths data
INSERT INTO career_paths (id, title, branch, service_type, description, requirements, training_duration, difficulty_level, match_keywords, civilian_translation, promotion_timeline) VALUES
('cyber-operations', 'Cybersecurity Specialist', 'Air Force', 'Active Duty', 
 'Protect military networks from cyber threats, conduct digital investigations, and implement security protocols.',
 ARRAY['High school diploma', 'Security clearance eligible', 'Strong analytical skills'],
 '6-12 months', 'moderate',
 ARRAY['cyber', 'technology', 'computer', 'security', 'IT', 'networks'],
 '{"job_titles": ["Cybersecurity Analyst", "Information Security Manager", "SOC Analyst"], "average_salary": "$85,000 - $140,000", "growth_outlook": "Excellent (22% growth)", "certifications": ["Security+", "CISSP", "CEH"]}',
 '[{"rank": "Airman Basic", "timeframe": "0-6 months", "pay_grade": "E-1"}, {"rank": "Senior Airman", "timeframe": "2-3 years", "pay_grade": "E-4"}, {"rank": "Staff Sergeant", "timeframe": "4-6 years", "pay_grade": "E-5"}]'),

('aviation-mechanic', 'Aircraft Maintenance Technician', 'Navy', 'Active Duty',
 'Maintain and repair military aircraft to ensure flight safety and mission readiness.',
 ARRAY['High school diploma', 'Mechanical aptitude', 'Attention to detail'],
 '4-6 months', 'moderate',
 ARRAY['aviation', 'aircraft', 'mechanical', 'repair', 'maintenance', 'hands-on'],
 '{"job_titles": ["Aircraft Mechanic", "Aviation Technician", "Maintenance Supervisor"], "average_salary": "$65,000 - $95,000", "growth_outlook": "Good (5% growth)", "certifications": ["A&P License", "FAA Certifications"]}',
 '[{"rank": "Seaman Recruit", "timeframe": "0-9 months", "pay_grade": "E-1"}, {"rank": "Petty Officer 3rd Class", "timeframe": "2-3 years", "pay_grade": "E-4"}, {"rank": "Petty Officer 2nd Class", "timeframe": "4-6 years", "pay_grade": "E-5"}]'),

('combat-medic', 'Combat Medic / Healthcare Specialist', 'Army', 'Active Duty',
 'Provide emergency medical care in field conditions and support medical operations.',
 ARRAY['High school diploma', 'Physical fitness', 'Emotional resilience'],
 '4-6 months', 'challenging',
 ARRAY['medical', 'healthcare', 'help people', 'emergency', 'first aid'],
 '{"job_titles": ["Paramedic", "Emergency Medical Technician", "Medical Assistant"], "average_salary": "$45,000 - $75,000", "growth_outlook": "Excellent (15% growth)", "certifications": ["EMT", "Paramedic License", "NREMT"]}',
 '[{"rank": "Private", "timeframe": "0-6 months", "pay_grade": "E-1"}, {"rank": "Specialist", "timeframe": "2-3 years", "pay_grade": "E-4"}, {"rank": "Sergeant", "timeframe": "4-6 years", "pay_grade": "E-5"}]'),

('intelligence-analyst', 'Intelligence Analyst', 'Air Force', 'Active Duty',
 'Analyze data and information to support military operations and national security.',
 ARRAY['High school diploma', 'Top Secret clearance eligible', 'Analytical mindset'],
 '6-8 months', 'challenging',
 ARRAY['analysis', 'research', 'investigation', 'data', 'intelligence', 'problem-solving'],
 '{"job_titles": ["Data Analyst", "Intelligence Specialist", "Research Analyst"], "average_salary": "$70,000 - $120,000", "growth_outlook": "Very Good (8% growth)", "certifications": ["Security+", "Certified Intelligence Professional"]}',
 '[{"rank": "Airman Basic", "timeframe": "0-6 months", "pay_grade": "E-1"}, {"rank": "Senior Airman", "timeframe": "2-3 years", "pay_grade": "E-4"}, {"rank": "Staff Sergeant", "timeframe": "4-6 years", "pay_grade": "E-5"}]'),

('logistics-specialist', 'Supply Chain / Logistics Specialist', 'Army', 'Active Duty',
 'Manage supply chains, coordinate equipment distribution, and ensure operational readiness.',
 ARRAY['High school diploma', 'Organizational skills', 'Attention to detail'],
 '3-4 months', 'easy',
 ARRAY['logistics', 'organization', 'management', 'coordination', 'planning'],
 '{"job_titles": ["Supply Chain Manager", "Logistics Coordinator", "Operations Manager"], "average_salary": "$55,000 - $90,000", "growth_outlook": "Good (7% growth)", "certifications": ["APICS", "Supply Chain Certification"]}',
 '[{"rank": "Private", "timeframe": "0-6 months", "pay_grade": "E-1"}, {"rank": "Specialist", "timeframe": "2-3 years", "pay_grade": "E-4"}, {"rank": "Sergeant", "timeframe": "4-6 years", "pay_grade": "E-5"}]');

-- Create triggers for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_career_paths_updated_at BEFORE UPDATE ON career_paths FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a view for user statistics
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.email,
    u.created_at,
    u.last_login,
    COUNT(DISTINCT c.id) as total_conversations,
    COUNT(DISTINCT m.id) as total_messages,
    COUNT(DISTINCT sc.id) as saved_careers_count,
    COUNT(DISTINCT cf.id) as career_forecasts_count
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
LEFT JOIN messages m ON c.id = m.conversation_id
LEFT JOIN saved_careers sc ON u.id = sc.user_id
LEFT JOIN career_forecasts cf ON u.id = cf.user_id
GROUP BY u.id, u.email, u.created_at, u.last_login;

-- Grant permissions (adjust as needed for your environment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO opportunity_ai_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO opportunity_ai_user;