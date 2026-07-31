import type { ReactNode } from 'react';
import './SectionCard.css';

interface SectionCardProps {
  id: string;
  title: string;
  description?: string;
  children: ReactNode;
}

export function SectionCard({ id, title, description, children }: SectionCardProps) {
  return (
    <section id={id} className="section-card" aria-labelledby={`${id}-title`}>
      <header className="section-card__header">
        <h2 id={`${id}-title`} className="section-card__title">
          {title}
        </h2>
        {description ? (
          <p className="section-card__description">{description}</p>
        ) : null}
      </header>
      <div className="section-card__body">{children}</div>
    </section>
  );
}
