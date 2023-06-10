import React from "react";
import "./PopUp.css";

const PopUp = ({children, setShow, customFunction, customFunctionBtnText, defaultBtnText}) => {

  return (
    <div className={"popup"}>
      {children}
      <div className="button-div">
        {customFunction ? (
          <button className="btn-popup" onClick={() => { customFunction(); setShow(false); }}>
            {customFunctionBtnText}
          </button> ) : (<></>)
        }
        <button className="btn-popup" onClick={() => setShow(false)}>
          {defaultBtnText}
        </button>
      </div>
    </div>
  );
};

export default PopUp;
