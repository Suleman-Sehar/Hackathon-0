import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bronze: {
          50: '#fdf8f6',
          100: '#f2e8e5',
          200: '#eaddd7',
          300: '#e0cec7',
          400: '#d2bab0',
          500: '#bfa094',
          600: '#a18072',
          700: '#977669',
          800: '#846358',
          900: '#6f5248',
        },
        gold: {
          50: '#fbf7e7',
          100: '#f7eecf',
          200: '#f0dda0',
          300: '#e8c76e',
          400: '#e0b345',
          500: '#d9a32e',
          600: '#cf8b1f',
          700: '#ad6f19',
          800: '#8b5a1d',
          900: '#704b1f',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'bronze-gradient': 'linear-gradient(135deg, #bfa094 0%, #846358 100%)',
        'gold-gradient': 'linear-gradient(135deg, #e8c76e 0%, #8b5a1d 100%)',
      },
    },
  },
  plugins: [],
};
export default config;
