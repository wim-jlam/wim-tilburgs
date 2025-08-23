import React from 'react';
import { useTranslation } from 'react-i18next';

const ContactPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50 py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {t('nav.contact')}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get in touch for AI health consulting or collaboration
          </p>
        </div>
        
        <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-lg p-8">
          <div className="text-center py-12 text-gray-500">
            =è Contact form komt hier...
            <br />
            <small className="text-sm">Email, LinkedIn, consulting inquiry form</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;