export const formatPrice = (price) => `$${price.toFixed(2)}`;
export const formatConfidence = (confidence) => `${(confidence * 100).toFixed(2)}%`;
export const formatDate = (date) => new Date(date).toLocaleString();