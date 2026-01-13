import { Link, Route, Routes } from "react-router-dom";
import "./App.css";
import { useAuthToken } from "./auth";
import { HomePage } from "./pages/HomePage";
import { ProductPage } from "./pages/ProductPage";
import { CheckoutPage } from "./pages/CheckoutPage";
import { CheckoutSuccessPage } from "./pages/CheckoutSuccessPage";
import { CheckoutCancelPage } from "./pages/CheckoutCancelPage";
import { AdminLoginPage } from "./pages/admin/AdminLoginPage";
import { AdminProductsPage } from "./pages/admin/AdminProductsPage";
import { AdminPromosPage } from "./pages/admin/AdminPromosPage";
import { AdminOrdersPage } from "./pages/admin/AdminOrdersPage";

export default function App() {
  const { token, setToken } = useAuthToken();

  return (
    <div className="container">
      <header className="header">
        <div className="brand">
          <Link to="/">Helix BA Shop</Link>
        </div>
        <nav className="nav">
          <Link to="/">Chat</Link>
          <Link to="/admin">Admin</Link>
          {token ? (
            <button className="linkButton" onClick={() => setToken(null)}>
              Sign out
            </button>
          ) : (
            <span className="muted">Not signed in</span>
          )}
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products/:id" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
        <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />

        <Route path="/admin" element={<AdminLoginPage />} />
        <Route path="/admin/products" element={<AdminProductsPage />} />
        <Route path="/admin/promos" element={<AdminPromosPage />} />
        <Route path="/admin/orders" element={<AdminOrdersPage />} />
      </Routes>
    </div>
  );
}
