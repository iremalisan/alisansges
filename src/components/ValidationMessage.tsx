import './ValidationMessage.css';

interface ValidationMessageProps {
  id?: string;
  message?: string;
}

export function ValidationMessage({ id, message }: ValidationMessageProps) {
  if (!message) {
    return null;
  }

  return (
    <p id={id} className="validation-message" role="alert">
      {message}
    </p>
  );
}
