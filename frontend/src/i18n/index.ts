export const t = (key: string, lang = 'en') => {
  const translations: Record<string, Record<string, string>> = {
    en: {
      signal: "Signal",
      confidence: "Confidence",
      message: "Custom Message",
      schedule: "Signal Schedule",
      trustLevel: "Trust Level",
      addPair: "Add Trading Pair"
    },
    he: {
      signal: "סיגנל",
      confidence: "רמת ביטחון",
      message: "הודעה מותאמת אישית",
      schedule: "תזמון סיגנלים",
      trustLevel: "רמת אמינות",
      addPair: "הוסף זוג מסחר"
    },
  };

  return translations[lang]?.[key] || key;
};