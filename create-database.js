const { Client } = require('pg');
require('dotenv').config();

async function createDatabase() {
  // First connect to default postgres database to create our database
  const adminClient = new Client({
    user: process.env.DB_USER || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    database: 'postgres', // Connect to default database first
    password: process.env.DB_PASSWORD || '198419t',
    port: process.env.DB_PORT || 5432,
  });

  try {
    console.log('Connecting to PostgreSQL server...');
    await adminClient.connect();
    console.log('✅ Connected to PostgreSQL server!');

    // Check if database exists
    const dbCheckResult = await adminClient.query(
      "SELECT 1 FROM pg_database WHERE datname = 'opportunityai'"
    );

    if (dbCheckResult.rows.length === 0) {
      console.log('Creating opportunityai database...');
      await adminClient.query('CREATE DATABASE opportunityai');
      console.log('✅ Database "opportunityai" created successfully!');
    } else {
      console.log('✅ Database "opportunityai" already exists!');
    }

  } catch (error) {
    console.error('❌ Database creation error:', error.message);
    console.log('\nTroubleshooting:');
    console.log('1. Make sure PostgreSQL is running on localhost:5432');
    console.log('2. Verify username "postgres" and password are correct');
    console.log('3. Check if PostgreSQL service is started');
  } finally {
    await adminClient.end();
  }
}

if (require.main === module) {
  createDatabase();
}

module.exports = createDatabase;