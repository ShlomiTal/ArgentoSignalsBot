import { useState } from 'react';
import en from '../locales/en.json';
import he from '../locales/he.json';

const translations = { en, he };

export const useTranslation = () => {
  const [lang, setLang] = useState('en');

  const t = (key) => translations[lang][key] || key;

  return { t, setLang, lang };
};