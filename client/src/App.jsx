import { useEffect, useState, useContext } from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";
import BooksList from "./Components/BooksList";
import Navbar from "./Components/Navbar";
import AddBooks from "./Components/AddBooks";
import EditBook from "./Components/EditBook";
import Users from "./Components/Users";
import Signup from "./Components/Signup";
import injectContext, { Context } from "./Store/appContext";

function App() {
  const [data, setData] = useState([]);
  const { store, actions } = useContext(Context);

  useEffect(() => {
    if (store.token && store.token != "" && store.token != undefined)
      fetch("http://127.0.0.1:5000/books")
        .then((res) => res.json())
        .then((data) => setData(data));
  }, [store.token]);

  const addNewBook = (newBookData) => {
    fetch("http://127.0.0.1:5000/books", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newBookData),
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
    console.log(newBookData);
  };

  const editBook = (bookData) => {
    fetch("http://127.0.0.1:5000/books/" + bookData.id, {
      method: "PATCH",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bookData),
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
    console.log(bookData);
  };

  const deleteBook = (id) => {
    fetch("http://127.0.0.1:5000/books/" + id, {
      method: "DELETE",
    });
    let remaining = data.filter((item) => item.id !== id);
    setData(remaining);
  };

  const addUSer = (createNewUser) => {
    fetch("http://127.0.0.1:5000/users", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(createNewUser),
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
    console.log(createNewUser);
  };

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Users />} />
        <Route path="/signup" element={<Signup createUser={addUSer} />} />
        <Route
          path="/books"
          element={<BooksList books={data} deleteBook={deleteBook} />}
        />
        <Route path="/addbook" element={<AddBooks addBook={addNewBook} />} />
        <Route
          path="/editbook/:id"
          element={<EditBook books={data} editBook={editBook} />}
        />
      </Routes>
    </>
  );
}

export default injectContext(App);
