import React, { useState } from 'react'
import { useForm } from "react-hook-form";
import axios from "axios";
import "./EditField.css"
const RE_NAME = /^\S.{3,20}$/;

const EditField = ({updatePopUpMessage,personId,field}) => {

  const [edit, setEdit] = useState(true)
  const hideEdit = () => setEdit(false)

  const {
    register,
    formState: { errors },
    handleSubmit,
    reset,
  } = useForm({defaultValues: {content: field.content}});

  const onSubmit = (data) => {
    hideEdit()
    reset()
    data.table=field.table
    data.record=field.record

    axios
      .put(`http://127.0.0.1:5000/profile/${personId[0]}`,data)
      .then((res) => {
        updatePopUpMessage("Success. Field has been edited.")
      })
      .catch((err) => {
        updatePopUpMessage("Error. Field hasn't been edited.")
      });
  }

  return (
  <>
  {edit ? (
  <span className="profile-it-txt">
  <form onSubmit={handleSubmit(onSubmit)} className="form-profile-edit">

    <div>
    <input className="profile-input"
      {...register("content", {
          required: true,
          pattern: { value: RE_NAME },
      })}
    />
    {errors.content ? (<p className="error-txt-edit">Invalid Field name.</p>)
    : (<p className="display-none error-txt-edit">Invalid Field name.</p>)}
    </div>

  <button className="btn-edit-profile" type="submit">
    <i className="fa-solid fa-check"></i>
  </button>
  </form>
  </span>):(<></>)}
  </>
  )
}

export default EditField