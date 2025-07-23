const { Client } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function setupDatabase() {
  const client = new Client({
    user: process.env.DB_USER || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    database: process.env.DB_NAME || 'opportunityai',
    password: process.env.DB_PASSWORD || '198419t',
    port: process.env.DB_PORT || 5432,
  });

  try {
    console.log('Connecting to PostgreSQL database...');
    await client.connect();
    console.log('✅ Connected to database successfully!');

    // Read and execute schema
    const schemaPath = path.join(__dirname, 'database', 'schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');
    
    console.log('Executing database schema...');
    await client.query(schema);
    console.log('✅ Database schema created successfully!');

    // Test the setup
    const result = await client.query('SELECT COUNT(*) FROM career_paths');
    console.log(`✅ Found ${result.rows[0].count} career paths in database`);

  } catch (error) {
    console.error('❌ Database setup error:', error.message);
    console.log('\nTroubleshooting:');
    console.log('1. Make sure PostgreSQL is running');
    console.log('2. Verify database "opportunityai" exists');
    console.log('3. Check your connection settings in .env file');
  } finally {
    await client.end();
  }
}

if (require.main === module) {
  setupDatabase();
}

module.exports = setupDatabase;