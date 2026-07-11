import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

Object.assign(import.meta.env, {
  BASE_URL: "/",
  SITE: "http://localhost:4321",
  PUBLIC_SITE_URL: "http://localhost:4321",
});

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = "";
  localStorage.clear();
  vi.restoreAllMocks();
});
