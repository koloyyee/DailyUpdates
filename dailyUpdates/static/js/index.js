let editorDiv = document.querySelector("#editorDiv");

// ClassicEditor.create(document.querySelector("#editor")).then((editor) => {
//   editorDiv.addEventListener("submit", (e) => {
//     e.preventDefault();
//     const data = editor.getData();

//   });
// });

const editor = async () => {
  const editor = await ClassicEditor.create(document.querySelector("#editor"));
  editorDiv.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = editor.getData();

    const resp = await fetch("/create", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(data),
    });
    console.log(JSON.stringify(data));
    return resp.json();
  });
};

editor();
