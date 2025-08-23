import React from 'react';
import { useTranslation } from 'react-i18next';

const AboutPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-white py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {t('about.title')}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Van diabeet naar AI health pioneer - mijn transformatiereis
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-20 text-gray-500">
            About page content wordt hier geladen...
            <br />
            <small className="text-sm">( Coming soon - Wim's transformatie verhaal</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;