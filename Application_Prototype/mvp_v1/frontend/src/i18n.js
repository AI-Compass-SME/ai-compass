import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import enTranslations from './locales/en.json';
import deTranslations from './locales/de.json';

i18n
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources: {
            en: { translation: enTranslations },
            de: { translation: deTranslations }
        },
        fallbackLng: 'de',
        detection: {
            order: ['querystring', 'localStorage'],
            lookupQuerystring: 'lang',
            caches: ['localStorage'],
        },
        interpolation: {
            escapeValue: false // react already safes from xss
        }
    });

export default i18n;
