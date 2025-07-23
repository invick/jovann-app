import express from 'express';

const router = express.Router();

interface UserProfile {
  id: string;
  name?: string;
  age?: number;
  education?: string;
  interests?: string[];
  militaryInterest?: {
    branches?: string[];
    serviceType?: string;
    jobCategories?: string[];
  };
  savedCareers?: string[];
  conversationHistory?: any[];
}

// Temporary in-memory storage (replace with database)
const userProfiles: Map<string, UserProfile> = new Map();

// GET /api/user/profile/:userId
router.get('/profile/:userId', (req, res) => {
  try {
    const { userId } = req.params;
    
    const profile = userProfiles.get(userId);
    
    if (!profile) {
      return res.status(404).json({ error: 'User profile not found' });
    }
    
    res.json(profile);
    
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({ error: 'Failed to retrieve user profile' });
  }
});

// PUT /api/user/profile/:userId
router.put('/profile/:userId', (req, res) => {
  try {
    const { userId } = req.params;
    const profileData = req.body;
    
    const existingProfile = userProfiles.get(userId) || { id: userId };
    
    const updatedProfile: UserProfile = {
      ...existingProfile,
      ...profileData,
      id: userId
    };
    
    userProfiles.set(userId, updatedProfile);
    
    res.json({
      message: 'Profile updated successfully',
      profile: updatedProfile
    });
    
  } catch (error) {
    console.error('Update profile error:', error);
    res.status(500).json({ error: 'Failed to update user profile' });
  }
});

// POST /api/user/save-career
router.post('/save-career', (req, res) => {
  try {
    const { userId, careerPathId } = req.body;
    
    if (!userId || !careerPathId) {
      return res.status(400).json({ error: 'User ID and career path ID are required' });
    }
    
    const profile = userProfiles.get(userId) || { id: userId, savedCareers: [] } as UserProfile;
    
    const savedCareers = profile.savedCareers || [];
    
    if (!savedCareers.includes(careerPathId)) {
      savedCareers.push(careerPathId);
    }
    
    const updatedProfile: UserProfile = {
      ...profile,
      savedCareers
    };
    
    userProfiles.set(userId, updatedProfile);
    
    res.json({
      message: 'Career saved successfully',
      savedCareers
    });
    
  } catch (error) {
    console.error('Save career error:', error);
    res.status(500).json({ error: 'Failed to save career' });
  }
});

// DELETE /api/user/saved-career/:userId/:careerPathId
router.delete('/saved-career/:userId/:careerPathId', (req, res) => {
  try {
    const { userId, careerPathId } = req.params;
    
    const profile = userProfiles.get(userId);
    
    if (!profile) {
      return res.status(404).json({ error: 'User profile not found' });
    }
    
    const savedCareers = profile.savedCareers || [];
    const updatedSavedCareers = savedCareers.filter(id => id !== careerPathId);
    
    const updatedProfile: UserProfile = {
      ...profile,
      savedCareers: updatedSavedCareers
    };
    
    userProfiles.set(userId, updatedProfile);
    
    res.json({
      message: 'Career removed from saved list',
      savedCareers: updatedSavedCareers
    });
    
  } catch (error) {
    console.error('Remove saved career error:', error);
    res.status(500).json({ error: 'Failed to remove saved career' });
  }
});

// GET /api/user/saved-careers/:userId
router.get('/saved-careers/:userId', (req, res) => {
  try {
    const { userId } = req.params;
    
    const profile = userProfiles.get(userId);
    
    if (!profile) {
      return res.status(404).json({ error: 'User profile not found' });
    }
    
    res.json({
      savedCareers: profile.savedCareers || [],
      userId
    });
    
  } catch (error) {
    console.error('Get saved careers error:', error);
    res.status(500).json({ error: 'Failed to retrieve saved careers' });
  }
});

export default router;