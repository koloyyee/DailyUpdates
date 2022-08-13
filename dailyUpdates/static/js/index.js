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

// open menu drawer

function openDrawer() {
  const topMenu = document.querySelector(".top-menu");
  topMenu.style.height = "100%";
  topMenu.style.top = "0%";

  document.querySelector("body").style.overflow = "hidden";
}
document.querySelector(".drawer-button").addEventListener("click", () => {
  openDrawer();
});

// close the drawer
function closeDrawer() {
  const topMenu = document.querySelector(".top-menu");
  topMenu.style.height = "0%";
  topMenu.style.top = "-100%";
  topMenu.style.width = "100%";

  document.querySelector("body").style.overflow = "";
}
document.querySelector(".close-button").addEventListener("click", () => {
  closeDrawer();
});
