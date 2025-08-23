import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useAIMotor, useMotorQuery, useMotorStats, useMotorRecommendation } from '@/hooks/useAIMotor';
import { AIMotor } from '@/services/aiMotor';
import LoadingSpinner from '@/components/common/LoadingSpinner';

const LabPage: React.FC = () => {
  const { t } = useTranslation();
  const { currentMotor, availableMotors, selectMotor } = useAIMotor();
  const { 
    executeQuery, 
    testCurrentMotor, 
    queryHealthAI,
    loading, 
    lastResponse, 
    queryHistory 
  } = useMotorQuery();
  const { stats } = useMotorStats();
  const { recommendation, analyzeQuery } = useMotorRecommendation();
  
  const [query, setQuery] = useState('');
  const [selectedMotorId, setSelectedMotorId] = useState(currentMotor.id);
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Update motor when selection changes
  useEffect(() => {
    if (selectedMotorId !== currentMotor.id) {
      selectMotor(selectedMotorId);
    }
  }, [selectedMotorId, currentMotor.id, selectMotor]);

  // Analyze query for motor recommendation
  useEffect(() => {
    if (query.length > 10) {
      analyzeQuery(query);
    }
  }, [query, analyzeQuery]);

  const handleQuery = async () => {
    if (!query.trim()) return;
    await executeQuery({ query });
  };

  const handleQuickTest = async () => {
    await testCurrentMotor();
  };

  const handleHealthAIQuery = async () => {
    await queryHealthAI("What are the latest applications of AI in diabetes management?");
  };

  const MotorCard: React.FC<{ motor: AIMotor; isSelected: boolean; onSelect: () => void }> = ({ 
    motor, 
    isSelected, 
    onSelect 
  }) => (
    <div 
      className={`cursor-pointer transition-all duration-200 ${
        isSelected 
          ? `bg-gradient-to-br ${motor.color.primary} text-white shadow-xl scale-105` 
          : `bg-white hover:shadow-lg border ${motor.color.secondary}`
      } rounded-xl p-6`}
      onClick={onSelect}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="text-3xl">{motor.icon}</div>
        <div className={`px-2 py-1 rounded-full text-xs ${
          isSelected ? 'bg-white/20 text-white' : `${motor.color.accent} bg-opacity-10`
        }`}>
          {motor.type.charAt(0).toUpperCase() + motor.type.slice(1)}
        </div>
      </div>
      
      <h3 className={`text-lg font-bold mb-2 ${isSelected ? 'text-white' : 'text-gray-900'}`}>
        {motor.name}
      </h3>
      
      <p className={`text-sm mb-4 ${isSelected ? 'text-white/90' : 'text-gray-600'}`}>
        {motor.tagline}
      </p>
      
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className={`text-center p-2 rounded ${
          isSelected ? 'bg-white/10' : 'bg-gray-50'
        }`}>
          <div className={`font-bold ${isSelected ? 'text-white' : 'text-gray-900'}`}>
            {motor.processingPower}/10
          </div>
          <div className={`text-xs ${isSelected ? 'text-white/80' : 'text-gray-600'}`}>
            Power
          </div>
        </div>
        <div className={`text-center p-2 rounded ${
          isSelected ? 'bg-white/10' : 'bg-gray-50'
        }`}>
          <div className={`font-bold ${isSelected ? 'text-white' : 'text-gray-900'}`}>
            {motor.knowledgeAccess}/5
          </div>
          <div className={`text-xs ${isSelected ? 'text-white/80' : 'text-gray-600'}`}>
            Depth
          </div>
        </div>
      </div>
      
      <div className={`text-xs ${isSelected ? 'text-white/80' : 'text-gray-500'}`}>
        {motor.stats.analysesCompleted.toLocaleString()} analyses completed
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-4">
            <div className="text-4xl mr-4">{currentMotor.icon}</div>
            <h1 className="text-4xl font-bold text-gray-900">
              AI Research Laboratory
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Select your AI Motor and explore the future of health AI with GPT-5 research
          </p>
          
          {/* Current Motor Status */}
          <div className="mt-6 inline-flex items-center px-6 py-3 bg-white rounded-full shadow-lg">
            <div className="w-3 h-3 rounded-full mr-3 bg-green-500 animate-pulse"></div>
            <span className="text-sm text-gray-700 font-medium">
              Active: {currentMotor.name}
            </span>
            <div className={`ml-3 px-3 py-1 rounded-full text-xs font-medium ${
              currentMotor.color.secondary
            } ${currentMotor.color.accent}`}>
              {currentMotor.reasoningDepth} reasoning
            </div>
          </div>
        </div>

        {/* AI Motor Selection */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Choose Your AI Motor
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {availableMotors.map((motor) => (
              <MotorCard
                key={motor.id}
                motor={motor}
                isSelected={motor.id === currentMotor.id}
                onSelect={() => setSelectedMotorId(motor.id)}
              />
            ))}
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-xl p-6 shadow-lg text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {stats.totalAnalyses.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Total Analyses</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-lg text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {stats.totalInsights.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Insights Generated</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-lg text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {stats.totalProblems.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Problems Solved</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-lg text-center">
            <div className="text-3xl font-bold text-orange-600 mb-2">
              {(stats.averageInsightQuality * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">Insight Quality</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                🧪 Quick Tests
              </h3>
              <div className="space-y-3">
                <button
                  onClick={handleQuickTest}
                  disabled={loading}
                  className="w-full bg-yellow-500 text-white py-3 px-4 rounded-lg hover:bg-yellow-600 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Testing...' : 'Famous "2+2" Test'}
                </button>
                <button
                  onClick={handleHealthAIQuery}
                  disabled={loading}
                  className="w-full bg-green-500 text-white py-3 px-4 rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50"
                >
                  Health AI Sample
                </button>
                <button
                  onClick={() => setQuery('Analyze the latest GPT-5 capabilities for medical diagnosis')}
                  className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg hover:bg-blue-600 transition-colors"
                >
                  Load GPT-5 Research Query
                </button>
              </div>
            </div>

            {/* Motor Capabilities */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                {currentMotor.icon} Current Capabilities
              </h3>
              <div className="space-y-2">
                {currentMotor.capabilities.map((capability) => (
                  <div key={capability} className="flex items-center text-sm">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                    <span className="capitalize">{capability.replace('_', ' ')}</span>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="text-sm text-gray-600">
                  <div className="flex justify-between mb-1">
                    <span>Max Tokens:</span>
                    <span className="font-medium">{currentMotor.maxTokens.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Reasoning:</span>
                    <span className="font-medium capitalize">{currentMotor.reasoningDepth}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Query Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-gray-900">
                  🤖 {currentMotor.name} Interface
                </h3>
                <button
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
                >
                  {showAdvanced ? 'Simple' : 'Advanced'}
                </button>
              </div>

              {/* Motor Recommendation */}
              {recommendation.recommendedMotor && recommendation.recommendedMotor.id !== currentMotor.id && (
                <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                  <div className="flex items-start">
                    <div className="text-xl mr-3">{recommendation.recommendedMotor.icon}</div>
                    <div className="flex-1">
                      <h4 className="font-medium text-amber-900 mb-1">
                        Recommended: {recommendation.recommendedMotor.name}
                      </h4>
                      <p className="text-sm text-amber-700 mb-2">
                        {recommendation.reason}
                      </p>
                      <button
                        onClick={() => setSelectedMotorId(recommendation.recommendedMotor!.id)}
                        className="text-sm bg-amber-600 text-white px-3 py-1 rounded hover:bg-amber-700 transition-colors"
                      >
                        Switch Motor
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Query Interface */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Query for {currentMotor.name}:
                  </label>
                  <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={`Ask ${currentMotor.name} about AI health research, GPT-5 capabilities, or complex analysis...`}
                    className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    rows={4}
                  />
                </div>
                
                {showAdvanced && (
                  <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Temperature: 0.7
                      </label>
                      <input type="range" min="0" max="1" step="0.1" defaultValue="0.7" className="w-full" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Use Reasoning Tokens
                      </label>
                      <label className="flex items-center mt-2">
                        <input type="checkbox" defaultChecked className="mr-2" />
                        <span className="text-sm">Enable deep reasoning</span>
                      </label>
                    </div>
                  </div>
                )}

                <button
                  onClick={handleQuery}
                  disabled={loading || !query.trim()}
                  className={`w-full py-4 px-6 rounded-lg transition-colors text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed bg-gradient-to-r ${currentMotor.color.primary} hover:shadow-lg`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <LoadingSpinner size="sm" />
                      <span className="ml-2">Processing with {currentMotor.name}...</span>
                    </span>
                  ) : (
                    `Activate ${currentMotor.name}`
                  )}
                </button>
              </div>

              {/* Response Display */}
              {lastResponse && (
                <div className="mt-8 p-6 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <span className="text-xl mr-2">{currentMotor.icon}</span>
                      <h4 className="font-medium text-gray-900">{lastResponse.data.motorUsed} Response:</h4>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-3 py-1 text-xs rounded-full ${
                        lastResponse.success 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {lastResponse.success ? 'Success' : 'Error'}
                      </span>
                      {lastResponse.data.insightQuality > 0 && (
                        <span className="px-3 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                          Quality: {(lastResponse.data.insightQuality * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>
                  </div>
                  
                  {lastResponse.success ? (
                    <div>
                      <div className="prose prose-sm max-w-none text-gray-900 mb-4">
                        <div className="whitespace-pre-wrap">{lastResponse.data.response}</div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-500 pt-4 border-t border-gray-200">
                        <div className="flex items-center space-x-4">
                          <span>Processing: {lastResponse.data.processingTime}ms</span>
                          <span>Tokens: {lastResponse.data.tokensUsed}</span>
                          {lastResponse.data.reasoningTokens && (
                            <span>Reasoning: {lastResponse.data.reasoningTokens}</span>
                          )}
                        </div>
                        <span>{new Date(lastResponse.data.timestamp).toLocaleTimeString()}</span>
                      </div>
                    </div>
                  ) : (
                    <div className="text-red-600">
                      <p className="mb-2">⚠️ Motor Processing Error:</p>
                      <p className="text-sm">{lastResponse.error || 'Unknown error occurred'}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Built with AI Section */}
        <div className="mt-16 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">
            🤖 Built Entirely With AI - Zero Human Code
          </h3>
          <p className="text-lg opacity-90 mb-6 max-w-4xl mx-auto">
            This entire platform - every component, every interaction, every design decision - was created 
            through AI collaboration. A living demonstration of AI's capability to build complex, functional systems.
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-2xl mb-2">🧠</div>
              <div className="font-semibold">GPT-5</div>
              <div className="text-sm opacity-75">Research Engine</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-2xl mb-2">💻</div>
              <div className="font-semibold">Claude</div>
              <div className="text-sm opacity-75">Code Generation</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-2xl mb-2">🎨</div>
              <div className="font-semibold">DALL-E 3</div>
              <div className="text-sm opacity-75">Visual Design</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-2xl mb-2">🌐</div>
              <div className="font-semibold">Gemini Pro</div>
              <div className="text-sm opacity-75">Translation</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-2xl mb-2">⚡</div>
              <div className="font-semibold">Cursor</div>
              <div className="text-sm opacity-75">AI IDE</div>
            </div>
          </div>

          <div className="text-sm opacity-75 mb-4">
            Tech Stack: React + TypeScript + Tailwind CSS + PostgreSQL + FastAPI
          </div>
          <div className="text-xs opacity-60">
            "From diabetes patient to AI health pioneer - powered entirely by artificial intelligence"
          </div>
        </div>
      </div>
    </div>
  );
};

export default LabPage;