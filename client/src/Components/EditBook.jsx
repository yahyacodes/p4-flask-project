import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import { useParams, useNavigate } from "react-router-dom";

const EditBook = ({ editBook }) => {
  const [book, setBook] = useState({});
  const { id } = useParams();
  useEffect(() => {
    fetch(`http://127.0.0.1:5555/books/${parseInt(id)}`)
      .then((res) => res.json())
      .then((data) => setBook(data));
  }, []);
  const { values, handleChange, handleSubmit } = useFormik({
    initialValues: {
      title: book.title,
      description: book.description,
      authorname: book.author,
      user_id: 1,
      categoryname: book.categoryname,
    },
    onSubmit: (data) => {
      data.id = book.id;
      console.log(book.id);
      editBook(data);
    },
  });
  return (
    <div className="isolate bg-white px-6 py-24 sm:py-32 lg:px-8">
      <div className="mx-auto max-w-2xl text-center">
        <p className="mt-2 text-lg leading-8 text-gray-600">Edit book</p>
      </div>
      <form className="mx-auto mt-16 max-w-xl sm:mt-20" onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label
              htmlFor="book"
              className="block text-sm font-semibold leading-6 text-gray-900"
            >
              Book name
            </label>
            <div className="mt-2.5">
              <input
                type="text"
                name="title"
                id="title"
                value={values.title}
                onChange={handleChange}
                autoComplete="organization"
                className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>
          <div className="sm:col-span-2">
            <label
              htmlFor="author"
              className="block text-sm font-semibold leading-6 text-gray-900"
            >
              Author
            </label>
            <div className="mt-2.5">
              <input
                type="text"
                name="authorname"
                id="authorname"
                value={values.authorname}
                onChange={handleChange}
                autoComplete="author"
                className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>
          <div className="sm:col-span-2">
            <label
              htmlFor="description"
              className="block text-sm font-semibold leading-6 text-gray-900"
            >
              Book Description
            </label>
            <div className="mt-2.5">
              <input
                type="text"
                name="description"
                id="description"
                value={values.description}
                onChange={handleChange}
                autoComplete="description"
                className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              />
            </div>
          </div>
        </div>
        <div className="mt-10">
          <button
            type="submit"
            className="block w-full rounded-md bg-indigo-600 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Edit Book
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditBook;
