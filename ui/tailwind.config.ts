import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "SF Pro Text",
          "system-ui",
          "sans-serif",
        ],
        display: [
          "-apple-system",
          "BlinkMacSystemFont",
          "SF Pro Display",
          "system-ui",
          "sans-serif",
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "SF Mono",
          "Menlo",
          "monospace",
        ],
      },
      colors: {
        surface: {
          DEFAULT: "#0a0a0c",
          elevated: "#161618",
          muted: "#232326",
          subtle: "#1c1c1f",
        },
        ink: {
          DEFAULT: "#f5f5f7",
          secondary: "#a1a1a6",
          muted: "#6e6e73",
          faint: "#3a3a3c",
          hairline: "#2c2c2e",
        },
        accent: {
          DEFAULT: "#0a84ff",
          hover: "#409cff",
          muted: "rgba(10, 132, 255, 0.14)",
        },
        status: {
          success: "#30d158",
          warning: "#ff9f0a",
          danger: "#ff453a",
          info: "#64d2ff",
        },
      },
      letterSpacing: {
        tightest: "-0.028em",
        tighter: "-0.022em",
        tight: "-0.016em",
      },
      boxShadow: {
        card: "0 0 0 1px rgba(255,255,255,0.06), 0 1px 2px rgba(0,0,0,0.4)",
        "card-hover":
          "0 0 0 1px rgba(255,255,255,0.1), 0 12px 32px rgba(0,0,0,0.5)",
        subtle: "0 0 0 1px rgba(255,255,255,0.06)",
      },
      maxWidth: {
        prose: "42rem",
        page: "72rem",
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
            color: "#a1a1a6",
            '[class~="lead"]': { color: "#a1a1a6" },
            a: {
              color: "#0a84ff",
              fontWeight: "500",
              textDecoration: "none",
              "&:hover": { textDecoration: "underline" },
            },
            strong: { color: "#f5f5f7", fontWeight: "600" },
            h1: {
              color: "#f5f5f7",
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "SF Pro Display", system-ui, sans-serif',
              letterSpacing: "-0.022em",
              fontWeight: "600",
            },
            h2: {
              color: "#f5f5f7",
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "SF Pro Display", system-ui, sans-serif',
              letterSpacing: "-0.018em",
              fontWeight: "600",
            },
            h3: {
              color: "#f5f5f7",
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "SF Pro Display", system-ui, sans-serif',
              letterSpacing: "-0.016em",
              fontWeight: "600",
            },
            h4: { color: "#f5f5f7" },
            code: {
              backgroundColor: "#232326",
              color: "#f5f5f7",
              padding: "0.125rem 0.375rem",
              borderRadius: "0.25rem",
              fontWeight: "500",
              border: "1px solid rgba(255,255,255,0.06)",
            },
            "code::before": { content: '""' },
            "code::after": { content: '""' },
            hr: { borderColor: "#2c2c2e" },
            blockquote: {
              color: "#a1a1a6",
              borderLeftColor: "#3a3a3c",
              fontStyle: "normal",
              fontWeight: "400",
            },
            "ul > li::marker": { color: "#6e6e73" },
            "ol > li::marker": { color: "#6e6e73" },
            table: {
              fontSize: "0.875rem",
            },
            "thead th": {
              color: "#f5f5f7",
              borderBottomColor: "#3a3a3c",
            },
            "tbody tr": {
              borderBottomColor: "#2c2c2e",
            },
            pre: {
              backgroundColor: "#161618",
              color: "#f5f5f7",
              border: "1px solid rgba(255,255,255,0.06)",
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

export default config;
