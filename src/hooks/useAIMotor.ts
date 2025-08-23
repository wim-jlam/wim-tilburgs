// AI Motor React hooks - "Stolen" functionality from CIA app 😄
import { useState, useEffect, useCallback } from 'react';
import { 
  aiMotorService, 
  AIMotor, 
  MotorQuery, 
  MotorResponse, 
  MotorType 
} from '@/services/aiMotor';

// Hook for managing current AI Motor
export const useAIMotor = () => {
  const [currentMotor, setCurrentMotor] = useState<AIMotor>(aiMotorService.getCurrentMotor());
  const [availableMotors, setAvailableMotors] = useState<AIMotor[]>(aiMotorService.getAvailableMotors());

  const selectMotor = useCallback((motorId: string) => {
    const motor = aiMotorService.selectMotor(motorId);
    if (motor) {
      setCurrentMotor(motor);
    }
  }, []);

  const recommendMotor = useCallback((queryType: 'research' | 'development' | 'enterprise') => {
    const recommended = aiMotorService.recommendMotor(queryType);
    return recommended;
  }, []);

  return {
    currentMotor,
    availableMotors,
    selectMotor,
    recommendMotor
  };
};

// Hook for executing AI Motor queries (stolen from CIA queryGPT5)
export const useMotorQuery = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastResponse, setLastResponse] = useState<MotorResponse | null>(null);
  const [queryHistory, setQueryHistory] = useState<MotorResponse[]>([]);

  const executeQuery = useCallback(async (query: MotorQuery): Promise<MotorResponse> => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await aiMotorService.executeQuery(query);
      setLastResponse(response);
      
      // Add to history
      setQueryHistory(prev => [response, ...prev.slice(0, 9)]); // Keep last 10
      
      if (!response.success) {
        setError(response.error || 'Motor processing failed');
      }
      
      return response;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to execute motor query';
      setError(errorMsg);
      
      const errorResponse: MotorResponse = {
        success: false,
        error: errorMsg,
        data: {
          response: '',
          motorUsed: aiMotorService.getCurrentMotor().name,
          processingTime: 0,
          tokensUsed: 0,
          insightQuality: 0,
          capabilities: aiMotorService.getCurrentMotor().capabilities,
          timestamp: new Date().toISOString()
        }
      };
      
      setLastResponse(errorResponse);
      setQueryHistory(prev => [errorResponse, ...prev.slice(0, 9)]);
      
      return errorResponse;
    } finally {
      setLoading(false);
    }
  }, []);

  // Famous 2+2 test (stolen from CIA testGPT5)
  const testCurrentMotor = useCallback(async () => {
    return await executeQuery({
      query: 'What is 2+2?',
      temperature: 0.1,
      useReasoningTokens: true
    });
  }, [executeQuery]);

  // Quick health AI query
  const queryHealthAI = useCallback(async (healthQuery: string) => {
    return await executeQuery({
      query: `Health AI Analysis: ${healthQuery}`,
      capability: 'health_research',
      useReasoningTokens: true
    });
  }, [executeQuery]);

  // GPT-5 research query
  const queryGPT5Research = useCallback(async (researchQuery: string) => {
    return await executeQuery({
      query: `GPT-5 Research: ${researchQuery}`,
      capability: 'gpt5_analysis',
      useReasoningTokens: true
    });
  }, [executeQuery]);

  const clearHistory = useCallback(() => {
    setQueryHistory([]);
    setLastResponse(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    executeQuery,
    testCurrentMotor,
    queryHealthAI,
    queryGPT5Research,
    loading,
    error,
    lastResponse,
    queryHistory,
    clearHistory,
    clearError
  };
};

// Hook for motor statistics and performance
export const useMotorStats = () => {
  const [stats, setStats] = useState<{
    totalAnalyses: number;
    totalInsights: number;
    totalProblems: number;
    averageProcessingTime: number;
    averageInsightQuality: number;
  }>({
    totalAnalyses: 0,
    totalInsights: 0, 
    totalProblems: 0,
    averageProcessingTime: 0,
    averageInsightQuality: 0
  });

  const updateStats = useCallback(() => {
    const motors = aiMotorService.getAvailableMotors();
    const totalAnalyses = motors.reduce((sum, motor) => sum + motor.stats.analysesCompleted, 0);
    const totalInsights = motors.reduce((sum, motor) => sum + motor.stats.insightsGenerated, 0);
    const totalProblems = motors.reduce((sum, motor) => sum + motor.stats.problemsSolved, 0);

    setStats({
      totalAnalyses,
      totalInsights,
      totalProblems,
      averageProcessingTime: 1250, // Mock average
      averageInsightQuality: 0.847 // Mock quality score
    });
  }, []);

  useEffect(() => {
    updateStats();
    // Update stats every 30 seconds
    const interval = setInterval(updateStats, 30000);
    return () => clearInterval(interval);
  }, [updateStats]);

  return { stats, updateStats };
};

// Hook for motor recommendations based on query analysis
export const useMotorRecommendation = () => {
  const [recommendation, setRecommendation] = useState<{
    recommendedMotor: AIMotor | null;
    reason: string;
    confidence: number;
  }>({
    recommendedMotor: null,
    reason: '',
    confidence: 0
  });

  const analyzeQuery = useCallback((query: string) => {
    const lowerQuery = query.toLowerCase();
    
    // Research-focused queries
    if (lowerQuery.includes('research') || lowerQuery.includes('analyze') || lowerQuery.includes('study')) {
      const motor = aiMotorService.getMotorByType('research');
      setRecommendation({
        recommendedMotor: motor,
        reason: 'Your query involves research and analysis - Research Engine is optimized for deep insights.',
        confidence: 0.9
      });
      return;
    }

    // Development/building queries  
    if (lowerQuery.includes('build') || lowerQuery.includes('create') || lowerQuery.includes('develop') || lowerQuery.includes('code')) {
      const motor = aiMotorService.getMotorByType('pioneer');
      setRecommendation({
        recommendedMotor: motor,
        reason: 'You\'re building something - Pioneer Laboratory has the tools you need.',
        confidence: 0.85
      });
      return;
    }

    // Enterprise/system queries
    if (lowerQuery.includes('enterprise') || lowerQuery.includes('system') || lowerQuery.includes('architecture') || lowerQuery.includes('scale')) {
      const motor = aiMotorService.getMotorByType('architect');
      setRecommendation({
        recommendedMotor: motor,
        reason: 'System-level thinking detected - System Architect provides enterprise-grade analysis.',
        confidence: 0.8
      });
      return;
    }

    // Default to current motor
    setRecommendation({
      recommendedMotor: aiMotorService.getCurrentMotor(),
      reason: 'Using your current motor - feel free to switch if needed.',
      confidence: 0.6
    });
  }, []);

  const clearRecommendation = useCallback(() => {
    setRecommendation({
      recommendedMotor: null,
      reason: '',
      confidence: 0
    });
  }, []);

  return {
    recommendation,
    analyzeQuery,
    clearRecommendation
  };
};