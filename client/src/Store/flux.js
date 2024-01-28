const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      token: null,
      message: null,
      books: [],
    },
    actions: {
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      syncToken: () => {
        const token = sessionStorage.getItem("token");
        console.log("Application loaded SyncToken");
        if (token && token != "" && token != undefined)
          setStore({ token: token });
      },

      login: async (data) => {
        const opts = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        };

        try {
          const res = await fetch("http://127.0.0.1:5555/login", opts);
          if (res.status !== 200) {
            alert("Status != 200");
            return false;
          }
          const data = await res.json();
          sessionStorage.setItem("token", data.access_token);
          setStore({ token: data.access_token });
          console.log(data.access_token);
          return true;
        } catch (error) {
          console.error("There has been an error login in");
        }
      },

      getMessage: async () => {
        try {
          const resp = await fetch("http://127.0.0.1:5555/books");
          const data = await resp.json();
          setStore({ message: data.message });
          return data;
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
      changeColor: (index, color) => {
        const store = getStore();

        const books = store.books.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });

        setStore({ books: books });
      },
    },
  };
};

export default getState;
