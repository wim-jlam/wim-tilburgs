import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
const nlTranslations = require('./locales/nl.json');
const enTranslations = require('./locales/en.json');

// Language detection options
const detection = {
  order: ['localStorage', 'navigator', 'htmlTag'],
  lookupLocalStorage: 'preferred-language',
  caches: ['localStorage'],
  excludeCacheFor: ['cimode'],
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    detection,
    resources: {
      nl: {
        translation: nlTranslations,
      },
      en: {
        translation: enTranslations,
      },
    },
    lng: 'nl', // Default language
    fallbackLng: 'nl',
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false, // React already escapes
    },
    
    react: {
      useSuspense: false,
    },
  });

export default i18n;