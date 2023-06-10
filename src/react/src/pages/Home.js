import React, { useEffect } from "react";
import axios from "axios";
import "./Home.css";

const Home = (props) => {

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000")
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => console.log(err));
  },[])

  return (
    <>
      <img className="home-bg" alt=""/>
      <h1 className="home-h1">Welcome to our <br/> Website!</h1>
      <h2 className="home-h2-1"> Help people who need it the most by donating one of many families from our portal, funds and gifts will be delivered by our professional caretakers. </h2>
      </>
  );
};

export default Home;