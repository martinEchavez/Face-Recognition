import React, {useState, useEffect} from 'react';
import {GoTrashcan, GoPencil } from 'react-icons/go';
import { store } from 'react-notifications-component';
import { Tooltip } from 'reactstrap';
const API = process.env.REACT_APP_API;

const tipeRoles = [
 {id: 1, name: 'Administrativo'},
 {id: 2, name: 'Estudiante'},
 {id: 3, name: 'Docente'}
]

export const Users = () => {

 const [tooltipEdit, setTooltipEdit] = useState(false);
 const [tooltipDelete, setTooltipDelete] = useState(false);
 const toggleEdit = () => setTooltipEdit(!tooltipEdit);
 const toggleDelete = () => setTooltipDelete(!tooltipDelete);

 const [name, setName] = useState('')
 const [lastName, setLastName] = useState('')
 const [tipeUser, setTipeUser] = useState('Estudiante')
 const [idNumber, setIdNumber] = useState('')
 const [cellPhone, setCellPhone] = useState('')
 const [email, setEmail] = useState('')

 const [editing, setEditing] = useState(false)
 const [id, setId] = useState('')

 const [users, setUsers] = useState([])

 const handleSubmit = async (e) => {
  try {
    e.preventDefault();

    if(!editing) {
     const res = await fetch(`${API}/users`, {
      method: 'POST',
      headers: {//Tipo de dato que se envia
       'Content-Type': 'application/json'
      },
      body: JSON.stringify({
       name,
       lastName,
       tipeUser,
       idNumber,
       cellPhone,
       email
      })
     })
     const data = await res.json();
     console.log(data);
     store.addNotification({
      title: "Usuario guardado",
      message: "El usuario se ha creado exitosamente.",
      type: "success",
      insert: "top",
      container: "top-center",
      animationIn: ["animated", "fadeIn"],
      animationOut: ["animated", "fadeOut"],
      dismiss: {
        duration: 3000,
        onScreen: true
      }
    });
    } else {
     const res = await fetch(`${API}/users/${id}`, {
      method: 'PUT',
      headers: {
       'Content-Type': 'application/json'
      },
      body: JSON.stringify({
       name,
       lastName,
       tipeUser,
       idNumber,
       cellPhone,
       email
      })
     })
     const data = await res.json();
     console.log(data)
     setEditing(false)
     setId('')
     store.addNotification({
      title: "Usuario editado",
      message: "El usuario ha sido editado correctamente.",
      type: "success",
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
  
    await getUsers();
    setName('')
    setLastName('')
    setTipeUser('')
    setIdNumber('')
    setCellPhone('')
    setEmail('')
  } catch (error) {
    alert('Error handleSubmit: '+ error);
  }
 }

 const getUsers = async () => {
  try {
    const res = await fetch(`${API}/users`)
    const data = await res.json();
    setUsers(data)
  } catch (error) {
    alert('Error getUsers: ' + error);
  }
 }

 useEffect(() => {
  getUsers();
 }, [])

 const deleteUser = async (id, name) => {
  try {
    const resConfirm = window.confirm('Esta seguro de eliminar al usuario: ' + name);
    if(resConfirm){
     const res = await fetch(`${API}/users/${id}`,{
      method : 'DELETE'
     });
     const data = await res.json();
     console.log(data);
     await getUsers();
     store.addNotification({
      title: "Usuario eliminado",
      message: "El usuario ha sido eliminado correctamente.",
      type: "danger",
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
  } catch (error) {
    alert('Error deleteUser: '+ error);
  }
 }

 const editUser = async (id) => {
  try {
    const res = await fetch(`${API}/user/${id}`)
    const data = await res.json();
  
    setEditing(true)
    setId(id)
  
    setName(data.name)
    setLastName(data.lastName)
    setTipeUser(data.tipeUser)
    setIdNumber(data.idNumber)
    setCellPhone(data.cellPhone)
    setEmail(data.email)
  } catch (error) {
    alert('Error editUser: ' + error);
  }
 }

 return(
  <div className="row">
   <div className="col-md-3 m-3">
    <form onSubmit={handleSubmit} className="card card-body">
     <div className="form-group">
      <input
       type="text"
       onChange={e => setName(e.target.value)}
       value={name}
       className="form-control"
       placeholder="Nombre"
       autoFocus
      />
     </div>
     <div className="form-group">
      <input
       type="text"
       onChange={e => setLastName(e.target.value)}
       value={lastName}
       className="form-control"
       placeholder="Apellido"
      />
     </div>
     <div className="form-group">
      <select
       value={tipeUser}
       onChange={e => setTipeUser((e.target.value))}
       className="form-control"
      >
       {tipeRoles.map(rol =>(
        <option key={rol.id} value={rol.name}>
         {rol.name}
        </option>
       ))}
      </select>
     </div>
     <div className="form-group">
      <input
       type="number"
       onChange={e => setIdNumber(e.target.value)}
       value={idNumber}
       className="form-control"
       placeholder="N°. Identificación"
      />
     </div>
     <div className="form-group">
      <input
       type="number"
       onChange={e => setCellPhone(e.target.value)}
       value={cellPhone}
       className="form-control"
       placeholder="Teléfono"
      />
     </div>
     <div className="form-group">
      <input
       type="email"
       onChange={e => setEmail(e.target.value)}
       value={email}
       className="form-control"
       placeholder="Email"
      />
     </div>
     <button className="btn btn-success btn-block">
      {editing ? 'Editar usuario': 'Crear usuario'}
     </button>
    </form>
   </div>
   <div className="col-md-8 m-2">
    <div className="table-responsive">
     <table className="table table-hover">
      <thead>
       <tr>
        <th>Nombre</th>
        <th>Apellido</th>
        <th>Usuario</th>
        <th>N° identificación</th>
        <th>Teléfono</th>
        <th>Email</th>
        <th className="text-center" colSpan="2">Opciones</th>
       </tr>
      </thead>
      <tbody>
       {users.map((user, index) => (
        <tr key={index} className="table-success">
        <td>{user.name}</td>
        <td>{user.lastName}</td>
        <td>{user.tipeUser}</td>
        <td>{user.idNumber}</td>
        <td>{user.cellPhone}</td>
        <td>{user.email}</td>
        <td className="text-center">
         <button
          className="btn btn-outline-primary"
          onClick={() => editUser(user._id)}
          id="TooltipEdit"
         >
           <Tooltip
            placement="top-start"
            isOpen={tooltipEdit}
            target="TooltipEdit"
            toggle={toggleEdit}>
              Editar
           </Tooltip>
           <GoPencil size={20}/>
         </button>
        </td>
        <td>
        <button
         className="btn btn-outline-primary"
         onClick={() => deleteUser(user._id, user.name)}
         id="TooltipDelete"
        >
          <Tooltip
            placement="top-start"
            isOpen={tooltipDelete}
            target="TooltipDelete"
            toggle={toggleDelete}>
              Eliminar
           </Tooltip>
          <GoTrashcan size={20}/>
         </button>
        </td>
       </tr>
       ))}
      </tbody>
     </table>
    </div>
   </div>
  </div>
 )
}