import { useState, useEffect } from "react";

const getStorageValue = (key, defaultValue) => {
  const saved = localStorage.getItem(key);
  return saved || defaultValue;
}

const useLocalStorage = (key, defaultValue) => {
  const [value, setValue] = useState(() => {
    return getStorageValue(key, defaultValue);
  });

  useEffect(() => {
    localStorage.setItem(key, value);
  }, [key, value]);

  return [value, setValue];
};

export default useLocalStorage