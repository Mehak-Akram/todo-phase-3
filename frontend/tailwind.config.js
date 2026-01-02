module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'blue': {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // Main blue
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        'red': {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444', // Main red
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
        'gold': {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b', // Main gold
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        'black': {
          50: '#fafafa',
          100: '#f4f4f5',
          200: '#e4e4e7',
          300: '#d4d4d8',
          400: '#a1a1aa',
          500: '#71717a',
          600: '#52525b',
          700: '#3f3f46',
          800: '#27272a',
          900: '#18181b', // Main black
        },
        'white': '#ffffff',
      },
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce': 'bounce 1s infinite',
      }
    },
  },
  plugins: [
    // Enable arbitrary values support
    function ({ addUtilities }) {
      addUtilities({
        '.mix-blend-multiply': {
          'mix-blend-mode': 'multiply'
        },
        '.filter': {
          'filter': 'blur(0)'
        },
        '.blur-3xl': {
          'filter': 'blur(80px)'
        },
        '.blur-4xl': {
          'filter': 'blur(100px)'
        },
        '.backdrop-blur-xl': {
          'backdrop-filter': 'blur(12px)',
        },
        '.bg-white\\/40': {
          'background-color': 'rgba(255, 255, 255, 0.4)',
        },
        '.border-white\\/60': {
          'border-color': 'rgba(255, 255, 255, 0.6)',
        },
        '.shadow-\\[0_20px_50px_rgba\\(0\\,0\\,0\\,0\\.1\\)\\]': {
          'box-shadow': '0 20px 50px rgba(0, 0, 0, 0.1)',
        },
        '.shadow-\\[0_8px_25px_rgba\\(0\\,123\\,255\\,0\\.4\\)\\]': {
          'box-shadow': '0 8px 25px rgba(0, 123, 255, 0.4)',
        },
      })
    },
  ],
}