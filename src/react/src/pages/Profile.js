import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import "./Profile.css";
import useLoginStatus from "../hooks/useLoginStatus";
import useLocalStorage from "../hooks/useLocalStorage";
import DeleteProfileButton from "../components/DeleteProfileButton";
import useUserRoleStatus from "../hooks/useUserRoleStatus";
import EditField from "../components/EditField";
import PopUp from "../components/PopUp";

const Profile = () => {
  const [profile, setProfile] = useState(null);

  const isLoggedIn = useLoginStatus()
  let personId = useLocalStorage("personId")
  let isUserDonor = useUserRoleStatus("donor")
  let isUserCaretaker = useUserRoleStatus("caretaker")
  const navigate = useNavigate();

  const [editField, setEditField] = useState("");

  const [showPopUp, setShowPopUp] = useState(false);
  const [popUpMessage, setPopUpMessage] = useState("")

  useEffect(() => {
    if (isLoggedIn) {
      axios
        .get(`http://127.0.0.1:5000/profile/${personId[0]}`)
        .then((res) => {
          setProfile(res.data);
        })
        .catch((err) => console.log(err));
    }
  }, [isLoggedIn, navigate, editField]);

  const updatePopUpMessage = (popUpMsg) => {
    setPopUpMessage(popUpMsg)
    setShowPopUp(true);
    setEditField("")
  }

  const logOut = () => {
    localStorage.removeItem("role");
    localStorage.removeItem("personId");
    setProfile(null);
    window.location.reload();
  };

  return (
    <div className="wrap-profile">
      {profile ? (
        <>
          {showPopUp ? (
          <PopUp setShow={setShowPopUp} defaultBtnText="Ok">
            <h1 className="leagues-popup-h1">Edit field info</h1>
            <span>
              {popUpMessage}
            </span>
          </PopUp>):(<></>)
          }
          <div className="left-panel">
            <div className="photo-panel"></div>
            <div></div>
          </div>
          <div className="right-panel">
            <h1 className="profile-h1">Profile information and settings</h1>
            <div className="profile-it">
              <span className="profile-it-txt">Email</span>
              <span className="profile-it-txt">
                {profile.email}
              </span>
            </div>
            <div className="profile-it">
              <span className="profile-it-txt">Phone number</span>
              <span className="profile-it-txt">
                {profile.phoneNumber}
              </span>
            </div>
            
            <div className="profile-it">
              <span className="profile-it-txt">First Name</span>

              {editField === profile.firstName ? (
              <EditField updatePopUpMessage={updatePopUpMessage} personId={personId} field={{'content':profile.firstName,'table':'person','record':'forename'}}/>
              ) : (
              <>
              <span className="profile-it-txt">
                {profile.firstName}
              </span>
              <button className="btn-edit-profile" onClick={()=>setEditField(profile.firstName)}>
                <i className="fa-solid fa-pen-to-square"></i>
              </button></>)}  
            </div>

            <div className="profile-it">
              <span className="profile-it-txt">Last Name</span>

              {editField === profile.lastName ? (
              <EditField updatePopUpMessage={updatePopUpMessage} personId={personId} field={{'content':profile.lastName,'table':'person','record':'surname'}}/>
              ) : (
              <>
              <span className="profile-it-txt">
                {profile.lastName}
              </span>
              <button className="btn-edit-profile" onClick={()=>setEditField(profile.lastName)}>
                <i className="fa-solid fa-pen-to-square"></i>
              </button></>)}  
            </div>

            {isUserDonor ? (
            <>
              <div className="profile-it">
                <span className="profile-it-txt">Donated packs</span>
                <span className="profile-it-txt">
                  {profile.packCount}
                </span>
              </div>
              <div className="profile-it">
                <span className="profile-it-txt">Donations sum</span>
                <span className="profile-it-txt">
                  {profile.donationsSum}
                </span>
              </div>
              <div className="profile-it">
                <span className="profile-it-txt">Points</span>
                <span className="profile-it-txt">
                  {profile.points}
                </span>
              </div>
            </>):(<></>)}

            {isUserCaretaker ? (
            <>
              <div className="profile-it">
                <span className="profile-it-txt">Donation Place</span>
                <span className="profile-it-txt">
                  {profile.donationPlace}
                </span>
              </div>
              <div className="profile-it">
                <span className="profile-it-txt">Owns a car</span>
                <span className="profile-it-txt">
                  {profile.carOwner}
                </span>
              </div>
              <div className="profile-it">
                <span className="profile-it-txt">Active Hours</span>
                <span className="profile-it-txt">
                  {profile.activeHoursStart}-{profile.activeHoursStart}
                </span>
              </div>
            </>):(<></>)}

            <div className="btns-profile">
              <button className="btn-log-out" onClick={logOut}>
                Log out
              </button>
              <DeleteProfileButton email={profile.email} />
            </div>
          </div>
        </>
      ) : (
        <div className="log-out-wrap">
          <span className="profile-span">You've been logged out or you don't have sufficient permission to view this tab, sign in again or sign up for free!</span>
          <div className="btns-profile">
            <Link className="btn-log-out" to="/SignIn">
              Sign in
            </Link>
            <Link className="btn-log-out" to="/SignUp">
              Sign up
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
