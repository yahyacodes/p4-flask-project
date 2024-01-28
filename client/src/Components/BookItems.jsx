import React, { useState } from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BiCommentDetail } from "react-icons/bi";
import { BiTrash } from "react-icons/bi";
import { BiSolidEdit } from "react-icons/bi";
import { useNavigate } from "react-router-dom";

const BookItems = ({ id, title, description, author, deleteBook }) => {
  const navigate = useNavigate();
  return (
    <section className="">
      <div className="max-w-screen-lg mx-auto px-4 md:px-8">
        <ul className="divide-y space-y-3">
          <li
            key={id}
            className="px-4 py-5 duration-150 hover:border-white hover:rounded-xl hover:bg-gray-100"
          >
            <div className="group relative flex justify-end gap-2">
              <div className="invisible group-hover:visible cursor-pointer justify-end hover:text-red-600">
                <BiTrash className="text-lg" onClick={() => deleteBook(id)} />
              </div>
              <div className="invisible group-hover:visible cursor-pointer hover:text-green-600">
                <BiSolidEdit
                  className="text-lg"
                  onClick={() => {
                    navigate(`/editbook/${id}`, { replace: true });
                  }}
                />
              </div>
            </div>
            <div className="flex items-center gap-x-3">
              <div>
                <h3 className="text-base text-gray-800 font-semibold mt-1">
                  Book name: {title}
                </h3>
                <span className="block text-sm text-gray-400 font-medium">
                  Author: {author.authorname}
                </span>
              </div>
            </div>
            <p className="text-gray-600 sm:text-sm">
              Description: {description}
            </p>
            <div className="text-sm text-gray-600 flex items-center gap-6 cursor-pointer mt-1">
              <span className="flex items-center gap-2">
                <BiCategoryAlt className="text-lg" />
                category
              </span>
              <span className="flex items-center gap-2">
                <BiCommentDetail className="text-lg" />
                Book reviews
              </span>
            </div>
          </li>
        </ul>
      </div>
    </section>
  );
};

export default BookItems;
