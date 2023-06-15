import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import useLocalStorage from "../hooks/useLocalStorage";
import useLoginStatus from "../hooks/useLoginStatus";
import '@fortawesome/fontawesome-free/css/all.min.css'
import PopUp from "../components/PopUp";
import axios from "axios";
import "./Fundraisers.css";
import useUserRoleStatus from "../hooks/useUserRoleStatus";
import ProgressBar from "../components/ProgressBar";

const Fundraisers = (props) => {
  const isLoggedIn = useLoginStatus()
  let personId = useLocalStorage("personId")
  let isUserDonor = useUserRoleStatus("donor")
  let isUserCaretaker = useUserRoleStatus("caretaker")

  const [showPopUp, setShowPopUp] = useState(false);
  const [popUpMessage, setPopUpMessage] = useState("")

  const [helpGroups, setHelpGroups] = useState([])

  const [editKey, setEditKey] = useState(-1)

  const {
    register,
    formState: { errors },
    handleSubmit,
    reset,
  } = useForm();

  useEffect(() => {
    axios
        .get("http://127.0.0.1:5000/fundraisers")
        .then((res) => {
          setHelpGroups(res.data.helpGroups)
        })
        .catch((err) => console.log(err));
  },[isLoggedIn,showPopUp,editKey])

  const takeCare = (groupId) => {
    axios
      .put(`http://127.0.0.1:5000/fundraisers/help-group/${groupId}/caretaker/${personId[0]}`)
      .then((res) => {
        setPopUpMessage("Success. You have taken care of chosen group, track 'Your Helpgroups' to learn more.")
        setShowPopUp(true)
      })
      .catch((err) => {
        setPopUpMessage("Error. You haven't taken care of chosen group due to unexpected error.")
        setShowPopUp(true)
      });
  }

  const donate = (data, groupId) => {
    reset()
    axios
      .post(`http://127.0.0.1:5000/fundraisers/help-group/${groupId}/donor/${personId[0]}`,data)
      .then((res) => {
        setPopUpMessage("Success. You have donated chosen group. Thank you!")
        setShowPopUp(true)
        setEditKey(-1)
      })
      .catch((err) => {
        setPopUpMessage("Error. You haven't donated chosen group due to unexpected error.")
        setShowPopUp(true)
        setEditKey(-1)
      });
  }

  return (
  <div className="wrap-fundraisers">
    {isLoggedIn ? (
      <>
        <h1 className="fundraisers-h1">Available fundraisers</h1>
        {showPopUp ? (
        <PopUp setShow={setShowPopUp} defaultBtnText="Ok">
          <h1 className="fundraisers-popup-h1">Help group information</h1>
          <span>
            {popUpMessage}
          </span>
        </PopUp>):(<></>)}

        {helpGroups.map((group,key) => 
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
            <span className="fundraisers-it-txt-50">Caretaker: {group.caretaker? group.caretaker.fullName +' ✔️' : 'Currently no caretaker ❌'} </span>
            
            {!group.caretaker && isUserCaretaker ? (
            <div className="fundraisers-it-txt-50">
            Take care of this group
            <button className="btn-take-care" onClick={() => takeCare(group.groupId)}>
              <i class="fa-solid fa-hands-holding-child"></i>
            </button>
            </div>) : (<></>)}

            {isUserDonor ? (
            <>
            {key === editKey ? (
              <form onSubmit={handleSubmit(e => donate(e,group.groupId))}>
                  <span className="fundraisers-it-txt-50">
                    <input className="donate-input" type="number" min="1" max="999"
                    {...register("amount", {
                      required: true,
                    })}
                    />$
                    <button className="btn-donate" type="submit">
                      <i className="fa-solid fa-check"></i>
                    </button>
                  </span>
              </form>):(
                <div className="fundraisers-it-txt-50">
                Donate this group
                  <button className="btn-take-care" onClick={() => setEditKey(key)}>
                    <i class="fa-solid fa-hand-holding-dollar"></i>
                  </button>
                </div>
              )}
            </>) : (<></>)}

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