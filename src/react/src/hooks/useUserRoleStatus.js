import { useState, useEffect } from "react";
import useLocalStorage from "./useLocalStorage";

const useUserRoleStatus = (roleToCheck) => {
    const [status, setStatus] = useState(false);
    let role = useLocalStorage("role")
    
    useEffect(() => {
        try {
            role[0] === roleToCheck ? setStatus(true) : setStatus(false)
        } catch {
            setStatus(false)
        }
    })

  return status;
};

export default useUserRoleStatus
