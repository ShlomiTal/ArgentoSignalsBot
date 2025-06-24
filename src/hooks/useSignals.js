import { useState, useCallback } from 'react';
import { getSignals } from '../utils/api';

export const useSignals = () => {
  const [signals, setSignals] = useState([]);

  const fetchSignals = useCallback(async () => {
    try {
      const data = await getSignals();
      setSignals(data);
    } catch (error) {
      console.error('Error fetching signals:', error);
    }
  }, []);

  return { signals, fetchSignals };
};