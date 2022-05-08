let editorDiv = document.querySelector("#editorDiv");

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

// toggle button

// const checkbox = document.querySelector("#checkbox");
// checkbox.attributes.checked = false;

// const btn = document.querySelector(".round");
// const fullStory = document.querySelector("#fullStory");
// fullStory.style.display = "none";

// const toggleMe = document.querySelector(".toggle");

// btn.addEventListener("click", (e) => {
//   if (
//     checkbox.attributes.checked == false &&
//     fullStory.style.display === "none"
//   ) {
//     fullStory.style.display = "block";
//     toggleMe.style.display = "none";
//     checkbox.attributes.checked = true;
//   } else {
//     fullStory.style.display = "none";
//     toggleMe.style.display = "block";
//     checkbox.attributes.checked = false;
//   }
// });
