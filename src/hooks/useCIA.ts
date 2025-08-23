// Custom React hooks for CIA service integration
import { useState, useEffect, useCallback } from 'react';
import { ciaService, GPT5QueryRequest, GPT5QueryResponse, ResearchDocument, CIAStatus } from '@/services/cia';

// Hook for CIA service status
export const useCIAStatus = () => {
  const [status, setStatus] = useState<CIAStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = useCallback(async () => {
    try {
      setLoading(true);
      const statusData = await ciaService.getStatus();
      setStatus(statusData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to check CIA status');
      setStatus(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkStatus();
    // Check status every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, [checkStatus]);

  return { status, loading, error, refetch: checkStatus };
};

// Hook for GPT-5 queries
export const useGPT5Query = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastResponse, setLastResponse] = useState<GPT5QueryResponse | null>(null);

  const queryGPT5 = useCallback(async (request: GPT5QueryRequest): Promise<GPT5QueryResponse> => {
    try {
      setLoading(true);
      setError(null);
      const response = await ciaService.queryGPT5(request);
      setLastResponse(response);
      
      if (!response.success) {
        setError(response.error || 'Query failed');
      }
      
      return response;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to query GPT-5';
      setError(errorMsg);
      const errorResponse: GPT5QueryResponse = {
        success: false,
        error: errorMsg,
        data: {
          response: '',
          model: 'GPT-5',
          timestamp: new Date().toISOString()
        }
      };
      setLastResponse(errorResponse);
      return errorResponse;
    } finally {
      setLoading(false);
    }
  }, []);

  const testGPT5 = useCallback(async () => {
    return await queryGPT5({
      query: 'What is 2+2?',
      temperature: 0.1,
      max_tokens: 100
    });
  }, [queryGPT5]);

  return {
    queryGPT5,
    testGPT5,
    loading,
    error,
    lastResponse,
    clearError: () => setError(null)
  };
};

// Hook for research documents
export const useResearchDocuments = () => {
  const [documents, setDocuments] = useState<ResearchDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    try {
      setLoading(true);
      const docs = await ciaService.getResearchDocuments();
      setDocuments(docs);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch research documents');
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  return { documents, loading, error, refetch: fetchDocuments };
};

// Hook for specific research document
export const useResearchDocument = (filename: string | null) => {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDocument = useCallback(async (docFilename: string) => {
    try {
      setLoading(true);
      setError(null);
      const documentContent = await ciaService.getResearchDocument(docFilename);
      setContent(documentContent);
    } catch (err: any) {
      setError(err.message || `Failed to fetch ${docFilename}`);
      setContent('');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (filename) {
      fetchDocument(filename);
    } else {
      setContent('');
      setError(null);
    }
  }, [filename, fetchDocument]);

  return { content, loading, error, refetch: filename ? () => fetchDocument(filename) : () => {} };
};

// Hook for GPT-5 research summary
export const useGPT5Summary = () => {
  const [summary, setSummary] = useState<{
    total_documents: number;
    total_words: number;
    key_findings: string[];
    latest_update: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = useCallback(async () => {
    try {
      setLoading(true);
      const summaryData = await ciaService.getGPT5Summary();
      setSummary(summaryData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch GPT-5 summary');
      setSummary(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSummary();
  }, [fetchSummary]);

  return { summary, loading, error, refetch: fetchSummary };
};