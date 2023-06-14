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
  <div className="wrap-fundraisers">
    {isLoggedIn ? (
      <>
        <h1 className="fundraisers-h1">Available fundraisers</h1>
        {showPopUp ? (
        <PopUp setShow={setShowPopUp} defaultBtnText="Ok">
          <h1 className="fundraisers-popup-h1">Add Team info</h1>
          <span>
            {popUpMessage}
          </span>
        </PopUp>):(<></>)}

        {helpGroups.map((group, arrayID) => 
        <>
          <div className="fundraisers-it">
            <span className="fundraisers-it-txt-30">Group poverty: {group.povertyLevel}</span>
            <span className="fundraisers-it-txt-30">Monetary Goal: {group.monetaryGoal}</span>
            <span className="fundraisers-it-txt-30">Finish Date: {group.finishDate}</span>
            <span className="fundraisers-it-txt-100">
                Donations: <select className="donations-select">
                {group.donations.map(donation => <option>{donation.date} {donation.amount}, from: {donation.donator}</option>)}
              </select>
            </span>
            <span className="fundraisers-it-txt-100">Product: {group.needs?.product}  x{group.needs?.count}</span>
            <span className="fundraisers-it-txt-50">Caretaker: {group.caretaker?.fullName} </span>
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