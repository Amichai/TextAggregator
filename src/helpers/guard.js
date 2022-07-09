export const guard = (condition) => !!condition;

export const guardWithThrow = (condition, message = '') => {
  if (condition) {
    throw message || 'Error on condition.';
  }

  return false;
};

export const allow = (condition) => !condition;

export const allowOrThrow = (condition, message = '') => {
  if (!condition) {
    throw message || 'Error on condition.';
  }

  return false;
};
