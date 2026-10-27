const password = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

togglePassword.addEventListener("click", () => {
  const visible = password.type === "text";

  password.type = visible ? "password" : "text";
  togglePassword.textContent = visible ? "◉" : "◌";
  togglePassword.setAttribute(
    "aria-label",
    visible ? "Mostrar senha" : "Ocultar senha"
  );
});

document.getElementById("signupForm").addEventListener("submit", (event) => {

  window.location.assign("../pagina-em-branco.html");
});
