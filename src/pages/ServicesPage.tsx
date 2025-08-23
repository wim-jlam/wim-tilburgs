import React from 'react';
import { useTranslation } from 'react-i18next';

const ServicesPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-white py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {t('services.title')}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            {t('services.subtitle')}
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-20 text-gray-500">
            =¼ Smart Health Consulting services komen hier...
            <br />
            <small className="text-sm">( AI Strategy, Implementation, Training</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServicesPage;