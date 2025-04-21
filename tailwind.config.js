/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html', // project level
    './*/templates/**/*.html', // app level
    './static/**/*.js',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {
      width: {
        '200': '200px',
        '500': '500px',
        '700': '700px',
        '900': '900px',
        '1200': '1200px',
       },
       height: {
        '400': '400px',
        '500': '500px',
        '700': '700px',
       },
       fontSize: {
        '2xs': '10px'
       },
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('daisyui'),
  ],
}

