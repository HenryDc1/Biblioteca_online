/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/myapp/*.{html,js}", "./templates/myapp/**/*.{html,js}, ./templates/myapp/**/**/*.{html,js}, ./templates/myapp/registration/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}

