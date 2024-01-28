import React from "react";
import BookItems from "./BookItems";

const BooksList = ({ books, deleteBook }) => {
  console.log(books);
  return (
    <>
      <div>
        {books.map((book) => (
          <BookItems key={book.id} {...book} deleteBook={deleteBook} />
        ))}
      </div>
    </>
  );
};

export default BooksList;
