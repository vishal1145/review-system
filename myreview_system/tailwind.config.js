module.exports = {
  content: [
    './myapp/templates/**/*.html',
    './templates/**/*.html',    // Include all HTML files in templates folder
    './static/js/**/*.js',      // Include all JavaScript files if you use Tailwind classes in JavaScript
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
