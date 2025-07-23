import express from 'express';

const router = express.Router();

interface CareerPath {
  id: string;
  title: string;
  branch: 'Army' | 'Navy' | 'Air Force' | 'Marines' | 'Space Force' | 'Coast Guard';
  serviceType: 'Active Duty' | 'National Guard' | 'Reserves';
  description: string;
  requirements: string[];
  trainingDuration: string;
  promotionTimeline: {
    rank: string;
    timeframe: string;
    payGrade: string;
  }[];
  civilianTranslation: {
    jobTitles: string[];
    industries: string[];
    averageSalary: string;
  };
  certifications: string[];
}

// Sample career data
const careerPaths: CareerPath[] = [
  {
    id: 'cyber-operations',
    title: 'Cybersecurity Specialist',
    branch: 'Air Force',
    serviceType: 'Active Duty',
    description: 'Protect military networks and systems from cyber threats, conduct digital forensics, and implement security measures.',
    requirements: ['High school diploma', 'Security clearance eligible', 'ASVAB Electronics score 60+'],
    trainingDuration: '6-12 months technical training',
    promotionTimeline: [
      { rank: 'Airman Basic', timeframe: '0-6 months', payGrade: 'E-1' },
      { rank: 'Senior Airman', timeframe: '2-3 years', payGrade: 'E-4' },
      { rank: 'Staff Sergeant', timeframe: '4-6 years', payGrade: 'E-5' }
    ],
    civilianTranslation: {
      jobTitles: ['Cybersecurity Analyst', 'Information Security Manager', 'Digital Forensics Investigator'],
      industries: ['Technology', 'Finance', 'Government', 'Healthcare'],
      averageSalary: '$85,000 - $140,000'
    },
    certifications: ['Security+', 'CISSP', 'CEH']
  },
  {
    id: 'aviation-mechanic',
    title: 'Aircraft Maintenance Technician',
    branch: 'Navy',
    serviceType: 'Active Duty',
    description: 'Maintain, repair, and inspect military aircraft to ensure flight safety and mission readiness.',
    requirements: ['High school diploma', 'Mechanical aptitude', 'Physical fitness standards'],
    trainingDuration: '4-6 months technical school',
    promotionTimeline: [
      { rank: 'Seaman Recruit', timeframe: '0-9 months', payGrade: 'E-1' },
      { rank: 'Petty Officer 3rd Class', timeframe: '2-3 years', payGrade: 'E-4' },
      { rank: 'Petty Officer 2nd Class', timeframe: '4-6 years', payGrade: 'E-5' }
    ],
    civilianTranslation: {
      jobTitles: ['Aircraft Mechanic', 'Aviation Technician', 'Maintenance Supervisor'],
      industries: ['Airlines', 'Aerospace Manufacturing', 'Private Aviation'],
      averageSalary: '$65,000 - $95,000'
    },
    certifications: ['A&P License', 'FAA Certifications']
  }
];

// GET /api/career/paths
router.get('/paths', (req, res) => {
  try {
    const { branch, serviceType, category } = req.query;
    
    let filteredPaths = [...careerPaths];
    
    if (branch) {
      filteredPaths = filteredPaths.filter(path => 
        path.branch.toLowerCase() === (branch as string).toLowerCase()
      );
    }
    
    if (serviceType) {
      filteredPaths = filteredPaths.filter(path => 
        path.serviceType.toLowerCase() === (serviceType as string).toLowerCase()
      );
    }
    
    res.json({
      careerPaths: filteredPaths,
      total: filteredPaths.length
    });
    
  } catch (error) {
    console.error('Get career paths error:', error);
    res.status(500).json({ error: 'Failed to retrieve career paths' });
  }
});

// GET /api/career/path/:id
router.get('/path/:id', (req, res) => {
  try {
    const { id } = req.params;
    
    const careerPath = careerPaths.find(path => path.id === id);
    
    if (!careerPath) {
      return res.status(404).json({ error: 'Career path not found' });
    }
    
    res.json(careerPath);
    
  } catch (error) {
    console.error('Get career path error:', error);
    res.status(500).json({ error: 'Failed to retrieve career path' });
  }
});

// POST /api/career/forecast
router.post('/forecast', (req, res) => {
  try {
    const { careerPathId, serviceYears = 4 } = req.body;
    
    const careerPath = careerPaths.find(path => path.id === careerPathId);
    
    if (!careerPath) {
      return res.status(404).json({ error: 'Career path not found' });
    }
    
    // Generate 4-year forecast
    const forecast = {
      careerPath: careerPath.title,
      branch: careerPath.branch,
      serviceType: careerPath.serviceType,
      timeline: [
        {
          year: 1,
          milestone: 'Basic Training & Technical School',
          rank: careerPath.promotionTimeline[0]?.rank || 'Entry Level',
          estimatedPay: '$25,000 - $30,000',
          skills: ['Basic military training', 'Technical foundations', 'Security clearance']
        },
        {
          year: 2,
          milestone: 'First Duty Assignment',
          rank: careerPath.promotionTimeline[0]?.rank || 'Junior Enlisted',
          estimatedPay: '$30,000 - $40,000',
          skills: ['On-the-job experience', 'Specialized training', 'Leadership basics']
        },
        {
          year: 3,
          milestone: 'Advanced Training & Promotion',
          rank: careerPath.promotionTimeline[1]?.rank || 'Mid-Level',
          estimatedPay: '$40,000 - $50,000',
          skills: ['Advanced technical skills', 'Mentoring junior personnel', 'Professional development']
        },
        {
          year: 4,
          milestone: 'Leadership Role & Specialization',
          rank: careerPath.promotionTimeline[2]?.rank || 'Senior Enlisted',
          estimatedPay: '$50,000 - $65,000',
          skills: ['Team leadership', 'Project management', 'Industry certifications']
        }
      ],
      civilianOutcome: {
        readiness: 'High',
        expectedSalary: careerPath.civilianTranslation.averageSalary,
        jobOpportunities: careerPath.civilianTranslation.jobTitles,
        certifications: careerPath.certifications
      }
    };
    
    res.json(forecast);
    
  } catch (error) {
    console.error('Career forecast error:', error);
    res.status(500).json({ error: 'Failed to generate career forecast' });
  }
});

export default router;