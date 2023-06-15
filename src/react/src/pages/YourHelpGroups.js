import React, { useEffect, useState } from "react";
import useLocalStorage from "../hooks/useLocalStorage";
import useLoginStatus from "../hooks/useLoginStatus";
import '@fortawesome/fontawesome-free/css/all.min.css'
import PopUp from "../components/PopUp";
import axios from "axios";
import "./Fundraisers.css";
import useUserRoleStatus from "../hooks/useUserRoleStatus";
import ProgressBar from "../components/ProgressBar";

const YourHelpGroups = (props) => {
  const isLoggedIn = useLoginStatus()
  let personId = useLocalStorage("personId")
  let isUserCaretaker = useUserRoleStatus("caretaker")

  const [showPopUp, setShowPopUp] = useState(false);
  const [popUpMessage, setPopUpMessage] = useState("")

  const [yourHelpGroups, setYourHelpGroups] = useState([])

  useEffect(() => {
    axios
        .get(`http://127.0.0.1:5000/your-help-groups/${personId[0]}`)
        .then((res) => {
          setYourHelpGroups(res.data.yourHelpGroups)
        })
        .catch((err) => console.log(err));
  },[isLoggedIn,showPopUp])

  const confirm = (groupId, goalPerc) => {
    // if(goalPerc < 100.0){
    //     setPopUpMessage("Error. Process couldn't been ended, insufficient funds collected.")
    //     setShowPopUp(true)
    //     return
    // }
    axios
      .delete(`http://127.0.0.1:5000/your-help-groups/${groupId}`)
      .then((res) => {
        setPopUpMessage("Success. Process has been ended.")
        setShowPopUp(true)
      })
      .catch((err) => {
        setPopUpMessage("Error. Process couldn't been ended.")
        setShowPopUp(true)
      });
  }

  return (
  <div className="wrap-fundraisers">
    {isLoggedIn && isUserCaretaker ? (
      <>
        <h1 className="fundraisers-h1">Your Helpgroups</h1>
        <h2 className="fundraisers-h2">Keep track of monetary goal of each group, when one is fulfilled you will have to withdraw the money from our system, buy products that are listed in the fundraiser and deliver them to the Helpgroup. When finished confirm that process has been ended and Helpgroup will be no longer in the system.</h2>
        {showPopUp ? (
        <PopUp setShow={setShowPopUp} defaultBtnText="Ok">
          <h1 className="fundraisers-popup-h1">Help group information</h1>
          <span>
            {popUpMessage}
          </span>
        </PopUp>):(<></>)}

        {yourHelpGroups.map((group) => 
        <>
          <div className="fundraisers-it">
            <span className="fundraisers-it-txt-50">Group Poverty: {group.povertyLevel}</span>
            <span className="fundraisers-it-txt-50">Finish Date: {group.finishDate}</span>
            <span className="fundraisers-it-txt-100">Monetary Goal: {group.monetaryGoal}$</span>
            <ProgressBar completed={group.goalPercentage}/>
            <span className="fundraisers-it-txt-100">
                Donations: <select className="donations-select">
                {group.donations.map(donation => <option>{donation.date} {donation.amount+'$'}, from: {donation.donator}</option>)}
              </select>
            </span>
            <span className="fundraisers-it-txt-100">
                Products: <select className="donations-select">
                {group.needs.map(need => <option>{need.product}  x{need.count}</option>)}
              </select>
            </span>
            <span className="fundraisers-it-txt-50">Caretaker: You are the caretaker. </span>

            {isUserCaretaker ? (
            <div className="fundraisers-it-txt-50">
            Confirm process has been ended:
            <button className="btn-take-care" onClick={() => confirm(group.groupId,group.goalPercentage)}>
                <i className="fa-solid fa-check"></i>
            </button>
            </div>) : (<></>)}

          </div>
        </>
        )}
      </>
    ) : (
      <span className="profile-span">You've been logged out or you don't have sufficient permission to view this tab, sign in again or sign up for free!</span>
    )}
  </div>
  );
};

export default YourHelpGroups;