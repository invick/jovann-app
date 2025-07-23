import express from 'express';
import axios from 'axios';

const router = express.Router();

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatRequest {
  message: string;
  userId?: string;
  conversationHistory?: ChatMessage[];
}

// POST /api/chat/message
router.post('/message', async (req, res) => {
  try {
    const { message, userId, conversationHistory = [] }: ChatRequest = req.body;

    if (!message || message.trim().length === 0) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Add user message to history
    const updatedHistory: ChatMessage[] = [
      ...conversationHistory,
      {
        role: 'user',
        content: message,
        timestamp: new Date()
      }
    ];

    // Call AI engine
    const aiEngineUrl = process.env.AI_ENGINE_URL || 'http://localhost:8000';
    
    try {
      const aiResponse = await axios.post(`${aiEngineUrl}/chat`, {
        message,
        conversation_history: updatedHistory.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      }, {
        timeout: 30000
      });

      console.log('AI Response:', aiResponse.data); // Debug log
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: aiResponse.data.response || 'No response received',
        timestamp: new Date()
      };

      const finalHistory = [...updatedHistory, assistantMessage];

      res.json({
        response: aiResponse.data.response,
        conversationHistory: finalHistory,
        recommendations: aiResponse.data.recommendations || [],
        careerPaths: aiResponse.data.career_paths || []
      });

    } catch (aiError) {
      console.error('AI Engine Error:', aiError);
      
      // Fallback response if AI engine is unavailable
      const fallbackResponse = generateFallbackResponse(message);
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: fallbackResponse,
        timestamp: new Date()
      };

      res.json({
        response: fallbackResponse,
        conversationHistory: [...updatedHistory, assistantMessage],
        recommendations: [],
        careerPaths: []
      });
    }

  } catch (error) {
    console.error('Chat endpoint error:', error);
    res.status(500).json({ error: 'Failed to process chat message' });
  }
});

// Simple fallback response generator
function generateFallbackResponse(message: string): string {
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('aviation') || lowerMessage.includes('pilot')) {
    return 'Aviation is an exciting field in the military! There are pilot positions, air traffic control, aircraft maintenance, and many technical roles. Would you like to learn more about any specific aviation career?';
  }
  
  if (lowerMessage.includes('cyber') || lowerMessage.includes('technology') || lowerMessage.includes('computer')) {
    return 'Cybersecurity and technology roles are in high demand! The military offers excellent training in IT, cybersecurity, network administration, and software development. These skills translate very well to civilian careers.';
  }
  
  if (lowerMessage.includes('medical') || lowerMessage.includes('health')) {
    return 'Military medical careers include medics, nurses, doctors, dental specialists, and medical technicians. The training is world-class and provides excellent civilian career opportunities in healthcare.';
  }
  
  return 'That\'s a great question! Military service offers many career paths with excellent training and civilian job prospects. Would you like to explore specific areas like technology, aviation, medical, logistics, or leadership roles?';
}

// GET /api/chat/conversation/:userId
router.get('/conversation/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    // TODO: Implement database retrieval of conversation history
    // For now, return empty array
    res.json({
      conversationHistory: [],
      userId
    });
    
  } catch (error) {
    console.error('Get conversation error:', error);
    res.status(500).json({ error: 'Failed to retrieve conversation' });
  }
});

export default router;