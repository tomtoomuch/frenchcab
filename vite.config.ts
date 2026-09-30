/// <reference types="vitest/config" />
import { defineConfig } from 'vite'

export default defineConfig({
    test: {
        envvironment: "jsdom",
        globals: true,
        include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    },
});