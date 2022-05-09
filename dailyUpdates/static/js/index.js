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

// hide navbar

document.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (document.scrollingElement.scrollTop > 100) {
    navbar.classList.add("navbar-scroll");
  } else {
    navbar.classList.remove("navbar-scroll");
  }
});
