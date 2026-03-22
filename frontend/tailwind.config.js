// tailwind.config.js

module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Add a custom text-shadow utility
      textShadow: {
        glow: "0 0 8px rgba(255, 255, 255, 0.8)", // Custom text glow effect
      },
    },
  },
  plugins: [
    function ({ addUtilities }) {
      const newUtilities = {
        ".text-shadow-glow": {
          textShadow: "0 0 8px rgba(255, 255, 255, 1)",
        },
      };
      addUtilities(newUtilities, ["responsive", "hover"]);
    },
  ],
};
