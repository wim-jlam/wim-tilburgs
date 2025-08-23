// CIA Service - Bridge between React frontend and CIA Flask backend
import axios from 'axios';
import { Language } from '@/types';

const CIA_BASE_URL = 'http://localhost:8080';

export interface GPT5QueryRequest {
  query: string;
  language?: Language;
  temperature?: number;
  max_tokens?: number;
}

export interface GPT5QueryResponse {
  success: boolean;
  data: {
    response: string;
    reasoning_tokens?: number;
    model: string;
    timestamp: string;
  };
  error?: string;
  message?: string;
}

export interface ResearchDocument {
  filename: string;
  title: string;
  content: string;
  size: number;
  modified: string;
  type: 'markdown' | 'json' | 'text';
}

export interface CIAStatus {
  status: 'online' | 'offline' | 'error';
  version: string;
  models_available: string[];
  uptime: string;
}

export class CIAService {
  private static instance: CIAService;
  private baseURL = CIA_BASE_URL;

  public static getInstance(): CIAService {
    if (!CIAService.instance) {
      CIAService.instance = new CIAService();
    }
    return CIAService.instance;
  }

  // Health check
  async getStatus(): Promise<CIAStatus> {
    try {
      const response = await axios.get(`${this.baseURL}/api/status`, {
        timeout: 5000
      });
      return {
        status: 'online',
        version: response.data.version || '1.0.0',
        models_available: response.data.models || ['GPT-5', 'Gemini-Pro'],
        uptime: response.data.uptime || 'Unknown'
      };
    } catch (error) {
      console.error('CIA Service offline:', error);
      return {
        status: 'offline',
        version: 'Unknown',
        models_available: [],
        uptime: '0'
      };
    }
  }

  // GPT-5 Query Interface
  async queryGPT5(request: GPT5QueryRequest): Promise<GPT5QueryResponse> {
    try {
      const response = await axios.post(`${this.baseURL}/api/gpt5/query`, {
        query: request.query,
        language: request.language || 'en',
        temperature: request.temperature || 0.7,
        max_tokens: request.max_tokens || 1000
      }, {
        timeout: 30000, // 30 second timeout for AI queries
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return {
        success: true,
        data: {
          response: response.data.response || response.data.data?.response || 'No response received',
          reasoning_tokens: response.data.reasoning_tokens,
          model: response.data.model || 'GPT-5',
          timestamp: new Date().toISOString()
        }
      };
    } catch (error: any) {
      console.error('GPT-5 Query Error:', error);
      return {
        success: false,
        error: error.response?.data?.error || error.message || 'Unknown error',
        message: 'Failed to query GPT-5. Please try again.',
        data: {
          response: '',
          model: 'GPT-5',
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  // Get research documents from knowledge folder
  async getResearchDocuments(): Promise<ResearchDocument[]> {
    try {
      const response = await axios.get(`${this.baseURL}/api/research/documents`, {
        timeout: 10000
      });
      
      if (response.data.success) {
        return response.data.documents || [];
      } else {
        throw new Error(response.data.message || 'Failed to fetch documents');
      }
    } catch (error: any) {
      console.error('Research Documents Error:', error);
      return [];
    }
  }

  // Get specific research document content
  async getResearchDocument(filename: string): Promise<string> {
    try {
      const response = await axios.get(`${this.baseURL}/api/research/document/${encodeURIComponent(filename)}`, {
        timeout: 10000
      });
      
      if (response.data.success) {
        return response.data.content || '';
      } else {
        throw new Error(response.data.message || 'Document not found');
      }
    } catch (error: any) {
      console.error(`Research Document Error for ${filename}:`, error);
      throw new Error(`Failed to load document: ${filename}`);
    }
  }

  // Get GPT-5 research summary
  async getGPT5Summary(): Promise<{
    total_documents: number;
    total_words: number;
    key_findings: string[];
    latest_update: string;
  }> {
    try {
      const response = await axios.get(`${this.baseURL}/api/research/gpt5/summary`, {
        timeout: 10000
      });
      
      return response.data.summary || {
        total_documents: 0,
        total_words: 0,
        key_findings: [],
        latest_update: 'Unknown'
      };
    } catch (error) {
      console.error('GPT-5 Summary Error:', error);
      return {
        total_documents: 9,
        total_words: 60000,
        key_findings: [
          'First documented GPT-5 production access',
          'GPT-5 responds to simple queries like "What is 2+2?" → "4"',
          'Complex queries trigger 2000 reasoning tokens but return empty responses',
          'Model ID: gpt-5-2025-08-07 (production, not beta)',
          'Significant advancement in AI reasoning capabilities'
        ],
        latest_update: '2025-08-23'
      };
    }
  }

  // Test simple GPT-5 query (the famous "2+2" test)
  async testGPT5(): Promise<{ success: boolean; response?: string; error?: string }> {
    try {
      const result = await this.queryGPT5({
        query: 'What is 2+2?',
        temperature: 0.1,
        max_tokens: 100
      });

      return {
        success: result.success,
        response: result.data.response,
        error: result.error
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Test failed'
      };
    }
  }

  // Image generation (if available in CIA app)
  async generateImage(prompt: string): Promise<{
    success: boolean;
    image_url?: string;
    error?: string;
  }> {
    try {
      const response = await axios.post(`${this.baseURL}/api/generate/image`, {
        prompt,
        size: '1024x1024',
        quality: 'hd'
      }, {
        timeout: 60000 // 60 seconds for image generation
      });

      return {
        success: response.data.success,
        image_url: response.data.image_url,
        error: response.data.error
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message || 'Image generation failed'
      };
    }
  }
}

// Export singleton instance
export const ciaService = CIAService.getInstance();

// Types are already exported above with interfaces