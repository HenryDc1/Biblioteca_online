/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/myapp/*.{html,js}", "./templates/myapp/**/*.{html,js}, ./templates/myapp/**/**/*.{html,js}, ./templates/myapp/registration/*.{html,js}, ./templates/myapp/dashboard/canviar_contrasenya.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}

