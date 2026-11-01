/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        w3: {
          green: '#04AA6D',
          greenHover: '#059862',
          greenDark: '#047857',
          slate: '#282A35',
          slateDeep: '#1D2A35',
          mint: '#D9EEE1',
          yellow: '#FFF4A3',
          pink: '#FFC0C7',
          example: '#E7E9EB',
          canvas: '#FAFAF8',
          card: '#FFFFFF',
          ink: '#18181B',
          muted: '#52525B',
          line: '#E4E4E0'
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '"IBM Plex Sans Arabic"', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', '"IBM Plex Sans Arabic"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      }
    }
  },
  plugins: [],
};
