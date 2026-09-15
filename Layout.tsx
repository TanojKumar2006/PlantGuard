import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { useState } from 'react';
import {
  Leaf, LayoutDashboard, Microscope, Clock, BookOpen,
  FlaskConical, BarChart3, Info, Sun, Moon, Menu, X
} from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import clsx from 'clsx';

const NAV = [
  { to: '/',          label: 'Home',           icon: Leaf },
  { to: '/dashboard', label: 'Dashboard',      icon: LayoutDashboard },
  { to: '/diagnose',  label: 'Diagnose',        icon: Microscope },
  { to: '/history',   label: 'History',         icon: Clock },
  { to: '/library',   label: 'Plant Library',   icon: BookOpen },
  { to: '/treatment', label: 'Treatment Guide', icon: FlaskConical },
  { to: '/analytics', label: 'Analytics',       icon: BarChart3 },
  { to: '/about',     label: 'About',           icon: Info },
];

export default function Layout() {
  const { darkMode, toggleDark } = useAppStore();
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen flex flex-col bg-[rgb(var(--color-bg))] transition-colors duration-300">
      {/* Top navbar */}
      <header className="sticky top-0 z-50 glass border-b border-[rgb(var(--color-border))]">
        <div className="max-w-screen-2xl mx-auto px-4 h-16 flex items-center gap-4">
          {/* Logo */}
          <NavLink to="/" className="flex items-center gap-2 font-bold text-lg shrink-0">
            <span className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-ai-500 flex items-center justify-center shadow-glow-green">
              <Leaf className="w-5 h-5 text-white" />
            </span>
            <span className="hidden sm:block">
              <span className="text-gradient font-extrabold">PlantGuard</span>
              <span className="text-gray-400 dark:text-gray-500 ml-1 font-light">AI</span>
            </span>
          </NavLink>

          {/* Desktop nav */}
          <nav className="hidden lg:flex items-center gap-1 ml-6 flex-1 overflow-x-auto">
            {NAV.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) => clsx('nav-link', isActive && 'active')}
              >
                <Icon className="w-4 h-4" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-2">
            {/* Dark mode toggle */}
            <button
              onClick={toggleDark}
              className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-gray-500" />}
            </button>
            {/* Diagnose CTA */}
            <NavLink to="/diagnose" className="btn-primary hidden sm:inline-flex text-sm">
              <Microscope className="w-4 h-4" />
              Diagnose
            </NavLink>
            {/* Mobile menu */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="lg:hidden p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile nav */}
        {mobileOpen && (
          <nav className="lg:hidden border-t border-[rgb(var(--color-border))] px-4 py-3 flex flex-col gap-1">
            {NAV.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) => clsx('nav-link', isActive && 'active')}
              >
                <Icon className="w-4 h-4" />
                {label}
              </NavLink>
            ))}
          </nav>
        )}
      </header>

      {/* Page content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-[rgb(var(--color-border))] py-6 px-4">
        <div className="max-w-screen-xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-400 dark:text-gray-500">
          <div className="flex items-center gap-2">
            <Leaf className="w-3.5 h-3.5 text-brand-500" />
            <span>PlantGuard AI · Neural Networks & Deep Learning Mini Project</span>
          </div>
          <span>Built with EfficientNetB0 · TensorFlow · FastAPI · React</span>
        </div>
      </footer>
    </div>
  );
}
