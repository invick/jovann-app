export const API_CONFIG = {
  BASE_URL: 'http://localhost:3001/api',
  TIMEOUT: 10000,
  ENDPOINTS: {
    CHAT: '/chat/message',
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      GUEST: '/auth/guest'
    },
    CAREER: {
      PATHS: '/career/paths',
      FORECAST: '/career/forecast'
    },
    USER: {
      PROFILE: '/user/profile',
      SAVE_CAREER: '/user/save-career'
    }
  }
};

export const getApiUrl = (endpoint: string) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};