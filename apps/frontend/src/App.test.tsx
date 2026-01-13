import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, test } from "vitest";
import App from "./App";

test("renders nav and chat entrypoint", () => {
  render(
    <MemoryRouter initialEntries={["/"]}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText("Helix BA Shop")).toBeInTheDocument();
  expect(screen.getByText("Chat agent")).toBeInTheDocument();
});

