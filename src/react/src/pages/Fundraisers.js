import React, { useEffect, useState } from "react";
import useLocalStorage from "../hooks/useLocalStorage";
import useLoginStatus from "../hooks/useLoginStatus";
import '@fortawesome/fontawesome-free/css/all.min.css'
import PopUp from "../components/PopUp";
import axios from "axios";
import "./Fundraisers.css";
import useUserRoleStatus from "../hooks/useUserRoleStatus";

const Fundraisers = (props) => {
  const isLoggedIn = useLoginStatus()
  let personId = useLocalStorage("personId")
  let isUserDonor = useUserRoleStatus("donor")
  let isUserCaretaker = useUserRoleStatus("caretaker")

  const [showPopUp, setShowPopUp] = useState(false);
  const [popUpMessage, setPopUpMessage] = useState("")

  const [helpGroups, setHelpGroups] = useState([])

  useEffect(() => {
    axios
        .get("http://127.0.0.1:5000/fundraisers")
        .then((res) => {
          setHelpGroups(res.data.helpGroups)
        })
        .catch((err) => console.log(err));
  },[isLoggedIn,showPopUp])

  const updatePopUpMessage = (popUpMsg) => {
    setPopUpMessage(popUpMsg)
    setShowPopUp(true);
    // setEditTeamID(-1)
  }

  useEffect(() => {
    console.log(helpGroups)
  },[helpGroups])

  return (
  <div className="wrap-teams">
    {isLoggedIn ? (
      <>
        <h1 className="teams-h1">Available fundraisers</h1>
        {showPopUp ? (
        <PopUp setShow={setShowPopUp} defaultBtnText="Ok">
          <h1 className="teams-popup-h1">Add Team info</h1>
          <span>
            {popUpMessage}
          </span>
        </PopUp>):(<></>)}

        {helpGroups.map((group, arrayID) => 
        <>
          <div className="teams-it">
            <span className="teams-it-txt-100">Group poverty: {group.povertyLevel}</span>
            <span className="teams-it-txt-100">Last donation: {group.donation.date} {group.donation.note}, from: {group.donation.donator}</span>
            <span className="teams-it-txt-100">Product: {group.needs.product}  x{group.needs.count}</span>
            <span className="teams-it-txt-50">Caretaker: {group.caretaker.fullName} </span>
            <span className="teams-it-txt-50">Active Hours: {group.caretaker.activeHoursStart}-{group.caretaker.activeHoursEnd}</span>
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

export default Fundraisers;