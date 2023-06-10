import { useState, useEffect } from "react";

const RE_INT = /^-?[0-9]+$/

const useLoginStatus = () => {
  const [status, setStatus] = useState(false);
  useEffect(() => {
    const getLoginStatus = () => {
      if (localStorage.getItem("personId")?.match(RE_INT)) setStatus(true);
      else setStatus(false);
    };
    getLoginStatus();
  });
  return status;
};

export default useLoginStatus;