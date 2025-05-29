/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        customGreen: "#508D4E",
        customBrown: "#8D493A"
      }
    },
  },
  plugins: [],
};
