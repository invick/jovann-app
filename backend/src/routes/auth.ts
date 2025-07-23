import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const router = express.Router();

interface User {
  id: string;
  email: string;
  hashedPassword: string;
  profile?: {
    name?: string;
    age?: number;
    interests?: string[];
    education?: string;
  };
  createdAt: Date;
}

// Temporary in-memory user storage (replace with database)
const users: Map<string, User> = new Map();

// POST /api/auth/register
router.post('/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Check if user already exists
    const existingUser = Array.from(users.values()).find(u => u.email === email);
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);

    // Create user
    const userId = `user_${Date.now()}`;
    const newUser: User = {
      id: userId,
      email,
      hashedPassword,
      profile: {
        name: name || '',
        interests: [],
      },
      createdAt: new Date()
    };

    users.set(userId, newUser);

    // Generate JWT
    const token = jwt.sign(
      { userId, email },
      process.env.JWT_SECRET || 'default-secret',
      { expiresIn: '7d' }
    );

    res.status(201).json({
      message: 'User created successfully',
      token,
      user: {
        id: userId,
        email,
        profile: newUser.profile
      }
    });

  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Failed to create user' });
  }
});

// POST /api/auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Find user
    const user = Array.from(users.values()).find(u => u.email === email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.hashedPassword);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate JWT
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET || 'default-secret',
      { expiresIn: '7d' }
    );

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user.id,
        email: user.email,
        profile: user.profile
      }
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Failed to login' });
  }
});

// POST /api/auth/guest
router.post('/guest', (req, res) => {
  try {
    // Generate guest session
    const guestId = `guest_${Date.now()}`;
    
    const token = jwt.sign(
      { userId: guestId, isGuest: true },
      process.env.JWT_SECRET || 'default-secret',
      { expiresIn: '24h' }
    );

    res.json({
      message: 'Guest session created',
      token,
      user: {
        id: guestId,
        isGuest: true
      }
    });

  } catch (error) {
    console.error('Guest session error:', error);
    res.status(500).json({ error: 'Failed to create guest session' });
  }
});

export default router;