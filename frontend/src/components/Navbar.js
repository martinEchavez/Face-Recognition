import React, {useState} from 'react';
import { FcVideoCall } from "react-icons/fc";
import {Link} from 'react-router-dom';
import { store } from 'react-notifications-component';
import { Tooltip } from 'reactstrap';
const API = process.env.REACT_APP_API;

export const Navbar = () => {

 const [start, setStart] = useState('')
 const [tooltipInfo, setTooltipInfo] = useState(false);
 const toggleInfo = () => setTooltipInfo(!tooltipInfo);

 const handleSubmit = async (e) => {
  e.preventDefault();
  store.addNotification({
    title: "Ha iniciado la grabación",
    message: "Se está iniciando la grabación",
    type: "info",
    insert: "top",
    container: "top-center",
    animationIn: ["animated", "fadeIn"],
    animationOut: ["animated", "fadeOut"],
    dismiss: {
      duration: 3000,
      onScreen: true
    }
  });
  const res = await fetch(`${API}/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      start
     })
  })
  const data = await res.json();
  console.log(data);
  store.addNotification({
    title: "Finalizando",
    message: "Ha finalizado la grabación.",
    type: "info",
    insert: "top",
    container: "top-center",
    animationIn: ["animated", "fadeIn"],
    animationOut: ["animated", "fadeOut"],
    dismiss: {
      duration: 3000,
      onScreen: true
    }
  });
 }

 return (
  <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
  <Link className="navbar-brand" to="/">
        <img src="https://pngimage.net/wp-content/uploads/2018/06/r-logo-png-2.png" width={30} height={30} className="d-inline-block align-top" alt="" />
        Recognizer
      </Link>
  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
    <span className="navbar-toggler-icon" />
  </button>
  <div className="collapse navbar-collapse" id="navbarColor01">
    <ul className="navbar-nav mr-auto">
      <li className="nav-item active">
        <Link className="nav-link" to="/">Inicio</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link" to="/about">¿Quiénes somos?</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link" to="/services">Servicios</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link" to="/contact">Contáctenos</Link>
      </li>
    </ul>
    <form
      onSubmit={handleSubmit}
      className="form-inline my-2 my-lg-0">
      <button
        className="btn btn-outline-success mr-5"
        value={start}
        onClick={() => setStart(true)}
        id="TooltipInfo"
        >
          <Tooltip
            placement="bottom-start"
            isOpen={tooltipInfo}
            target="TooltipInfo"
            toggle={toggleInfo}>
              Iniciar reconocimiento
           </Tooltip>
          <FcVideoCall size={30} />
      </button>
      <input className="form-control mr-sm-2" type="text" placeholder="Buscar" />
      <button className="btn btn-secondary my-2 my-sm-0" type="submit">Buscar</button>
    </form>
  </div>
 </nav>
 )
}