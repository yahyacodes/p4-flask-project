const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      token: null,
      // bookData: null,
      books: [],
    },
    actions: {
      syncToken: () => {
        const token = sessionStorage.getItem("token");
        if (token && token != "" && token != undefined)
          setStore({ token: token });
      },

      logout: () => {
        sessionStorage.removeItem("token");
        console.log("Logging out");
        setStore({ token: null });
      },

      login: async (data) => {
        const opts = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        };

        console.log("Request Headers:", opts.headers);

        try {
          const res = await fetch("http://127.0.0.1:5555/login", opts);
          if (res.status !== 200) {
            alert("Status != 200");
            return false;
          }
          const data = await res.json();
          console.log(data);
          sessionStorage.setItem("token", data.access_token);
          setStore({ token: data.access_token });
          console.log(data.access_token);
          return true;
        } catch (error) {
          console.error("There has been an error login in", error);
        }
      },

      // getBooks: async () => {
      //   const store = getStore();
      //   const opts = {
      //     headers: {
      //       Authorization: "Bearer " + store.token,
      //     },
      //   };
      //   try {
      //     const resp = await fetch("http://127.0.0.1:5555/books", opts);
      //     const data = await resp.json();
      //     setStore({ bookData: data.bookData });
      //     return data;
      //   } catch (error) {
      //     console.log("Error loading books data from backend", error);
      //   }
      // },
    },
  };
};

export default getState;
