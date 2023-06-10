import { useState, useEffect } from "react";

const useLocalStorageStatus = (item) => {
  const [status, setStatus] = useState(false);
  useEffect(() => {
    const getLoginStatus = () => {
      if (localStorage.getItem(item)) setStatus(true);
      else setStatus(false);
    };
    getLoginStatus();
  });
  return status;
};

export default useLocalStorageStatus;
