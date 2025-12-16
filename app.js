const list = document.querySelector(".todos");
const search = document.querySelector(".search input");

/*
  Load assignment plan from plan.json
*/
fetch("plan.json")
  .then((res) => res.json())
  .then((data) => {
    // Set page title if exists
    const header = document.querySelector("h1");
    if (header && data.assignment_title) {
      header.innerText = data.assignment_title;
    }

    list.innerHTML = "";

    data.mini_tasks.forEach((task) => {
      const li = document.createElement("li");
      li.className =
        "list-group-item d-flex justify-content-between align-items-center";

      li.innerHTML = `
        <span>
          ${task.task}<br/>
          <small class="text-muted">
            ${task.estimated_minutes} min · due ${task.due_by}
          </small>
        </span>
        <i class="far fa-trash-alt delete"></i>
      `;

      list.appendChild(li);
    });
  })
  .catch((err) => {
    console.error("Failed to load plan.json", err);
  });

/*
  Delete todos
*/
list.addEventListener("click", (e) => {
  if (e.target.classList.contains("delete")) {
    e.target.parentElement.remove();
  }
});

/*
  Filter todos
*/
const filterTodos = (term) => {
  Array.from(list.children)
    .filter((todo) => !todo.textContent.toLowerCase().includes(term))
    .forEach((todo) => todo.classList.add("filtered"));

  Array.from(list.children)
    .filter((todo) => todo.textContent.toLowerCase().includes(term))
    .forEach((todo) => todo.classList.remove("filtered"));
};

search.addEventListener("keyup", () => {
  const term = search.value.trim().toLowerCase();
  filterTodos(term);
});
