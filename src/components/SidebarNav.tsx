import type { AppSectionId } from '../domain/types';
import { NAV_ITEMS } from '../domain/navigation';
import './SidebarNav.css';

interface SidebarNavProps {
  activeSection: AppSectionId;
  onNavigate: (section: AppSectionId) => void;
}

export function SidebarNav({ activeSection, onNavigate }: SidebarNavProps) {
  return (
    <nav className="sidebar-nav" aria-label="Bölüm navigasyonu">
      <p className="sidebar-nav__title">Bölümler</p>
      <ol className="sidebar-nav__list">
        {NAV_ITEMS.map((item, index) => {
          const isActive = item.id === activeSection;

          return (
            <li key={item.id}>
              <button
                type="button"
                className={`sidebar-nav__item${isActive ? ' is-active' : ''}`}
                aria-current={isActive ? 'true' : undefined}
                onClick={() => onNavigate(item.id)}
              >
                <span className="sidebar-nav__index">{index + 1}</span>
                <span className="sidebar-nav__label">{item.label}</span>
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
