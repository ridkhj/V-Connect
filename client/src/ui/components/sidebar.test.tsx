import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Sidebar from "./sidebar";

// Mocka apenas o FileUploader, porque ele é de outro arquivo
vi.mock("@/components/file-uploader", () => ({
  default: () => <div>FileUploader Component</div>
}));

describe("Sidebar", () => {
  it("renderiza o logo e o título Connect", () => {
    render(<Sidebar />);

    const logo = screen.getByAltText("Logo");
    const title = screen.getByText("Connect");

    expect(logo).toBeInTheDocument();
    expect(title).toBeInTheDocument();
  });

  it("renderiza o componente FileUploader", () => {
    render(<Sidebar />);

    expect(screen.getByText("FileUploader Component")).toBeInTheDocument();
  });

  it("renderiza o rodapé com direitos reservados", () => {
    render(<Sidebar />);

    expect(
      screen.getByText("© 2025 V Connect | Todos os direitos reservados.")
    ).toBeInTheDocument();
  });
});
